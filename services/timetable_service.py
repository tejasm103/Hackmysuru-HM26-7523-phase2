"""
AdaptiveLearn AI - Adaptive Timetable Service ("My Adaptive Day")
Dynamically generates and balances daily learning schedules with necessary rest, breaks, and personal time.
Adapts learning slots based on weak concepts, unfinished missions, and available study hours.
"""

from database.db import db

class TimetableService:
    def get_student_timetable(self, student_id):
        """
        Retrieves current adaptive day schedule or generates one tailored to the student's learning gaps.
        """
        timetable = db.get_one("""
            SELECT id, student_id, day_name, available_hours
            FROM timetables
            WHERE student_id = %s
            ORDER BY id DESC LIMIT 1
        """, (student_id,))
        
        if not timetable:
            # Generate default adaptive schedule
            tt_id = self.generate_adaptive_timetable(student_id, available_hours=4.0)
            timetable = db.get_one("SELECT * FROM timetables WHERE id = %s", (tt_id,))

        sessions = db.query("""
            SELECT ts.id, ts.start_time, ts.activity_name, ts.activity_type, ts.duration_minutes, 
                   ts.concept_id, ts.is_adaptive, c.title as concept_title
            FROM timetable_sessions ts
            LEFT JOIN concepts c ON ts.concept_id = c.id
            WHERE ts.timetable_id = %s
            ORDER BY ts.start_time ASC
        """, (timetable["id"],))

        return {
            "timetable_id": timetable["id"],
            "day_name": timetable["day_name"],
            "available_hours": float(timetable["available_hours"]),
            "sessions": sessions
        }

    def generate_adaptive_timetable(self, student_id, available_hours=4.0):
        """
        Generates a balanced schedule integrating weak concepts, missions, and mindful breaks.
        """
        # Find weakest concept
        weak_concept = db.get_one("""
            SELECT c.id, c.title, sm.mastery_score
            FROM student_mastery sm
            JOIN concepts c ON sm.concept_id = c.id
            WHERE sm.student_id = %s AND sm.status IN ('STRUGGLING', 'NEEDS_PRACTICE')
            ORDER BY sm.mastery_score ASC LIMIT 1
        """, (student_id,))
        
        weak_id = weak_concept["id"] if weak_concept else 4
        weak_title = weak_concept["title"] if weak_concept else "Statistics Foundations"

        # Create or update timetable record
        tt_id = db.execute("""
            INSERT INTO timetables (student_id, day_name, available_hours)
            VALUES (%s, 'Today', %s)
        """, (student_id, available_hours))

        # Clear existing sessions for this student if any
        db.execute("DELETE FROM timetable_sessions WHERE timetable_id = %s", (tt_id,))

        # Core Balanced Day Blueprint:
        blueprint = [
            ("09:00", "Regular School / Academic Session", "school", 210, None, False),
            ("12:30", "Nutritious Lunch & Rest Break", "lunch", 45, None, False),
            ("16:30", f"Interactive Mission: {weak_title}", "mission", 25, weak_id, True),
            ("17:00", "Mindfulness Break & Hydration", "break", 30, None, False),
            ("17:30", "Video Learning & Concept Walkthrough", "learning", 20, weak_id, True),
            ("18:00", "Sports & Personal Free Time", "free_time", 60, None, False),
            ("19:00", f"Targeted Practice: {weak_title}", "practice", 25, weak_id, True),
            ("19:30", "Family Dinner & Relaxation", "dinner", 60, None, False),
            ("20:30", "Active Prerequisite Revision", "revision", 20, None, True),
            ("21:00", "Wind-Down & Personal Interests", "personal", 45, None, False),
        ]

        for start, name, act_type, duration, cid, is_adapt in blueprint:
            db.execute("""
                INSERT INTO timetable_sessions (timetable_id, start_time, activity_name, activity_type, duration_minutes, concept_id, is_adaptive)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (tt_id, start, name, act_type, duration, cid, 1 if is_adapt else 0))

        return tt_id

timetable_service = TimetableService()
