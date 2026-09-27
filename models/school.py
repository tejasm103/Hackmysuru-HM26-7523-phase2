"""
AdaptiveLearn AI - School Model
"""

from database.db import db

class SchoolModel:
    @staticmethod
    def get_all():
        return db.query("SELECT * FROM schools ORDER BY name ASC")
