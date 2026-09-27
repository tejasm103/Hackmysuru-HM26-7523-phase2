"""
AdaptiveLearn AI - Adaptive Learning Flow Routes
Provides the central loop next-best-activity and full adaptive learning path.
"""

from flask import Blueprint, request, jsonify, session
from adaptive.engine import adaptive_engine
from ml.predictor import evaluate_student_concept_ml
from database.db import db

learning_bp = Blueprint("learning", __name__)

def _get_active_student_id():
    return session.get("student_id") or 1

@learning_bp.route("/api/learning/next", methods=["GET"])
def get_next_activity():
    student_id = _get_active_student_id()
    course_id = request.args.get("course_id", type=int)
    next_activity = adaptive_engine.get_next_best_activity(student_id, course_id)
    return jsonify(next_activity)

@learning_bp.route("/api/learning/path", methods=["GET"])
def get_adaptive_path():
    student_id = _get_active_student_id()
    course_id = request.args.get("course_id", type=int) or 1
    
    # Query concepts with student mastery
    concepts = db.query("""
        SELECT c.id, c.code, c.title, c.sequence_order, c.difficulty_level, c.category,
               COALESCE(sm.mastery_score, 0.0) as mastery_score,
               COALESCE(sm.status, 'LOCKED') as status,
               COALESCE(sm.attempts_count, 0) as attempts,
               COALESCE(sm.failed_attempts, 0) as failed_attempts
        FROM concepts c
        LEFT JOIN student_mastery sm ON sm.concept_id = c.id AND sm.student_id = %s
        WHERE c.course_id = %s
        ORDER BY c.sequence_order ASC
    """, (student_id, course_id))

    path = []
    for c in concepts:
        # Determine recommended next action for this step in path
        score = float(c["mastery_score"])
        status = c["status"]
        if status == "LOCKED":
            action = "Locked: Unmet Prerequisites"
            difficulty = "N/A"
        elif score >= 85.0:
            action = "Advanced Competitive Challenge"
            difficulty = "HARD"
        elif score >= 70.0:
            action = "Applied Mission Progression"
            difficulty = "MEDIUM"
        elif score >= 40.0:
            action = "Scaffolded Practice & Guided Mission"
            difficulty = "MEDIUM"
        else:
            action = "Remediation & Prerequisite Review"
            difficulty = "EASY"

        path.append({
            "concept": c,
            "recommended_action": action,
            "difficulty": difficulty
        })

    return jsonify({
        "student_id": student_id,
        "course_id": course_id,
        "adaptive_path": path
    })

@learning_bp.route("/api/learning/complete", methods=["POST"])
def complete_activity():
    student_id = _get_active_student_id()
    data = request.get_json() or {}
    activity_id = data.get("activity_id")
    if activity_id:
        db.execute("""
            UPDATE learning_activities
            SET status = 'completed', completed_at = CURRENT_TIMESTAMP
            WHERE id = %s AND student_id = %s
        """, (activity_id, student_id))
    return jsonify({"status": "success", "message": "Activity recorded as completed."})

@learning_bp.route("/api/ml/status", methods=["GET"])
def get_ml_status():
    student_id = _get_active_student_id()
    concept_id = request.args.get("concept_id", type=int) or 4
    ml_eval = evaluate_student_concept_ml(student_id, concept_id)
    return jsonify(ml_eval)
