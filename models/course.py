"""
AdaptiveLearn AI - Course and Concept Models
"""

from database.db import db

class CourseModel:
    @staticmethod
    def get_all():
        return db.query("SELECT * FROM courses ORDER BY id ASC")

    @staticmethod
    def get_by_id(course_id):
        return db.get_one("SELECT * FROM courses WHERE id = %s", (course_id,))

    @staticmethod
    def get_student_courses(student_id):
        return db.query("""
            SELECT c.*, e.status as enrollment_status, e.enrolled_at
            FROM courses c
            JOIN enrollments e ON e.course_id = c.id
            WHERE e.student_id = %s
        """, (student_id,))

    @staticmethod
    def enroll_student(student_id, course_id):
        return db.execute("""
            INSERT INTO enrollments (student_id, course_id, status)
            VALUES (%s, %s, 'active')
        """, (student_id, course_id))

class ConceptModel:
    @staticmethod
    def get_by_course(course_id):
        return db.query("""
            SELECT * FROM concepts
            WHERE course_id = %s
            ORDER BY sequence_order ASC
        """, (course_id,))

    @staticmethod
    def get_by_id(concept_id):
        return db.get_one("""
            SELECT c.*, crs.title as course_title, crs.code as course_code
            FROM concepts c
            JOIN courses crs ON c.course_id = crs.id
            WHERE c.id = %s
        """, (concept_id,))
