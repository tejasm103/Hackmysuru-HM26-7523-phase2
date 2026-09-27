"""
AdaptiveLearn AI - ML Learning State Predictor
Evaluates student learning signals and predicts state (IMPROVING, STABLE, NEEDS_SUPPORT).
CRITICAL: ML is a supporting signal and NEVER unilaterally decides academic mastery.
"""

import json
from ml.model import decision_tree_model
from ml.features import extract_features
from database.db import db

def predict_learning_state(student_stats, student_id=None, concept_id=None, persist=False):
    """
    Computes ML Learning State prediction from input features.
    Returns:
    {
        "predicted_state": "IMPROVING" | "STABLE" | "NEEDS_SUPPORT",
        "confidence_score": float,
        "feature_snapshot": dict,
        "is_struggling": bool
    }
    """
    feature_vector = extract_features(student_stats)
    
    # Predict using DecisionTreeClassifier
    probs = decision_tree_model.predict_proba([feature_vector])[0]
    classes = decision_tree_model.classes_
    max_idx = probs.argmax()
    predicted_state = classes[max_idx]
    confidence_score = round(float(probs[max_idx]), 2)
    
    feature_snapshot = {
        "assessment_score": feature_vector[0],
        "practice_score": feature_vector[1],
        "attempts_count": feature_vector[2],
        "failed_attempts": feature_vector[3],
        "previous_mastery": feature_vector[4],
        "performance_trend": feature_vector[5],
        "video_engagement_ratio": feature_vector[6],
        "time_between_attempts_hours": feature_vector[7]
    }
    
    # Persist prediction in database if requested
    if persist and student_id:
        try:
            db.execute("""
                INSERT INTO ml_predictions (student_id, concept_id, predicted_state, confidence_score, feature_snapshot)
                VALUES (%s, %s, %s, %s, %s)
            """, (student_id, concept_id, predicted_state, confidence_score, json.dumps(feature_snapshot)))
        except Exception as e:
            print(f"[ML Predictor] Notice during db write: {e}")

    return {
        "predicted_state": predicted_state,
        "confidence_score": confidence_score,
        "feature_snapshot": feature_snapshot,
        "is_struggling": predicted_state == "NEEDS_SUPPORT"
    }

def evaluate_student_concept_ml(student_id, concept_id=None, persist=True):
    """Evaluates ML state directly by querying student mastery, predictions, and attempts from database."""
    # 1. Check if a prediction exists for this student and concept
    query_sql = """
        SELECT predicted_state, confidence_score, feature_snapshot
        FROM ml_predictions
        WHERE student_id = %s
    """
    params = [student_id]
    if concept_id:
        query_sql += " AND concept_id = %s"
        params.append(concept_id)
    query_sql += " ORDER BY id DESC LIMIT 1"
    
    existing = db.get_one(query_sql, params)
    if existing and existing.get("predicted_state"):
        snapshot = existing.get("feature_snapshot")
        if isinstance(snapshot, str):
            try:
                snapshot = json.loads(snapshot)
            except Exception:
                snapshot = {}
        return {
            "predicted_state": existing["predicted_state"],
            "confidence_score": float(existing.get("confidence_score") or 0.88),
            "feature_snapshot": snapshot or {},
            "is_struggling": existing["predicted_state"] == "NEEDS_SUPPORT"
        }

    mastery_record = None
    if concept_id:
        mastery_record = db.get_one("""
            SELECT mastery_score, attempts_count, failed_attempts, last_assessment_score
            FROM student_mastery
            WHERE student_id = %s AND concept_id = %s
        """, (student_id, concept_id))
    
    if not mastery_record:
        # Check student overall summary
        return {
            "predicted_state": "STABLE",
            "confidence_score": 0.75,
            "feature_snapshot": {},
            "is_struggling": False
        }

    score = float(mastery_record.get("last_assessment_score") or mastery_record.get("mastery_score") or 50.0)
    attempts = int(mastery_record.get("attempts_count") or 1)
    failed = int(mastery_record.get("failed_attempts") or 0)
    
    trend = 1.0 if (failed == 0 and score >= 70.0) else (-1.0 if (failed >= 2 or score < 45.0) else 0.0)
    
    # Query video engagement duration for this concept
    vid_prog = db.get_one("""
        SELECT COALESCE(SUM(watched_seconds), 0) as total_watch
        FROM student_video_progress svp
        JOIN youtube_videos yv ON svp.video_id = yv.id
        WHERE svp.student_id = %s AND yv.concept_id = %s
    """, (student_id, concept_id))
    
    watch_seconds = vid_prog["total_watch"] if vid_prog else 0
    video_ratio = min(1.0, watch_seconds / 180.0)

    stats = {
        "assessment_score": score,
        "practice_score": score,
        "attempts_count": attempts,
        "failed_attempts": failed,
        "previous_mastery": float(mastery_record.get("mastery_score") or 50.0),
        "video_engagement_ratio": video_ratio
    }
    
    return predict_learning_state(stats, student_id=student_id, concept_id=concept_id, persist=persist)
