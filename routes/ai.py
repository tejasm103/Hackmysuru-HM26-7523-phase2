"""
AdaptiveLearn AI - AI REST API Routes
Exposes contextual re-theming, translation, pedagogical tutoring, and career matching.
"""

from flask import Blueprint, request, jsonify, session
from ai.retheme import retheme_question
from ai.translation import translate_content
from ai.tutor import generate_tutor_response
from ai.career import get_career_pathways
from database.db import db

ai_bp = Blueprint("ai", __name__)

def _get_active_student_id():
    return session.get("student_id") or 1

@ai_bp.route("/api/ai/retheme", methods=["POST"])
def retheme_endpoint():
    data = request.get_json() or {}
    question = data.get("question", {})
    interest_theme = data.get("interest_theme", "Space & Astronomy")
    result = retheme_question(question, interest_theme)
    return jsonify(result)

@ai_bp.route("/api/ai/translate", methods=["POST"])
def translate_endpoint():
    data = request.get_json() or {}
    text = data.get("text", "")
    target_language = data.get("target_language", "en")
    translated = translate_content(text, target_language)
    return jsonify({
        "original_text": text,
        "target_language": target_language,
        "translated_text": translated
    })

@ai_bp.route("/api/ai/chat", methods=["POST"])
def chat_endpoint():
    student_id = _get_active_student_id()
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    concept_id = data.get("concept_id")
    if not message:
        return jsonify({"error": "Message is required."}), 400

    response = generate_tutor_response(student_id, message, concept_id)
    return jsonify(response)

@ai_bp.route("/api/ai/explain", methods=["POST"])
def explain_concept():
    data = request.get_json() or {}
    concept_title = data.get("concept_title", "Statistics Variance")
    explanation = (
        f"Conceptual Breakdown for {concept_title}:\n"
        f"Variance measures the average squared deviation of each data point from the mean. "
        f"By squaring differences, we prevent negative deviations from cancelling positive ones, "
        f"and we place proportionally greater weight on distant outliers."
    )
    return jsonify({"concept": concept_title, "explanation": explanation})

@ai_bp.route("/api/ai/career", methods=["POST", "GET"])
def career_endpoint():
    student_id = _get_active_student_id()
    pathways = get_career_pathways(student_id)
    return jsonify({"pathways": pathways})
