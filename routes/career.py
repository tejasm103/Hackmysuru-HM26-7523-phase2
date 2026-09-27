"""
AdaptiveLearn AI - Career & Timetable Routes
"""

from flask import Blueprint, request, jsonify, session
from ai.career import get_career_pathways
from services.timetable_service import timetable_service

career_bp = Blueprint("career", __name__)
timetable_bp = Blueprint("timetable", __name__)

def _get_active_student_id():
    return session.get("student_id") or 1

# Career Routes
@career_bp.route("/api/career/pathways", methods=["GET"])
def get_pathways():
    student_id = _get_active_student_id()
    pathways = get_career_pathways(student_id)
    return jsonify({"pathways": pathways})

@career_bp.route("/api/career/recommendations", methods=["GET"])
def get_recommendations():
    student_id = _get_active_student_id()
    pathways = get_career_pathways(student_id)
    return jsonify({"recommended_pathways": pathways[:2]})

# Timetable Routes
@timetable_bp.route("/api/timetable", methods=["GET"])
def get_timetable():
    student_id = _get_active_student_id()
    data = timetable_service.get_student_timetable(student_id)
    return jsonify(data)

@timetable_bp.route("/api/timetable/generate", methods=["POST"])
def generate_timetable():
    student_id = _get_active_student_id()
    payload = request.get_json() or {}
    hours = float(payload.get("available_hours", 4.0))
    tt_id = timetable_service.generate_adaptive_timetable(student_id, hours)
    data = timetable_service.get_student_timetable(student_id)
    return jsonify({"status": "success", "timetable": data})

@timetable_bp.route("/api/timetable/update", methods=["POST"])
def update_timetable():
    return generate_timetable()
