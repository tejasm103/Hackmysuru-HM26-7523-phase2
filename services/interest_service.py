"""
AdaptiveLearn AI - Interest Analysis & Interest Graph Service
Maintains the "Learning Interest Profile" (explicitly NOT a psychological diagnosis).
Fuses multiple engagement signals:
- Video watch duration & completion
- Replay counts
- Topic & subject frequency
- Saved videos
- Mission selections
- Initial student-selected interests
"""

from database.db import db

class InterestService:
    def get_student_interest_profile(self, student_id):
        """
        Retrieves the normalized Learning Interest Profile for a student across all tracked domains.
        """
        records = db.query("""
            SELECT i.id, i.name, i.category, i.icon, si.affinity_score, si.source
            FROM student_interests si
            JOIN interests i ON si.interest_id = i.id
            WHERE si.student_id = %s
            ORDER BY si.affinity_score DESC
        """, (student_id,))
        
        # If student has no records yet, populate default baseline interests
        if not records:
            all_interests = db.query("SELECT id, name, category, icon FROM interests")
            for idx, item in enumerate(all_interests):
                score = 80.0 if idx == 0 else 50.0
                try:
                    db.execute("""
                        INSERT INTO student_interests (student_id, interest_id, affinity_score, source)
                        VALUES (%s, %s, %s, 'onboarding')
                    """, (student_id, item["id"], score))
                except Exception:
                    pass
            records = db.query("""
                SELECT i.id, i.name, i.category, i.icon, si.affinity_score, si.source
                FROM student_interests si
                JOIN interests i ON si.interest_id = i.id
                WHERE si.student_id = %s
                ORDER BY si.affinity_score DESC
            """, (student_id,))

        labels = [r["name"] for r in records]
        scores = [float(r["affinity_score"]) for r in records]
        
        return {
            "title": "Learning Interest Profile",
            "disclaimer": "This profile reflects current platform learning engagement and is not a psychological diagnosis.",
            "interests": records,
            "chart_data": {
                "labels": labels,
                "scores": scores
            }
        }

    def record_video_engagement(self, student_id, video_id, action_type="watch", watched_seconds=0, is_completed=False, replay_count=0):
        """
        Captures real-time video interaction and boosts affinity in the student's Learning Interest Profile.
        CRITICAL: Video engagement is an INTEREST signal, NEVER academic mastery.
        """
        # 1. Update student_video_progress
        existing_prog = db.get_one("""
            SELECT id, watched_seconds, is_completed, replay_count 
            FROM student_video_progress
            WHERE student_id = %s AND video_id = %s
        """, (student_id, video_id))
        
        if existing_prog:
            total_sec = existing_prog["watched_seconds"] + watched_seconds
            total_replays = existing_prog["replay_count"] + replay_count
            completed = 1 if is_completed or existing_prog["is_completed"] else 0
            db.execute("""
                UPDATE student_video_progress
                SET watched_seconds = %s,
                    is_completed = %s,
                    replay_count = %s,
                    last_position_seconds = %s
                WHERE id = %s
            """, (total_sec, completed, total_replays, watched_seconds, existing_prog["id"]))
        else:
            db.execute("""
                INSERT INTO student_video_progress (student_id, video_id, watched_seconds, is_completed, replay_count)
                VALUES (%s, %s, %s, %s, %s)
            """, (student_id, video_id, watched_seconds, 1 if is_completed else 0, replay_count))

        # 2. Append to chronological video_view_history
        db.execute("""
            INSERT INTO video_view_history (student_id, video_id, duration_watched_seconds, completed, action_type)
            VALUES (%s, %s, %s, %s, %s)
        """, (student_id, video_id, watched_seconds, 1 if is_completed else 0, action_type))

        # 3. Adjust interest affinity score for matching topic
        video = db.get_one("SELECT subject, title FROM youtube_videos WHERE id = %s", (video_id,))
        if video:
            subject = video.get("subject", "")
            # Boost score slightly
            boost = 3.5 if is_completed else 1.5
            if replay_count > 0:
                boost += 2.0
                
            db.execute("""
                UPDATE student_interests
                SET affinity_score = MIN(99.0, affinity_score + %s)
                WHERE student_id = %s AND interest_id IN (
                    SELECT id FROM interests WHERE name LIKE %s OR category LIKE %s
                )
            """, (boost, student_id, f"%{subject}%", f"%{subject}%"))

        return {
            "status": "success",
            "student_id": student_id,
            "video_id": video_id,
            "action_type": action_type,
            "message": "Engagement captured. Learning Interest Profile updated."
        }

interest_service = InterestService()
