"""
AdaptiveLearn AI - Learning Mission Routes
Interactive academic missions where students learn by doing.
Enforces automatic completion and updates concept mastery.
"""

from flask import Blueprint, request, jsonify, session
from services.mission_service import mission_service
from models.mission import MissionModel

missions_bp = Blueprint("missions", __name__)

def _get_active_student_id():
    return session.get("student_id") or 1

@missions_bp.route("/api/missions", methods=["GET"])
def list_missions():
    missions = MissionModel.get_all_missions()
    student_id = _get_active_student_id()
    attempts = MissionModel.get_student_mission_status(student_id)
    attempt_map = {a["mission_id"]: a for a in attempts}

    results = []
    for m in missions:
        att = attempt_map.get(m["id"])
        results.append({
            "id": m["id"],
            "code": m["code"],
            "title": m["title"],
            "scenario_description": m["scenario_description"],
            "difficulty": m["difficulty"],
            "theme": m["theme"],
            "concept_id": m["concept_id"],
            "concept_title": m["concept_title"],
            "course_title": m["course_title"],
            "xp_reward": m["xp_reward"],
            "is_completed": bool(att["is_completed"]) if att else False,
            "current_step": att["current_step"] if att else 1,
            "mistakes_count": att["mistakes_count"] if att else 0
        })

    return jsonify({"missions": results})

@missions_bp.route("/api/missions/<int:mission_id>", methods=["GET"])
def get_mission(mission_id):
    student_id = _get_active_student_id()
    data = mission_service.get_mission_details(mission_id, student_id)
    if not data:
        return jsonify({"error": "Mission not found."}), 404
    return jsonify(data)

@missions_bp.route("/api/missions/<int:mission_id>/attempt", methods=["POST"])
def attempt_step(mission_id):
    student_id = _get_active_student_id()
    payload = request.get_json() or {}
    step_number = int(payload.get("step_number", 1))
    submitted_value = payload.get("submitted_value", "")
    time_spent = int(payload.get("time_spent_seconds", 30))

    if str(submitted_value).strip() == "":
        return jsonify({"error": "Submitted value cannot be empty."}), 400

    result = mission_service.validate_mission_step(
        student_id=student_id,
        mission_id=mission_id,
        step_number=step_number,
        submitted_value=submitted_value,
        time_spent_seconds=time_spent
    )
    return jsonify(result)

@missions_bp.route("/api/missions/<int:mission_id>/status", methods=["GET"])
def get_status(mission_id):
    student_id = _get_active_student_id()
    data = mission_service.get_mission_details(mission_id, student_id)
    if not data:
        return jsonify({"error": "Mission not found."}), 404
    return jsonify({
        "mission_id": mission_id,
        "active_attempt": data.get("active_attempt")
    })
