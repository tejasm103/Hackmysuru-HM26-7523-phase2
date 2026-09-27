"""
AdaptiveLearn AI - Student Dashboard & Profile Routes
"""

from flask import Blueprint, request, jsonify, session
from models.student import StudentModel
from models.mastery import MasteryModel
from models.course import CourseModel
from adaptive.engine import adaptive_engine
from services.interest_service import interest_service
from services.youtube_service import youtube_service
from ml.predictor import evaluate_student_concept_ml
from database.db import db

student_bp = Blueprint("student", __name__)

def _get_active_student_id():
    """Helper to get logged-in student id or fallback to Rahul (id: 1) for demo evaluation."""
    sid = session.get("student_id")
    if sid:
        return sid
    uid = session.get("user_id")
    if uid:
        st = StudentModel.get_by_user_id(uid)
        if st:
            return st["id"]
    return 1 # Default demo student: Rahul

@student_bp.route("/api/onboarding", methods=["POST"])
def complete_onboarding():
    data = request.get_json() or {}
    user_id = session.get("user_id") or 1
    
    study_level = data.get("study_level", "Grade 10")
    grade = data.get("grade", "10th")
    stream = data.get("stream", "Science & Mathematics")
    preferred_language = data.get("preferred_language", "English")
    school_name = data.get("school_name", "State Model School")
    learning_goal = data.get("learning_goal", "Master Core Foundations")
    career_goal = data.get("career_goal", "Explore STEM Careers")
    interests = data.get("interests", ["Space & Astronomy", "Robotics & Automation"])
    course_code = data.get("course_code", "MATH-10")

    # Update profile
    student_id = StudentModel.create_or_update_profile(
        user_id=user_id,
        study_level=study_level,
        grade=grade,
        stream=stream,
        preferred_language=preferred_language,
        school_id=1,
        learning_goal=learning_goal,
        career_goal=career_goal,
        interests=interests
    )
    session["student_id"] = student_id

    # Auto enroll in requested course
    course = db.get_one("SELECT id FROM courses WHERE code = %s", (course_code,))
    course_id = course["id"] if course else 1
    try:
        CourseModel.enroll_student(student_id, course_id)
    except Exception:
        pass

    return jsonify({
        "status": "success",
        "message": "Onboarding completed successfully.",
        "student_id": student_id,
        "course_id": course_id
    })

@student_bp.route("/api/student/dashboard", methods=["GET"])
def get_dashboard():
    student_id = _get_active_student_id()
    student = StudentModel.get_by_id(student_id)
    if not student:
        return jsonify({"error": "Student record not found."}), 404

    # 1. Overall Mastery
    overall_mastery = MasteryModel.get_overall_mastery_percentage(student_id)

    # 2. Primary Enrolled Course
    courses = CourseModel.get_student_courses(student_id)
    current_course = courses[0] if courses else db.get_one("SELECT * FROM courses WHERE id = 1")
    course_id = current_course["id"] if current_course else 1

    # 3. Central Adaptive Engine Recommendation
    next_activity = adaptive_engine.get_next_best_activity(student_id, course_id)

    # 4. ML Learning State
    focal_cid = next_activity["concept"]["id"]
    ml_eval = evaluate_student_concept_ml(student_id, focal_cid)
    if ml_eval.get("predicted_state") != "NEEDS_SUPPORT":
        struggle_pred = db.get_one("""
            SELECT predicted_state, confidence_score
            FROM ml_predictions
            WHERE student_id = %s AND predicted_state = 'NEEDS_SUPPORT'
            ORDER BY id DESC LIMIT 1
        """, (student_id,))
        if struggle_pred:
            ml_eval = {
                "predicted_state": "NEEDS_SUPPORT",
                "confidence_score": float(struggle_pred.get("confidence_score") or 0.90),
                "is_struggling": True
            }

    # 5. Interest Graph
    interest_data = interest_service.get_student_interest_profile(student_id)

    # 6. Recommended Playlists
    playlists = youtube_service.get_recommended_playlists(student_id, course_id)

    # 7. Check if student has open interventions
    active_interventions = db.query("""
        SELECT iv.*, c.title as concept_title
        FROM interventions iv
        JOIN concepts c ON iv.concept_id = c.id
        WHERE iv.student_id = %s AND iv.status IN ('open', 'assigned', 'in_progress')
    """, (student_id,))

    # 8. Learning Streak
    streak = student.get("learning_streak") or 1

    return jsonify({
        "student": {
            "id": student["id"],
            "name": student["name"],
            "email": student["email"],
            "study_level": student["study_level"],
            "grade": student.get("grade"),
            "stream": student.get("stream"),
            "preferred_language": student.get("preferred_language", "English"),
            "learning_goal": student.get("learning_goal"),
            "career_goal": student.get("career_goal"),
            "streak": streak,
            "overall_mastery": overall_mastery
        },
        "current_course": current_course,
        "next_best_activity": next_activity,
        "ml_state": {
            "state": ml_eval["predicted_state"],
            "confidence": ml_eval["confidence_score"],
            "is_struggling": ml_eval["is_struggling"]
        },
        "interest_graph": interest_data,
        "recommended_playlists": playlists[:4],
        "active_interventions": active_interventions,
        "greeting": f"Good morning, {student['name']} 👋"
    })

@student_bp.route("/api/student/profile", methods=["GET"])
def get_profile():
    student_id = _get_active_student_id()
    student = StudentModel.get_by_id(student_id)
    interests = interest_service.get_student_interest_profile(student_id)
    return jsonify({
        "student": student,
        "interests": interests
    })

@student_bp.route("/api/student/courses", methods=["GET"])
def get_courses():
    student_id = _get_active_student_id()
    courses = CourseModel.get_student_courses(student_id)
    if not courses:
        # Fallback all courses with enrollment status
        courses = CourseModel.get_all()
    return jsonify({"courses": courses})

@student_bp.route("/api/student/interests", methods=["GET"])
def get_interests():
    student_id = _get_active_student_id()
    return jsonify(interest_service.get_student_interest_profile(student_id))

@student_bp.route("/api/student/interest-graph", methods=["GET"])
def get_interest_graph():
    student_id = _get_active_student_id()
    return jsonify(interest_service.get_student_interest_profile(student_id))
