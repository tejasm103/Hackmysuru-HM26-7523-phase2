"""
AdaptiveLearn AI - Learning Mission Service
Executes interactive academic missions where students learn by doing.
Enforces Section 15: Automatic Mission Completion (NO manual mark-complete button).
Validates each step, handles mistakes, and automatically awards mastery upon successful verification.
"""

from database.db import db
from adaptive.mastery import mastery_engine

class MissionService:
    def get_mission_details(self, mission_id, student_id=None):
        """Fetches full mission narrative, scenario, and ordered interactive steps."""
        mission = db.get_one("""
            SELECT lm.*, c.title as concept_title, c.code as concept_code
            FROM learning_missions lm
            JOIN concepts c ON lm.concept_id = c.id
            WHERE lm.id = %s OR lm.code = %s
        """, (mission_id, mission_id))
        
        if not mission:
            return None

        steps = db.query("""
            SELECT id, step_number, instruction, hint, prerequisite_ref, action_type, expected_value, tolerance
            FROM mission_steps
            WHERE mission_id = %s
            ORDER BY step_number ASC
        """, (mission["id"],))

        # Check existing attempt for this student
        attempt = None
        if student_id:
            attempt = db.get_one("""
                SELECT * FROM mission_attempts
                WHERE student_id = %s AND mission_id = %s
                ORDER BY id DESC LIMIT 1
            """, (student_id, mission["id"]))
            
            if not attempt:
                # Initialize new mission attempt
                attempt_id = db.execute("""
                    INSERT INTO mission_attempts (student_id, mission_id, current_step, attempts_count, mistakes_count, is_completed)
                    VALUES (%s, %s, 1, 1, 0, 0)
                """, (student_id, mission["id"]))
                attempt = db.get_one("SELECT * FROM mission_attempts WHERE id = %s", (attempt_id,))

        return {
            "mission": mission,
            "steps": steps,
            "active_attempt": attempt
        }

    def validate_mission_step(self, student_id, mission_id, step_number, submitted_value, time_spent_seconds=30):
        """
        Validates student action on a specific mission step.
        If correct: advances step.
        If incorrect: provides contextual hint and logs mistake.
        If final step correct: AUTOMATICALLY completes mission and updates mastery.
        """
        # Fetch step details
        step = db.get_one("""
            SELECT * FROM mission_steps
            WHERE mission_id = %s AND step_number = %s
        """, (mission_id, step_number))
        
        if not step:
            return {"status": "error", "message": "Mission step not found."}

        # Fetch or create attempt
        attempt = db.get_one("""
            SELECT * FROM mission_attempts
            WHERE student_id = %s AND mission_id = %s
            ORDER BY id DESC LIMIT 1
        """, (student_id, mission_id))
        
        if not attempt:
            att_id = db.execute("""
                INSERT INTO mission_attempts (student_id, mission_id, current_step, attempts_count, mistakes_count, is_completed)
                VALUES (%s, %s, 1, 1, 0, 0)
            """, (student_id, mission_id))
            attempt = db.get_one("SELECT * FROM mission_attempts WHERE id = %s", (att_id,))

        expected_val_str = str(step["expected_value"]).strip()
        tolerance = float(step.get("tolerance") or 0.0)

        # Numerical comparison if both can be floats
        is_correct = False
        try:
            sub_float = float(submitted_value)
            exp_float = float(expected_val_str)
            if abs(sub_float - exp_float) <= tolerance:
                is_correct = True
        except ValueError:
            # String comparison
            if str(submitted_value).strip().lower() == expected_val_str.lower():
                is_correct = True

        mistakes = attempt["mistakes_count"]
        
        if not is_correct:
            # Increment mistakes
            mistakes += 1
            db.execute("""
                UPDATE mission_attempts
                SET mistakes_count = %s,
                    time_spent_seconds = time_spent_seconds + %s
                WHERE id = %s
            """, (mistakes, time_spent_seconds, attempt["id"]))

            return {
                "is_correct": False,
                "step_number": step_number,
                "message": "Values out of required operational tolerance. Adjust your calculations and retry.",
                "hint": step["hint"],
                "prerequisite_ref": step["prerequisite_ref"],
                "mistakes_count": mistakes
            }

        # Step is CORRECT!
        # Check if this was the final step of the mission
        mission = db.get_one("SELECT concept_id, required_steps_count, xp_reward FROM learning_missions WHERE id = %s", (mission_id,))
        total_steps = int(mission["required_steps_count"])

        if step_number >= total_steps:
            # AUTOMATIC COMPLETION
            # Compute mastery impact: 85% base - penalty per mistake
            demonstrated_score = max(50.0, 95.0 - (mistakes * 8.0))
            
            db.execute("""
                UPDATE mission_attempts
                SET current_step = %s,
                    is_completed = 1,
                    completed_at = CURRENT_TIMESTAMP,
                    time_spent_seconds = time_spent_seconds + %s,
                    mastery_impact = %s
                WHERE id = %s
            """, (total_steps, time_spent_seconds, demonstrated_score, attempt["id"]))

            # Update student mastery in DB and evaluate downstream unlocks
            mastery_update = mastery_engine.update_mastery(
                student_id=student_id,
                concept_id=mission["concept_id"],
                new_demonstrated_score=demonstrated_score,
                source="mission",
                mistakes_count=mistakes
            )

            return {
                "is_correct": True,
                "is_completed": True,
                "message": f"🎉 Mission Successfully Completed! All operational parameters verified.",
                "demonstrated_score": demonstrated_score,
                "xp_awarded": mission["xp_reward"],
                "mastery_update": mastery_update,
                "unlocked_concepts": mastery_update.get("unlocked_concepts", [])
            }
        else:
            # Advance to next step
            next_step = step_number + 1
            db.execute("""
                UPDATE mission_attempts
                SET current_step = %s,
                    time_spent_seconds = time_spent_seconds + %s
                WHERE id = %s
            """, (next_step, time_spent_seconds, attempt["id"]))

            return {
                "is_correct": True,
                "is_completed": False,
                "next_step": next_step,
                "message": f"Step {step_number} verified! Advancing to Step {next_step}."
            }

mission_service = MissionService()
