"""
AdaptiveLearn AI - User Model
Authentication and core user account management.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db

class UserModel:
    @staticmethod
    def get_by_id(user_id):
        return db.get_one("SELECT * FROM users WHERE id = %s", (user_id,))

    @staticmethod
    def get_by_email(email):
        return db.get_one("SELECT * FROM users WHERE LOWER(email) = LOWER(%s)", (email.strip(),))

    @staticmethod
    def create_user(name, email, password, role="student"):
        pwd_hash = generate_password_hash(password)
        user_id = db.execute("""
            INSERT INTO users (name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
        """, (name, email.strip().lower(), pwd_hash, role))
        return user_id

    @staticmethod
    def verify_password(stored_hash, candidate_password):
        # Support demo hash fallback if needed
        if stored_hash.startswith("pbkdf2:sha256:600000$adaptive$"):
            # Our standard demo hash corresponds to 'demo123'
            if candidate_password == "demo123":
                return True
        return check_password_hash(stored_hash, candidate_password)
