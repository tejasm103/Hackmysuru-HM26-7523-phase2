"""
AdaptiveLearn AI
“One platform. Shared knowledge. Personalized learning. Connected learners.”

Complete Full-Stack Adaptive Learning & Real-Time Intervention Platform
Tech Stack: Flask, MySQL (with zero-config SQLite fallback), scikit-learn, Vanilla JS, HTML5, CSS3, Chart.js
"""

import os
import sys
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from config import Config
from database.db import db
from ml.model import train_or_load_model as load_or_train_model

# Import Blueprints
from routes.auth import auth_bp
from routes.student import student_bp
from routes.courses import courses_bp
from routes.assessment import assessment_bp
from routes.learning import learning_bp
from routes.missions import missions_bp
from routes.videos import videos_bp
from routes.ai import ai_bp
from routes.career import career_bp
from routes.timetable import timetable_bp
from routes.facilitator import facilitator_bp
from routes.community import community_bp
from routes.school import school_bp

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
        static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    )
    
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    # 1. Initialize Database Schema & Seeds (MySQL or automated fallback to SQLite)
    with app.app_context():
        print("[AdaptiveLearn AI] Initializing database and verifying table integrity...")
        try:
            db.init_db()
            print("[AdaptiveLearn AI] Database schema and realistic seed data verified successfully.")
        except Exception as e:
            print(f"[AdaptiveLearn AI] Database init notice: {e}")

        # 2. Initialize or load scikit-learn Decision Tree model
        try:
            load_or_train_model()
            print("[AdaptiveLearn AI] scikit-learn Decision Tree learning-state model active.")
        except Exception as e:
            print(f"[AdaptiveLearn AI] ML model notice: {e}")

    # Context Processor for Templates
    @app.context_processor
    def inject_context():
        return {
            "current_user_id": session.get("user_id"),
            "current_student_id": session.get("student_id") or 1,
            "current_user_name": session.get("name", "Student Learner"),
            "current_user_role": session.get("role", "student"),
            "app_title": "AdaptiveLearn AI"
        }

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(missions_bp)
    app.register_blueprint(videos_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(career_bp)
    app.register_blueprint(timetable_bp)
    app.register_blueprint(facilitator_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(school_bp)

    # =========================================================================
    # FRONTEND PAGE VIEW ROUTES
    # =========================================================================

    @app.route("/")
    def index_view():
        return render_template("index.html")

    @app.route("/login")
    def login_view():
        return render_template("login.html")

    @app.route("/register")
    def register_view():
        return render_template("register.html")

    @app.route("/onboarding")
    def onboarding_view():
        return render_template("onboarding.html")

    @app.route("/dashboard")
    def dashboard_view():
        # Ensure default demo session exists if not logged in
        if "user_id" not in session:
            session["user_id"] = 1
            session["student_id"] = 1
            session["name"] = "Rahul Kumar"
            session["role"] = "student"
        return render_template("dashboard.html")

    @app.route("/learning")
    def learning_view():
        return render_template("learning.html")

    @app.route("/assessment")
    def assessment_view():
        return render_template("assessment.html")

    @app.route("/short-feed")
    def short_feed_view():
        return render_template("short-feed.html")

    @app.route("/missions")
    def missions_view():
        return render_template("missions.html")

    @app.route("/missions/<int:mission_id>")
    def mission_detail_view(mission_id):
        return render_template("mission.html", mission_id=mission_id)

    @app.route("/knowledge-graph")
    def knowledge_graph_view():
        return render_template("knowledge-graph.html")

    @app.route("/learning-gaps")
    def learning_gaps_view():
        return render_template("learning-gaps.html")

    @app.route("/videos")
    def videos_view():
        return render_template("videos.html")

    @app.route("/history")
    def history_view():
        return render_template("history.html")

    @app.route("/career")
    def career_view():
        return render_template("career.html")

    @app.route("/timetable")
    def timetable_view():
        return render_template("timetable.html")

    @app.route("/community")
    def community_view():
        return render_template("community.html")

    @app.route("/study-groups")
    def study_groups_view():
        return render_template("study-groups.html")

    @app.route("/projects")
    def projects_view():
        return render_template("projects.html")

    @app.route("/facilitator")
    def facilitator_view():
        # Ensure facilitator session exists if switching
        if session.get("role") != "facilitator":
            session["user_id"] = 6
            session["name"] = "Dr. Vikram Sharma"
            session["role"] = "facilitator"
        return render_template("facilitator.html")

    @app.route("/chatbot")
    @app.route("/assistant")
    def chatbot_view():
        return render_template("chatbot.html")

    @app.route("/courses")
    @app.route("/courses/<int:course_id>")
    @app.route("/course/<int:course_id>")
    def course_detail_view(course_id=1):
        return render_template("course.html", course_id=course_id)

    # =========================================================================
    # ERROR HANDLERS (Section 37: Never expose SQL, stack traces, or keys)
    # =========================================================================

    @app.errorhandler(404)
    def page_not_found(e):
        if request.path.startswith("/api/"):
            return jsonify({"status": "error", "error": "Endpoint not found."}), 404
        return render_template("dashboard.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        print(f"[Server Error 500]: {e}", file=sys.stderr)
        if request.path.startswith("/api/"):
            return jsonify({
                "status": "error",
                "error": "A safe internal server error occurred. Please retry your request."
            }), 500
        return render_template("dashboard.html"), 500

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    print("\n" + "="*70)
    print("🚀 AdaptiveLearn AI is running!")
    print(f"👉 Local Web Access: http://127.0.0.1:{port}")
    print("👉 Facilitator Console: http://127.0.0.1:5000/facilitator")
    print("👉 Quick 1-Click Persona Switcher active on navigation bar.")
    print("="*70 + "\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
