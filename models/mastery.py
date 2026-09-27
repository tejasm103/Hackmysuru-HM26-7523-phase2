"""
AdaptiveLearn AI - Mastery and Assessment Models
"""

from database.db import db

class MasteryModel:
    @staticmethod
    def get_student_mastery_by_course(student_id, course_id):
        return db.query("""
            SELECT sm.*, c.title as concept_title, c.code as concept_code, c.sequence_order, c.difficulty_level
            FROM student_mastery sm
            JOIN concepts c ON sm.concept_id = c.id
            WHERE sm.student_id = %s AND c.course_id = %s
            ORDER BY c.sequence_order ASC
        """, (student_id, course_id))

    @staticmethod
    def get_overall_mastery_percentage(student_id):
        result = db.get_one("""
            SELECT AVG(mastery_score) as avg_mastery, COUNT(*) as total_tracked
            FROM student_mastery
            WHERE student_id = %s
        """, (student_id,))
        if result and result["avg_mastery"] is not None:
            return round(float(result["avg_mastery"]), 1)
        return 0.0

class AssessmentModel:
    @staticmethod
    def get_questions_for_concept(concept_id, limit=5):
        return db.query("""
            SELECT id, concept_id, difficulty, question_text, question_type, 
                   option_a, option_b, option_c, option_d, correct_answer, explanation, retheme_theme
            FROM questions
            WHERE concept_id = %s
            ORDER BY id ASC LIMIT %s
        """, (concept_id, limit))

    @staticmethod
    def record_attempt(student_id, question_id, student_answer, is_correct, time_taken_seconds=0):
        return db.execute("""
            INSERT INTO question_attempts (student_id, question_id, student_answer, is_correct, time_taken_seconds)
            VALUES (%s, %s, %s, %s, %s)
        """, (student_id, question_id, student_answer, 1 if is_correct else 0, time_taken_seconds))
