"""
AdaptiveLearn AI - Mastery Management Engine
Calculates and updates concept mastery from verified academic demonstrations:
- Assessments
- Interactive Learning Missions
- Practice problem performance

IMPORTANT RULE:
Video completion NEVER equals academic mastery. Video engagement is tracked as an interest signal only.
"""

from database.db import db

MASTERY_THRESHOLD = 70.0

class MasteryEngine:
    def get_or_create_mastery(self, student_id, concept_id):
        """Fetches existing mastery record or initializes one with default locked/learning status."""
        record = db.get_one("""
            SELECT id, student_id, concept_id, mastery_score, status, attempts_count, failed_attempts, last_assessment_score
            FROM student_mastery
            WHERE student_id = %s AND concept_id = %s
        """, (student_id, concept_id))
        
        if record:
            return record
            
        # Check if prerequisites are satisfied to set initial status
        prereqs = db.query("""
            SELECT prerequisite_id, min_mastery_required
            FROM concept_prerequisites
            WHERE concept_id = %s
        """, (concept_id,))
        
        is_locked = False
        for p in prereqs:
            p_rec = db.get_one("""
                SELECT mastery_score FROM student_mastery
                WHERE student_id = %s AND concept_id = %s
            """, (student_id, p["prerequisite_id"]))
            score = float(p_rec["mastery_score"]) if p_rec else 0.0
            if score < float(p["min_mastery_required"]):
                is_locked = True
                break
                
        initial_status = "LOCKED" if is_locked else "LEARNING"
        
        db.execute("""
            INSERT INTO student_mastery (student_id, concept_id, mastery_score, status, attempts_count, failed_attempts)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (student_id, concept_id, 0.00, initial_status, 0, 0))
        
        return db.get_one("""
            SELECT id, student_id, concept_id, mastery_score, status, attempts_count, failed_attempts, last_assessment_score
            FROM student_mastery
            WHERE student_id = %s AND concept_id = %s
        """, (student_id, concept_id))

    def update_mastery(self, student_id, concept_id, new_demonstrated_score, source="practice", mistakes_count=0):
        """
        Updates mastery based on demonstrated performance using an Exponential Moving Average / Bayesian update.
        """
        m_rec = self.get_or_create_mastery(student_id, concept_id)
        current_mastery = float(m_rec["mastery_score"] or 0.0)
        attempts = int(m_rec["attempts_count"] or 0) + 1
        failed = int(m_rec["failed_attempts"] or 0)
        
        if new_demonstrated_score < 60.0 or mistakes_count > 2:
            failed += 1
            
        # Weighting based on source
        if source == "assessment":
            weight = 0.50 if current_mastery > 0 else 0.90
        elif source == "mission":
            weight = 0.40
        else: # Practice
            weight = 0.25
            
        calculated_mastery = round((current_mastery * (1.0 - weight)) + (new_demonstrated_score * weight), 2)
        calculated_mastery = max(0.0, min(100.0, calculated_mastery))
        
        # Determine status
        if calculated_mastery >= MASTERY_THRESHOLD:
            new_status = "MASTERED"
        elif calculated_mastery >= 40.0:
            new_status = "NEEDS_PRACTICE"
        elif failed >= 2 or calculated_mastery < 40.0:
            new_status = "STRUGGLING"
        else:
            new_status = "LEARNING"
            
        db.execute("""
            UPDATE student_mastery
            SET mastery_score = %s,
                status = %s,
                attempts_count = %s,
                failed_attempts = %s,
                last_assessment_score = %s,
                last_practiced_at = CURRENT_TIMESTAMP
            WHERE student_id = %s AND concept_id = %s
        """, (calculated_mastery, new_status, attempts, failed, new_demonstrated_score, student_id, concept_id))
        
        # Check downstream unlocks
        unlocked_concepts = self.check_and_unlock_dependents(student_id, concept_id, calculated_mastery)
        
        return {
            "concept_id": concept_id,
            "previous_mastery": current_mastery,
            "new_mastery": calculated_mastery,
            "status": new_status,
            "attempts": attempts,
            "failed_attempts": failed,
            "unlocked_concepts": unlocked_concepts
        }

    def check_and_unlock_dependents(self, student_id, completed_concept_id, new_mastery):
        """
        Unlocks downstream concepts if all prerequisites meet or exceed the threshold (default 70%).
        """
        if new_mastery < MASTERY_THRESHOLD:
            return []
            
        # Find all concepts that require this completed concept as a prerequisite
        dependents = db.query("""
            SELECT cp.concept_id, c.title, c.code, cp.min_mastery_required
            FROM concept_prerequisites cp
            JOIN concepts c ON cp.concept_id = c.id
            WHERE cp.prerequisite_id = %s
        """, (completed_concept_id,))
        
        unlocked = []
        for dep in dependents:
            dep_id = dep["concept_id"]
            
            # Check all prerequisites for this dependent concept
            all_prereqs = db.query("""
                SELECT cp.prerequisite_id, cp.min_mastery_required
                FROM concept_prerequisites cp
                WHERE cp.concept_id = %s
            """, (dep_id,))
            
            all_satisfied = True
            for pr in all_prereqs:
                p_mastery_rec = db.get_one("""
                    SELECT mastery_score FROM student_mastery
                    WHERE student_id = %s AND concept_id = %s
                """, (student_id, pr["prerequisite_id"]))
                p_score = float(p_mastery_rec["mastery_score"]) if p_mastery_rec else 0.0
                if p_score < float(pr["min_mastery_required"]):
                    all_satisfied = False
                    break
                    
            if all_satisfied:
                # If currently LOCKED, promote to LEARNING
                dep_m = self.get_or_create_mastery(student_id, dep_id)
                if dep_m["status"] == "LOCKED":
                    db.execute("""
                        UPDATE student_mastery
                        SET status = 'LEARNING'
                        WHERE student_id = %s AND concept_id = %s
                    """, (student_id, dep_id))
                    unlocked.append({
                        "id": dep_id,
                        "title": dep["title"],
                        "code": dep["code"]
                    })
                    
        return unlocked

mastery_engine = MasteryEngine()
