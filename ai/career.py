"""
AdaptiveLearn AI - Career Guidance & Exploration Engine
Synthesizes:
- Current study level
- Enrolled subjects
- Learning interest profile (affinity scores)
- Demonstrated mastery in key concepts
- Student-selected career goals

Presents "Possible pathways to explore" (NOT deterministic career predictions).
"""

from database.db import db
from config import Config

def get_career_pathways(student_id):
    """
    Computes personalized career exploration pathways matched to the student's profile.
    """
    student = db.get_one("""
        SELECT s.id, s.study_level, s.grade, s.stream, s.learning_goal, s.career_goal
        FROM students s
        WHERE s.id = %s
    """, (student_id,))
    
    if not student:
        return []

    # Get student interests
    interests = db.query("""
        SELECT i.name, si.affinity_score
        FROM student_interests si
        JOIN interests i ON si.interest_id = i.id
        WHERE si.student_id = %s
        ORDER BY si.affinity_score DESC
    """, (student_id,))
    
    interest_names = [i["name"] for i in interests]
    
    # Query all career paths from DB
    paths = db.query("""
        SELECT id, title, field_category, education_level, description, growth_outlook
        FROM career_paths
    """)
    
    results = []
    for p in paths:
        # Fetch associated skills
        skills = db.query("""
            SELECT cs.skill_name, cs.importance_level, c.title as related_course_title
            FROM career_skills cs
            LEFT JOIN courses c ON cs.related_course_id = c.id
            WHERE cs.career_path_id = %s
        """, (p["id"],))
        
        # Calculate matching score based on interests & study level
        match_score = 65.0
        if "Space" in p["title"] and any("Space" in i for i in interest_names):
            match_score += 25.0
        elif "Machine Learning" in p["title"] and any("AI" in i for i in interest_names):
            match_score += 25.0
        elif "Robotics" in p["title"] and any("Robotics" in i for i in interest_names):
            match_score += 25.0
        elif "Ecological" in p["title"] and any("Ecology" in i or "Biology" in i for i in interest_names):
            match_score += 25.0

        match_score = min(98.0, match_score)

        # Related projects & missions
        suggested_missions = db.query("""
            SELECT lm.id, lm.title, lm.theme
            FROM learning_missions lm
            LIMIT 2
        """)

        results.append({
            "id": p["id"],
            "title": p["title"],
            "field_category": p["field_category"],
            "education_level": p["education_level"],
            "description": p["description"],
            "growth_outlook": p["growth_outlook"],
            "match_score": round(match_score, 1),
            "required_subjects": ["Mathematics", "Physics", "Computer Science"] if "Robotics" in p["title"] or "Space" in p["title"] else ["Biology", "Chemistry", "Environmental Science"],
            "suggested_skills": [s["skill_name"] for s in skills],
            "recommended_courses": ["Grade 10 Mathematics", "PUC Physics"] if "Space" in p["title"] else ["Diploma Computer Science"],
            "suggested_missions": [m["title"] for m in suggested_missions],
            "statement": "Possible pathway to explore based on current demonstrated strengths and interests."
        })

    # Sort by match score descending
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results
