"""
AdaptiveLearn AI - AI Recommendations Engine
Synthesizes student mastery, video watch trends, and learning missions into actionable suggestions.
"""

from database.db import db

def get_student_recommendations(student_id):
    """Returns curated learning recommendations for dashboard presentation."""
    # Top struggling or learning concepts
    focal = db.query("""
        SELECT c.id, c.title, c.code, sm.mastery_score, sm.status, crs.title as course_title
        FROM student_mastery sm
        JOIN concepts c ON sm.concept_id = c.id
        JOIN courses crs ON c.course_id = crs.id
        WHERE sm.student_id = %s AND sm.status IN ('STRUGGLING', 'NEEDS_PRACTICE', 'LEARNING')
        ORDER BY sm.mastery_score ASC LIMIT 3
    """, (student_id,))
    
    recommendations = []
    for f in focal:
        if f["status"] == "STRUGGLING":
            action = "Remediation & Review"
            badge = "High Priority"
            desc = f"Mastery is at {f['mastery_score']}%. Complete guided practice to rebuild foundations."
        elif f["status"] == "NEEDS_PRACTICE":
            action = "Guided Practice"
            badge = "Recommended"
            desc = f"Mastery is at {f['mastery_score']}%. You are close to the 70% threshold!"
        else:
            action = "Explore Missions"
            badge = "Next Step"
            desc = f"Newly unlocked! Test your skills with an interactive academic mission."

        recommendations.append({
            "concept_id": f["id"],
            "concept_title": f["title"],
            "course_title": f["course_title"],
            "action": action,
            "badge": badge,
            "description": desc,
            "mastery_score": f["mastery_score"]
        })
        
    return recommendations
