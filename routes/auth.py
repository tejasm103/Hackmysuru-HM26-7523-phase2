"""
AdaptiveLearn AI - Authentication Routes
Registration, Login, Session Management, and Hackathon 1-Click Demo Switcher.
"""

from flask import Blueprint, request, jsonify, session
from models.user import UserModel
from models.student import StudentModel
from database.db import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    role = data.get("role", "student")

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required."}), 400

    existing = UserModel.get_by_email(email)
    if existing:
        return jsonify({"error": "An account with this email already exists."}), 409

    user_id = UserModel.create_user(name, email, password, role)
    session["user_id"] = user_id
    session["role"] = role
    session["name"] = name

    # If student, create initial student record
    student_id = None
    if role == "student":
        student_id = StudentModel.create_or_update_profile(
            user_id=user_id,
            study_level=data.get("study_level", "Grade 10"),
            grade=data.get("grade", "10th"),
            stream=data.get("stream", "Science & Mathematics"),
            preferred_language=data.get("preferred_language", "English")
        )
        session["student_id"] = student_id

    return jsonify({
        "status": "success",
        "message": "Registration successful.",
        "user": {
            "id": user_id,
            "name": name,
            "email": email,
            "role": role,
            "student_id": student_id
        }
    }), 201

@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = UserModel.get_by_email(email)
    if not user:
        return jsonify({"error": "Invalid email or password."}), 401

    if not UserModel.verify_password(user["password_hash"], password):
        return jsonify({"error": "Invalid email or password."}), 401

    session["user_id"] = user["id"]
    session["role"] = user["role"]
    session["name"] = user["name"]

    student_id = None
    if user["role"] == "student":
        st = StudentModel.get_by_user_id(user["id"])
        student_id = st["id"] if st else None
        session["student_id"] = student_id

    return jsonify({
        "status": "success",
        "message": "Login successful.",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "student_id": student_id
        }
    })

@auth_bp.route("/api/auth/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return jsonify({"status": "success", "message": "Logged out successfully."})

@auth_bp.route("/api/auth/me", methods=["GET"])
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"user": None, "authenticated": False})

    user = UserModel.get_by_id(user_id)
    if not user:
        session.clear()
        return jsonify({"user": None, "authenticated": False})

    student_id = session.get("student_id")
    student_profile = None
    if user["role"] == "student":
        student_profile = StudentModel.get_by_user_id(user_id)
        if student_profile:
            student_id = student_profile["id"]

    return jsonify({
        "authenticated": True,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "student_id": student_id
        },
        "student": student_profile
    })

@auth_bp.route("/api/auth/switch-demo", methods=["POST"])
def switch_demo_user():
    """
    Evaluator Utility: Switches current active session instantly between:
    - Rahul (Student B: Struggling, Stats 43%, ML Needs Support)
    - Priya (Student A: Advanced, Stats 82%, ML Improving)
    - Arjun (Diploma CS, ML Stable)
    - Ananya (PUC Science, ML Improving)
    - Facilitator (Dr. Vikram Sharma)
    """
    data = request.get_json() or {}
    target = data.get("target", "rahul").lower()

    email_map = {
        "rahul": "rahul@adaptivelearn.ai",
        "priya": "priya@adaptivelearn.ai",
        "arjun": "arjun@adaptivelearn.ai",
        "ananya": "ananya@adaptivelearn.ai",
        "kiran": "kiran@adaptivelearn.ai",
        "facilitator": "facilitator@adaptivelearn.ai",
        "admin": "admin@adaptivelearn.ai"
    }

    target_email = email_map.get(target, "rahul@adaptivelearn.ai")
    user = UserModel.get_by_email(target_email)
    if not user:
        return jsonify({"error": f"Demo user '{target}' not found."}), 404

    session["user_id"] = user["id"]
    session["role"] = user["role"]
    session["name"] = user["name"]

    student_id = None
    if user["role"] == "student":
        st = StudentModel.get_by_user_id(user["id"])
        student_id = st["id"] if st else None
        session["student_id"] = student_id

    return jsonify({
        "status": "success",
        "message": f"Switched active session to {user['name']} ({user['role']}).",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "student_id": student_id
        }
    })
