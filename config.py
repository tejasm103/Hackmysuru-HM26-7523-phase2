import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "adaptivelearn-ai-secret-default-key")
    
    # Database configuration
    DB_TYPE = os.getenv("DB_TYPE", "mysql")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "adaptivelearn_db")
    
    # External API Keys (stored securely on backend)
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Server configuration
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    
    # Mastery Threshold Rule
    DEFAULT_MASTERY_THRESHOLD = 70.0
    
    # Supported Languages
    SUPPORTED_LANGUAGES = [
        {"code": "en", "name": "English"},
        {"code": "kn", "name": "Kannada"},
        {"code": "hi", "name": "Hindi"},
        {"code": "te", "name": "Telugu"},
        {"code": "ta", "name": "Tamil"},
        {"code": "ml", "name": "Malayalam"},
    ]
    
    # Supported Study Levels
    STUDY_LEVELS = [
        "Grade 10",
        "PUC",
        "Diploma",
        "ITI",
        "Professional Course"
    ]
    
    # Streams
    STREAMS = [
        "Science",
        "Commerce",
        "Computer Science",
        "Electronics",
        "Mechanical",
        "Civil",
        "Mathematics",
        "Biology",
        "Programming"
    ]
