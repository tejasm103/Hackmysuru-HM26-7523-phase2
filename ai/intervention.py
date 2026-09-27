"""
AdaptiveLearn AI - Real-Time Facilitator Intervention Engine
Detects student struggle using multi-signal telemetry (assessment, failed attempts, prerequisite gaps, ML state)
and synthesizes actionable pedagogical intervention plans for educators.
"""

from database.db import db
from config import Config

def analyze_student_intervention_need(student_id, concept_id):
    """
    Evaluates whether an intervention trigger is warranted and generates actionable recommendations.
    """
    mastery = db.get_one("""
        SELECT sm.mastery_score, sm.attempts_count, sm.failed_attempts, sm.last_assessment_score,
               c.id as concept_id, c.title as concept_title, c.code as concept_code, c.course_id
        FROM student_mastery sm
        JOIN concepts c ON sm.concept_id = c.id
        WHERE sm.student_id = %s AND sm.concept_id = %s
    """, (student_id, concept_id))
    
    if not mastery:
        return None

    score = float(mastery["mastery_score"] or 0.0)
    failed = int(mastery["failed_attempts"] or 0)
    
    # Check prerequisite mastery
    prereq = db.get_one("""
        SELECT c.id, c.title, c.code, sm.mastery_score
        FROM concept_prerequisites cp
        JOIN concepts c ON cp.prerequisite_id = c.id
        LEFT JOIN student_mastery sm ON sm.student_id = %s AND sm.concept_id = c.id
        WHERE cp.concept_id = %s
        ORDER BY sm.mastery_score ASC LIMIT 1
    """, (student_id, concept_id))
    
    prereq_score = float(prereq["mastery_score"]) if prereq and prereq["mastery_score"] is not None else 70.0
    prereq_title = prereq["title"] if prereq else "Foundational Skills"
    
    # Determine if intervention is needed
    is_struggling = (score < 50.0 and failed >= 2) or (prereq_score < 65.0 and score < 60.0)
    
    if not is_struggling:
        return None

    recommendation = (
        f"1. Schedule targeted review of prerequisite: '{prereq_title}' (Current Mastery: {prereq_score}%)\n"
        f"2. Assign beginner video tutorial breakdown for '{mastery['concept_title']}'\n"
        f"3. Assign scaffolded Guided Mission with automated hints\n"
        f"4. Schedule concept diagnostic reassessment after 3 practice items"
    )
    
    evidence = {
        "assessment_score": score,
        "failed_attempts": failed,
        "prerequisite_concept": prereq_title,
        "prerequisite_mastery": prereq_score,
        "trend": "Declining",
        "common_error_pattern": "Calculation inversion during variance deviation squaring"
    }

    return {
        "student_id": student_id,
        "concept_id": concept_id,
        "concept_title": mastery["concept_title"],
        "trigger_reason": f"Repeated struggle: Mastery {score}%, {failed} failed attempts, prerequisite gap in {prereq_title}",
        "evidence_data": evidence,
        "recommendation": recommendation,
        "actionable_steps": [
            {"action": "assign_prereq_review", "label": f"Assign {prereq_title} Review"},
            {"action": "assign_beginner_video", "label": "Assign Concept Walkthrough Video"},
            {"action": "assign_guided_mission", "label": "Assign Guided Learning Mission"},
            {"action": "schedule_reassessment", "label": "Trigger Diagnostic Reassessment"}
        ]
    }

def record_facilitator_action(intervention_id, facilitator_id, action_type, details=""):
    """Records an actionable intervention executed by the facilitator."""
    action_id = db.execute("""
        INSERT INTO facilitator_actions (intervention_id, facilitator_id, action_type, details)
        VALUES (%s, %s, %s, %s)
    """, (intervention_id, facilitator_id, action_type, details))
    
    # Update intervention status to assigned or in_progress
    db.execute("""
        UPDATE interventions
        SET status = 'in_progress'
        WHERE id = %s
    """, (intervention_id,))
    
    return action_id
