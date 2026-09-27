"""
AdaptiveLearn AI - Community, Study Groups & Projects Routes
"""

from flask import Blueprint, request, jsonify, session
from models.community import CommunityModel
from ai.community import generate_peer_hint
from database.db import db

community_bp = Blueprint("community", __name__)

def _get_active_user_id():
    return session.get("user_id") or 1

@community_bp.route("/api/community", methods=["GET"])
def get_community_overview():
    community_id = request.args.get("community_id", type=int)
    posts = CommunityModel.get_posts(community_id)
    communities = db.query("SELECT * FROM communities ORDER BY id ASC")
    return jsonify({
        "communities": communities,
        "posts": posts
    })

@community_bp.route("/api/community/posts", methods=["POST"])
def create_post():
    user_id = _get_active_user_id()
    data = request.get_json() or {}
    community_id = data.get("community_id", 1)
    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    concept_id = data.get("concept_id")
    post_type = data.get("post_type", "discussion")

    if not title or not content:
        return jsonify({"error": "Title and content are required."}), 400

    post_id = CommunityModel.create_post(community_id, user_id, title, content, concept_id, post_type)
    return jsonify({
        "status": "success",
        "post_id": post_id,
        "message": "Post published to community board."
    }), 201

@community_bp.route("/api/community/posts/<int:post_id>/comments", methods=["GET", "POST"])
def handle_comments(post_id):
    if request.method == "POST":
        user_id = _get_active_user_id()
        data = request.get_json() or {}
        comment_text = data.get("comment_text", "").strip()
        if not comment_text:
            return jsonify({"error": "Comment text cannot be empty."}), 400

        comment_id = db.execute("""
            INSERT INTO community_comments (post_id, user_id, comment_text)
            VALUES (%s, %s, %s)
        """, (post_id, user_id, comment_text))

        return jsonify({
            "status": "success",
            "comment_id": comment_id,
            "message": "Comment posted."
        }), 201
    else:
        comments = db.query("""
            SELECT cc.*, u.name as author_name, u.role as author_role
            FROM community_comments cc
            JOIN users u ON cc.user_id = u.id
            WHERE cc.post_id = %s
            ORDER BY cc.created_at ASC
        """, (post_id,))
        return jsonify({"comments": comments})

@community_bp.route("/api/community/posts/<int:post_id>/reactions", methods=["POST"])
def react_to_post(post_id):
    user_id = _get_active_user_id()
    data = request.get_json() or {}
    reaction_type = data.get("reaction_type", "like") # like, helpful, insightful, celebrate
    
    try:
        db.execute("""
            INSERT INTO post_reactions (post_id, user_id, reaction_type)
            VALUES (%s, %s, %s)
        """, (post_id, user_id, reaction_type))
    except Exception:
        pass # Ignore duplicate reaction

    count = db.get_one("SELECT COUNT(*) as c FROM post_reactions WHERE post_id = %s", (post_id,))["c"]
    return jsonify({"status": "success", "reaction_count": count})

@community_bp.route("/api/community/posts/<int:post_id>/report", methods=["POST"])
def report_post(post_id):
    user_id = _get_active_user_id()
    data = request.get_json() or {}
    reason = data.get("reason", "Inappropriate content").strip()
    
    db.execute("""
        INSERT INTO post_reports (post_id, reporter_id, reason, status)
        VALUES (%s, %s, %s, 'pending')
    """, (post_id, user_id, reason))
    
    return jsonify({"status": "success", "message": "Report submitted for moderator review."})

@community_bp.route("/api/study-groups", methods=["GET"])
def get_study_groups():
    groups = db.query("""
        SELECT sg.*, c.title as concept_title, crs.title as course_title,
               (SELECT COUNT(*) FROM study_group_members sgm WHERE sgm.group_id = sg.id) as current_member_count
        FROM study_groups sg
        JOIN courses crs ON sg.course_id = crs.id
        LEFT JOIN concepts c ON sg.concept_id = c.id
        ORDER BY sg.id ASC
    """)
    return jsonify({"study_groups": groups})

@community_bp.route("/api/projects", methods=["GET"])
def get_projects():
    projects = db.query("""
        SELECT p.*,
               (SELECT COUNT(*) FROM project_members pm WHERE pm.project_id = p.id) as member_count
        FROM projects p
        ORDER BY p.id ASC
    """)
    return jsonify({"projects": projects})

@community_bp.route("/api/challenges", methods=["GET"])
def get_challenges():
    challenges = db.query("SELECT * FROM challenges ORDER BY id ASC")
    return jsonify({"challenges": challenges})
