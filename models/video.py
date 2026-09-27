"""
AdaptiveLearn AI - Video, Mission, Community, and Intervention Models
"""

from database.db import db

class VideoModel:
    @staticmethod
    def get_view_history(student_id, filter_subject=None):
        sql = """
            SELECT svp.*, yv.title, yv.channel_name, yv.duration_seconds, yv.thumbnail_url, yv.subject,
                   c.title as concept_title, crs.title as course_title
            FROM student_video_progress svp
            JOIN youtube_videos yv ON svp.video_id = yv.id
            LEFT JOIN concepts c ON yv.concept_id = c.id
            LEFT JOIN courses crs ON c.course_id = crs.id
            WHERE svp.student_id = %s
        """
        params = [student_id]
        if filter_subject and filter_subject != "all":
            sql += " AND yv.subject LIKE %s"
            params.append(f"%{filter_subject}%")
            
        sql += " ORDER BY svp.updated_at DESC"
        return db.query(sql, params)

class MissionModel:
    @staticmethod
    def get_all_missions():
        return db.query("""
            SELECT lm.*, c.title as concept_title, c.code as concept_code, crs.title as course_title
            FROM learning_missions lm
            JOIN concepts c ON lm.concept_id = c.id
            JOIN courses crs ON c.course_id = crs.id
            ORDER BY lm.id ASC
        """)

    @staticmethod
    def get_student_mission_status(student_id):
        return db.query("""
            SELECT ma.*, lm.title, lm.code, lm.theme, lm.xp_reward
            FROM mission_attempts ma
            JOIN learning_missions lm ON ma.mission_id = lm.id
            WHERE ma.student_id = %s
        """, (student_id,))

class CommunityModel:
    @staticmethod
    def get_posts(community_id=None, limit=20):
        sql = """
            SELECT cp.*, u.name as author_name, u.role as author_role, c.title as concept_title,
                   (SELECT COUNT(*) FROM community_comments cc WHERE cc.post_id = cp.id) as comment_count,
                   (SELECT COUNT(*) FROM post_reactions pr WHERE pr.post_id = cp.id) as reaction_count
            FROM community_posts cp
            JOIN users u ON cp.user_id = u.id
            LEFT JOIN concepts c ON cp.concept_id = c.id
        """
        params = []
        if community_id:
            sql += " WHERE cp.community_id = %s"
            params.append(community_id)
            
        sql += " ORDER BY cp.is_pinned DESC, cp.created_at DESC LIMIT %s"
        params.append(limit)
        return db.query(sql, params)

    @staticmethod
    def create_post(community_id, user_id, title, content, concept_id=None, post_type="discussion"):
        return db.execute("""
            INSERT INTO community_posts (community_id, user_id, concept_id, title, content, post_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (community_id, user_id, concept_id, title, content, post_type))

class InterventionModel:
    @staticmethod
    def get_all_interventions(status=None):
        sql = """
            SELECT iv.*, u.name as student_name, u.email as student_email, s.study_level, s.grade,
                   c.title as concept_title, crs.title as course_title, crs.code as course_code
            FROM interventions iv
            JOIN students s ON iv.student_id = s.id
            JOIN users u ON s.user_id = u.id
            JOIN concepts c ON iv.concept_id = c.id
            JOIN courses crs ON c.course_id = crs.id
        """
        params = []
        if status:
            sql += " WHERE iv.status = %s"
            params.append(status)
            
        sql += " ORDER BY iv.created_at DESC"
        return db.query(sql, params)
