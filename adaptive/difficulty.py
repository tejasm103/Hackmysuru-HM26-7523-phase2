"""
AdaptiveLearn AI - Adaptive Difficulty Engine
Controls dynamic difficulty scaling (EASY, MEDIUM, HARD) and manages the Remediation Ladder:
Prerequisite Review -> Guided Example -> Easy Practice -> Medium Practice -> Reassessment
"""

from database.db import db

class DifficultyEngine:
    DIFFICULTIES = ["EASY", "MEDIUM", "HARD"]

    def determine_difficulty(self, student_id, concept_id):
        """
        Determines the appropriate difficulty level for the next activity.
        Inputs: mastery score, recent attempt accuracy, failed attempts count.
        """
        mastery_rec = db.get_one("""
            SELECT mastery_score, attempts_count, failed_attempts, status
            FROM student_mastery
            WHERE student_id = %s AND concept_id = %s
        """, (student_id, concept_id))
        
        if not mastery_rec:
            return "EASY"
            
        score = float(mastery_rec["mastery_score"] or 0.0)
        failed = int(mastery_rec["failed_attempts"] or 0)
        
        # Scaling rules
        if score >= 85.0 and failed == 0:
            return "HARD"
        elif score >= 70.0 and failed <= 1:
            return "MEDIUM"
        elif score >= 40.0:
            return "MEDIUM" if failed <= 1 else "EASY"
        else:
            return "EASY"

    def get_remediation_ladder(self, student_id, concept_id):
        """
        Generates the 5-step structured pedagogical recovery pathway when repeated struggle is detected.
        """
        concept = db.get_one("SELECT id, title, code, course_id FROM concepts WHERE id = %s", (concept_id,))
        if not concept:
            return []

        # Find prerequisite if any
        prereq = db.get_one("""
            SELECT c.id, c.title, c.code, sm.mastery_score
            FROM concept_prerequisites cp
            JOIN concepts c ON cp.prerequisite_id = c.id
            LEFT JOIN student_mastery sm ON sm.student_id = %s AND sm.concept_id = c.id
            WHERE cp.concept_id = %s
            ORDER BY sm.mastery_score ASC
            LIMIT 1
        """, (student_id, concept_id))

        prereq_title = prereq["title"] if prereq else "Foundational Expressions"
        prereq_id = prereq["id"] if prereq else concept_id

        return [
            {
                "step": 1,
                "type": "prerequisite_review",
                "title": f"Step 1: Review Prerequisite: {prereq_title}",
                "description": f"Solidify missing foundational concepts from {prereq_title} before advancing.",
                "concept_id": prereq_id,
                "action": "Review Prerequisite"
            },
            {
                "step": 2,
                "type": "video_explanation",
                "title": f"Step 2: Watch Concept Walkthrough: {concept['title']}",
                "description": "Engage with short intuitive visual explanation to build mental models.",
                "concept_id": concept_id,
                "action": "Watch Video"
            },
            {
                "step": 3,
                "type": "guided_mission",
                "title": f"Step 3: Complete Guided Learning Mission",
                "description": "Apply core principles in an interactive learn-by-doing scenario with hints.",
                "concept_id": concept_id,
                "action": "Launch Mission"
            },
            {
                "step": 4,
                "type": "easy_practice",
                "title": f"Step 4: Solve Scaffolded Practice Problems",
                "description": "Reinforce procedural confidence with 3 easy questions.",
                "concept_id": concept_id,
                "action": "Start Practice"
            },
            {
                "step": 5,
                "type": "reassessment",
                "title": f"Step 5: Concept Diagnostic Reassessment",
                "description": "Demonstrate mastery to cross the 70% threshold and unlock next steps.",
                "concept_id": concept_id,
                "action": "Take Assessment"
            }
        ]

difficulty_engine = DifficultyEngine()
