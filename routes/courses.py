"""
AdaptiveLearn AI - Courses & Knowledge Graph Routes
"""

from flask import Blueprint, request, jsonify, session
from models.course import CourseModel, ConceptModel
from adaptive.knowledge_graph import knowledge_graph_engine
from adaptive.difficulty import difficulty_engine
from database.db import db

courses_bp = Blueprint("courses", __name__)

def _get_active_student_id():
    return session.get("student_id") or 1

@courses_bp.route("/api/courses", methods=["GET"])
def list_courses():
    courses = CourseModel.get_all()
    return jsonify({"courses": courses})

@courses_bp.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    course = CourseModel.get_by_id(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    concepts = ConceptModel.get_by_course(course_id)
    return jsonify({"course": course, "concepts": concepts})

@courses_bp.route("/api/concepts/graph", methods=["GET"])
def get_knowledge_graph():
    """
    Returns visual DAG for a course with node statuses:
    GREEN (Mastered >=70%), BLUE (Learning), YELLOW (Needs Practice), RED (Struggling), LOCK (Locked)
    """
    course_id = request.args.get("course_id", type=int) or 1
    student_id = _get_active_student_id()
    graph_data = knowledge_graph_engine.get_course_graph(course_id, student_id)
    return jsonify(graph_data)

@courses_bp.route("/api/mastery", methods=["GET"])
def get_mastery_overview():
    """
    Returns student concept mastery list and "Where am I stuck?" diagnostic breakdown.
    """
    student_id = _get_active_student_id()
    course_id = request.args.get("course_id", type=int) or 1
    
    # Query all concepts with mastery
    records = db.query("""
        SELECT c.id, c.code, c.title, c.sequence_order, c.difficulty_level, c.category,
               COALESCE(sm.mastery_score, 0.0) as mastery_score,
               COALESCE(sm.status, 'LOCKED') as status,
               COALESCE(sm.attempts_count, 0) as attempts_count,
               COALESCE(sm.failed_attempts, 0) as failed_attempts,
               sm.last_assessment_score, sm.last_practiced_at
        FROM concepts c
        LEFT JOIN student_mastery sm ON sm.concept_id = c.id AND sm.student_id = %s
        WHERE c.course_id = %s
        ORDER BY c.sequence_order ASC
    """, (student_id, course_id))

    # Identify stuck / struggling concepts
    stuck_concepts = []
    for r in records:
        if r["status"] in ("STRUGGLING", "NEEDS_PRACTICE") or (r["failed_attempts"] >= 2 and r["mastery_score"] < 70.0):
            # Generate recommended recovery path
            recovery_path = difficulty_engine.get_remediation_ladder(student_id, r["id"])
            stuck_concepts.append({
                "concept": r,
                "why_stuck": {
                    "assessment_score": r["last_assessment_score"] or r["mastery_score"],
                    "failed_attempts": r["failed_attempts"],
                    "mastery_score": r["mastery_score"],
                    "trend": "Declining" if r["failed_attempts"] >= 2 else "Needs Practice",
                    "common_error_pattern": "Procedural calculation error during variance deviation calculation"
                },
                "recovery_path": recovery_path
            })

    return jsonify({
        "student_id": student_id,
        "course_id": course_id,
        "concepts": records,
        "stuck_concepts": stuck_concepts
    })
