"""
AdaptiveLearn AI - Student Model
Manages student demographics, education level, stream, languages, goals, and interests.
"""

from database.db import db

class StudentModel:
    @staticmethod
    def get_by_user_id(user_id):
        return db.get_one("""
            SELECT s.*, u.name, u.email, u.role, sc.name as school_name
            FROM students s
            JOIN users u ON s.user_id = u.id
            LEFT JOIN schools sc ON s.school_id = sc.id
            WHERE s.user_id = %s
        """, (user_id,))

    @staticmethod
    def get_by_id(student_id):
        return db.get_one("""
            SELECT s.*, u.name, u.email, u.role, sc.name as school_name
            FROM students s
            JOIN users u ON s.user_id = u.id
            LEFT JOIN schools sc ON s.school_id = sc.id
            WHERE s.id = %s
        """, (student_id,))

    @staticmethod
    def create_or_update_profile(user_id, study_level, grade="", stream="", preferred_language="English", 
                                 school_id=1, learning_goal="", career_goal="", interests=None):
        existing = db.get_one("SELECT id FROM students WHERE user_id = %s", (user_id,))
        if existing:
            student_id = existing["id"]
            db.execute("""
                UPDATE students
                SET study_level = %s, grade = %s, stream = %s, preferred_language = %s,
                    school_id = %s, learning_goal = %s, career_goal = %s
                WHERE id = %s
            """, (study_level, grade, stream, preferred_language, school_id, learning_goal, career_goal, student_id))
        else:
            student_id = db.execute("""
                INSERT INTO students (user_id, school_id, study_level, grade, stream, preferred_language, learning_goal, career_goal)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, school_id, study_level, grade, stream, preferred_language, learning_goal, career_goal))

        # Update interests if provided
        if interests:
            for interest_name in interests:
                int_rec = db.get_one("SELECT id FROM interests WHERE name = %s", (interest_name,))
                if int_rec:
                    try:
                        db.execute("""
                            INSERT INTO student_interests (student_id, interest_id, affinity_score, source)
                            VALUES (%s, %s, 85.00, 'onboarding')
                        """, (student_id, int_rec["id"]))
                    except Exception:
                        pass
        return student_id
