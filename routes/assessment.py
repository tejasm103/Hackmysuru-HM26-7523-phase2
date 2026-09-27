"""
AdaptiveLearn AI - Assessment Routes
Serves diagnostic and practice items with contextual AI re-theming,
grades student submissions, updates mastery, and triggers downstream concept unlocks.
"""

from flask import Blueprint, request, jsonify, session
from models.assessment import AssessmentModel
from adaptive.mastery import mastery_engine
from ml.predictor import evaluate_student_concept_ml
from ai.retheme import retheme_question
from database.db import db

assessment_bp = Blueprint("assessment", __name__)

def _get_active_student_id():
    return session.get("student_id") or 1

@assessment_bp.route("/api/assessment", methods=["GET"])
def get_assessment():
    concept_id = request.args.get("concept_id", type=int) or 4
    student_id = _get_active_student_id()
    difficulty = request.args.get("difficulty", "MEDIUM")
    should_retheme = request.args.get("retheme", "true").lower() in ("true", "1", "yes")

    # Fetch questions for concept
    questions = db.query("""
        SELECT id, concept_id, difficulty, question_text, question_type,
               option_a, option_b, option_c, option_d, correct_answer, explanation, retheme_theme
        FROM questions
        WHERE concept_id = %s
        ORDER BY id ASC LIMIT 5
    """, (concept_id,))

    # If no questions found for this specific concept, provide questions from concept 4 or 1
    if not questions:
        questions = db.query("SELECT * FROM questions LIMIT 4")

    # Get student's top interest for re-theming
    top_interest = "Space & Astronomy"
    int_rec = db.get_one("""
        SELECT i.name FROM student_interests si
        JOIN interests i ON si.interest_id = i.id
        WHERE si.student_id = %s
        ORDER BY si.affinity_score DESC LIMIT 1
    """, (student_id,))
    if int_rec:
        top_interest = int_rec["name"]

    processed_questions = []
    for q in questions:
        if should_retheme:
            rethemed = retheme_question(q, top_interest)
            processed_questions.append({
                "id": q["id"],
                "concept_id": q["concept_id"],
                "difficulty": q["difficulty"],
                "question_text": rethemed["question_text"],
                "option_a": rethemed["option_a"],
                "option_b": rethemed["option_b"],
                "option_c": rethemed["option_c"],
                "option_d": rethemed["option_d"],
                "theme": rethemed.get("retheme_theme", top_interest),
                "narrative_context": rethemed.get("narrative_context", "Contextualized narrative"),
                "is_rethemed": True
            })
        else:
            processed_questions.append({
                "id": q["id"],
                "concept_id": q["concept_id"],
                "difficulty": q["difficulty"],
                "question_text": q["question_text"],
                "option_a": q["option_a"],
                "option_b": q["option_b"],
                "option_c": q["option_c"],
                "option_d": q["option_d"],
                "is_rethemed": False
            })

    concept = db.get_one("SELECT id, title, code FROM concepts WHERE id = %s", (concept_id,))
    return jsonify({
        "concept": concept,
        "student_top_interest": top_interest,
        "questions": processed_questions
    })

@assessment_bp.route("/api/assessment/submit", methods=["POST"])
def submit_assessment():
    student_id = _get_active_student_id()
    data = request.get_json() or {}
    concept_id = data.get("concept_id", 4)
    answers = data.get("answers", []) # list of { question_id, answer, time_taken }

    if not answers:
        return jsonify({"error": "No answers provided."}), 400

    correct_count = 0
    total_count = len(answers)
    detailed_results = []

    for item in answers:
        qid = item.get("question_id")
        student_ans = str(item.get("answer", "")).strip()
        time_taken = int(item.get("time_taken", 15))

        q = db.get_one("SELECT * FROM questions WHERE id = %s", (qid,))
        if not q:
            continue

        is_corr = (student_ans.lower() == str(q["correct_answer"]).strip().lower())
        if is_corr:
            correct_count += 1

        # Record attempt
        AssessmentModel.record_attempt(student_id, qid, student_ans, is_corr, time_taken)

        detailed_results.append({
            "question_id": qid,
            "student_answer": student_ans,
            "correct_answer": q["correct_answer"],
            "is_correct": is_corr,
            "explanation": q.get("explanation")
        })

    score = round((correct_count / max(1, total_count)) * 100.0, 1)

    # Update Mastery through central mastery engine
    mastery_result = mastery_engine.update_mastery(
        student_id=student_id,
        concept_id=concept_id,
        new_demonstrated_score=score,
        source="assessment",
        mistakes_count=(total_count - correct_count)
    )

    # Re-evaluate ML state
    ml_eval = evaluate_student_concept_ml(student_id, concept_id, persist=True)

    return jsonify({
        "status": "success",
        "score": score,
        "correct_count": correct_count,
        "total_count": total_count,
        "passed": score >= 70.0,
        "mastery_result": mastery_result,
        "unlocked_concepts": mastery_result.get("unlocked_concepts", []),
        "ml_state": ml_eval["predicted_state"],
        "detailed_results": detailed_results
    })
