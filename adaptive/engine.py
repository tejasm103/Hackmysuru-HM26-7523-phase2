"""
AdaptiveLearn AI - Central Adaptive Learning Engine
Orchestrates pedagogical adaptation by fusing:
- Continuous academic mastery (student_mastery)
- Assessment and practice history
- Knowledge graph prerequisites (DAG)
- Student interest profiles (student_interests)
- Video engagement signals
- scikit-learn ML Learning State (IMPROVING, STABLE, NEEDS_SUPPORT)
- Facilitator intervention tracking

Outputs deterministic, personalized next steps:
- 85–100% -> Advanced challenge
- 70–84%  -> Normal progression
- 40–69%  -> Guided practice
- 0–39%   -> Remediation + prerequisite review
"""

from database.db import db
from adaptive.knowledge_graph import knowledge_graph_engine
from adaptive.difficulty import difficulty_engine
from ml.predictor import evaluate_student_concept_ml

class AdaptiveEngine:
    def get_next_best_activity(self, student_id, course_id=None):
        """
        Calculates the single next best learning activity for a student.
        Considers all performance signals, ML state, and interest graph.
        """
        # If course_id is not specified, get primary active enrollment
        if not course_id:
            enrollment = db.get_one("""
                SELECT course_id FROM enrollments 
                WHERE student_id = %s AND status = 'active'
                ORDER BY enrolled_at DESC LIMIT 1
            """, (student_id,))
            course_id = enrollment["course_id"] if enrollment else 1

        # Fetch knowledge graph state for this student
        graph_data = knowledge_graph_engine.get_course_graph(course_id, student_id)
        nodes = graph_data["nodes"]
        
        # 1. Identify the focal concept:
        # Priority order:
        # a) Concept with STRUGGLING status (Red, needs immediate intervention)
        # b) Concept with NEEDS_PRACTICE status (Yellow, 40-69%)
        # c) Concept with LEARNING status (Blue, active unlocked next step)
        # d) Next unmastered concept whose prerequisites are satisfied
        
        focal_concept = None
        for n in nodes:
            if n["status"] == "STRUGGLING":
                focal_concept = n
                break
                
        if not focal_concept:
            for n in nodes:
                if n["status"] == "NEEDS_PRACTICE":
                    focal_concept = n
                    break

        if not focal_concept:
            for n in nodes:
                if n["status"] == "LEARNING" and not n["is_locked"]:
                    focal_concept = n
                    break

        # Fallback to the first unlocked non-mastered node, or first node
        if not focal_concept:
            for n in nodes:
                if not n["is_locked"] and n["mastery_score"] < 100.0:
                    focal_concept = n
                    break
        if not focal_concept and nodes:
            focal_concept = nodes[0]

        concept_id = focal_concept["id"]
        mastery_score = float(focal_concept.get("mastery_score", 0.0))
        failed_attempts = int(focal_concept.get("failed_attempts", 0))
        
        # 2. Query Machine Learning Learning State
        ml_result = evaluate_student_concept_ml(student_id, concept_id)
        ml_state = ml_result["predicted_state"] # IMPROVING, STABLE, NEEDS_SUPPORT

        # 3. Query Top Student Interests for Contextual Alignment
        interests = db.query("""
            SELECT i.name, si.affinity_score
            FROM student_interests si
            JOIN interests i ON si.interest_id = i.id
            WHERE si.student_id = %s
            ORDER BY si.affinity_score DESC LIMIT 2
        """, (student_id,))
        top_interest = interests[0]["name"] if interests else "Space & Technology"

        # 4. Query Related Learning Mission
        mission = db.get_one("""
            SELECT id, code, title, scenario_description, difficulty, theme, xp_reward
            FROM learning_missions
            WHERE concept_id = %s LIMIT 1
        """, (concept_id,))

        # 5. Query Relevant Video Resource
        video = db.get_one("""
            SELECT id, video_id, title, channel_name, duration_seconds, thumbnail_url, difficulty
            FROM youtube_videos
            WHERE concept_id = %s LIMIT 1
        """, (concept_id,))

        # 6. Apply Pedagogical Decision Rules:
        # Rule Set 1: 0 - 39% or Repeated Errors -> Remediation + Prerequisite Review
        if mastery_score < 40.0 or (failed_attempts >= 2 and mastery_score < 70.0) or ml_state == "NEEDS_SUPPORT":
            difficulty = "EASY"
            activity_type = "prerequisite_review"
            rule_matched = "0-39% / Repeated Struggle: Remediation & Prerequisite Review"
            remediation_ladder = difficulty_engine.get_remediation_ladder(student_id, concept_id)
            
            recommendation_text = (
                f"Your performance indicates concept gaps in {focal_concept['title']} "
                f"(Mastery: {mastery_score}%, Failed attempts: {failed_attempts}). "
                f"ML State: {ml_state}. We recommend completing the prerequisite recovery ladder."
            )
            practice_quantity = 3
            needs_intervention = True
            
            # Auto-check or record intervention if open
            self._ensure_intervention_recorded(student_id, concept_id, focal_concept, mastery_score, failed_attempts, ml_state)

        # Rule Set 2: 40 - 69% -> Guided Practice
        elif mastery_score < 70.0:
            difficulty = "MEDIUM" if failed_attempts == 0 else "EASY"
            activity_type = "guided_mission" if mission else "practice"
            rule_matched = "40-69%: Guided Practice & Mission Execution"
            remediation_ladder = []
            recommendation_text = (
                f"You are building solid comprehension in {focal_concept['title']} ({mastery_score}%). "
                f"Solve guided interactive tasks to reach the 70% mastery threshold."
            )
            practice_quantity = 4
            needs_intervention = False

        # Rule Set 3: 70 - 84% -> Normal Progression
        elif mastery_score < 85.0:
            difficulty = "MEDIUM"
            activity_type = "mission" if mission else "reassessment"
            rule_matched = "70-84%: Normal Progression & Applied Reinforcement"
            remediation_ladder = []
            recommendation_text = (
                f"Strong demonstrated mastery in {focal_concept['title']} ({mastery_score}%). "
                f"Prerequisites unlocked! Advance through high-level missions and practice."
            )
            practice_quantity = 3
            needs_intervention = False

        # Rule Set 4: 85 - 100% -> Advanced Challenge
        else:
            difficulty = "HARD"
            activity_type = "advanced_challenge"
            rule_matched = "85-100%: Advanced Challenge & Complex Real-World Modeling"
            remediation_ladder = []
            recommendation_text = (
                f"Exceptional mastery demonstrated ({mastery_score}%). "
                f"Tackle advanced competitive scenarios and interdisciplinary projects."
            )
            practice_quantity = 2
            needs_intervention = False

        return {
            "student_id": student_id,
            "course_id": course_id,
            "concept": {
                "id": concept_id,
                "code": focal_concept["code"],
                "title": focal_concept["title"],
                "mastery_score": mastery_score,
                "status": focal_concept["status"],
                "attempts": focal_concept.get("attempts", 0),
                "failed_attempts": failed_attempts
            },
            "activity_type": activity_type,
            "difficulty": difficulty,
            "rule_matched": rule_matched,
            "recommendation_text": recommendation_text,
            "practice_quantity": practice_quantity,
            "needs_intervention": needs_intervention,
            "ml_state": ml_state,
            "top_interest": top_interest,
            "mission": mission,
            "video": video,
            "remediation_ladder": remediation_ladder if mastery_score < 40.0 or ml_state == "NEEDS_SUPPORT" else []
        }

    def _ensure_intervention_recorded(self, student_id, concept_id, concept, score, failed, ml_state):
        """Creates an intervention record if student is struggling and no open intervention exists."""
        existing = db.get_one("""
            SELECT id FROM interventions 
            WHERE student_id = %s AND concept_id = %s AND status = 'open'
        """, (student_id, concept_id))
        
        if not existing:
            trigger_reason = f"Automated Alert: Low mastery ({score}%), {failed} failed attempts, ML State: {ml_state}"
            recommendation = (
                f"1. Review prerequisites for {concept['title']}\n"
                f"2. Assign beginner video tutorial\n"
                f"3. Assign guided mission with hints\n"
                f"4. Reassess upon practice completion"
            )
            evidence = f'{{"mastery_score": {score}, "failed_attempts": {failed}, "ml_state": "{ml_state}"}}'
            try:
                db.execute("""
                    INSERT INTO interventions (student_id, concept_id, trigger_reason, evidence_data, recommendation, status)
                    VALUES (%s, %s, %s, %s, %s, 'open')
                """, (student_id, concept_id, trigger_reason, evidence, recommendation))
            except Exception as e:
                print(f"[AdaptiveEngine] Notice during intervention insert: {e}")

adaptive_engine = AdaptiveEngine()
