"""
AdaptiveLearn AI - AI Tutor Chatbot ("Adaptive Learning Assistant")
Pedagogical assistant that understands student mastery, locked concepts, missions, and career goals.
Follows scaffolding structure: Hint -> Explanation -> Example -> Practice.
Never simply hands out direct answers without educational reasoning.
"""

from database.db import db
from config import Config

TUTOR_SYSTEM_PROMPT = """You are the Adaptive Learning Assistant for AdaptiveLearn AI.
Your role is to guide students using the pedagogical scaffolding loop:
1. Hint (guide their thinking)
2. Explanation (clear conceptual breakdown)
3. Example (analogous working illustration)
4. Practice (scaffolded check for understanding)

CRITICAL RULES:
- Never just hand out direct answers to assessments or missions.
- If a concept is locked (e.g. Probability for Rahul because Statistics is below 70%), explain clearly why it is locked and outline the exact recovery steps.
- Speak encouragingly, with precision, using the student's personal interests (e.g., Space, Robotics) where appropriate.
"""

def generate_tutor_response(student_id, user_message, concept_id=None):
    """
    Synthesizes student profile, mastery, locked concepts, and active mission
    to generate personalized pedagogical tutoring.
    """
    # 1. Fetch student contextual state
    student = db.get_one("""
        SELECT s.id, u.name, s.study_level, s.preferred_language, s.learning_goal, s.career_goal
        FROM students s
        JOIN users u ON s.user_id = u.id
        WHERE s.id = %s
    """, (student_id,))
    
    student_name = student["name"] if student else "Student"
    
    # 2. Fetch mastery records and locked concepts
    mastery_records = db.query("""
        SELECT c.id, c.code, c.title, sm.mastery_score, sm.status, sm.failed_attempts
        FROM student_mastery sm
        JOIN concepts c ON sm.concept_id = c.id
        WHERE sm.student_id = %s
        ORDER BY c.sequence_order ASC
    """, (student_id,))
    
    locked_concepts = [m for m in mastery_records if m["status"] == "LOCKED"]
    struggling_concepts = [m for m in mastery_records if m["status"] == "STRUGGLING"]
    
    # 3. Fetch current active mission if any
    active_mission = db.get_one("""
        SELECT lm.title, lm.scenario_description, lm.theme
        FROM learning_missions lm
        JOIN mission_attempts ma ON ma.mission_id = lm.id
        WHERE ma.student_id = %s AND ma.is_completed = 0
        ORDER BY ma.started_at DESC LIMIT 1
    """, (student_id,))

    # Check for live Gemini API
    if Config.GEMINI_API_KEY:
        try:
            import google.genai as genai
            client = genai.Client(api_key=Config.GEMINI_API_KEY)
            locked_titles = [c['title'] for c in locked_concepts]
            struggling_details = [f"{c['title']} ({c.get('mastery_score', 0)}%)" for c in struggling_concepts]
            context_summary = f"""
Student Name: {student_name}
Study Level: {student.get('study_level')}
Locked Concepts: {locked_titles}
Struggling Concepts: {struggling_details}
Active Mission: {active_mission.get('title') if active_mission else 'None'}
Career Goal: {student.get('career_goal')}
"""
            prompt = f"{context_summary}\n\nStudent Message: {user_message}"
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=dict(system_instruction=TUTOR_SYSTEM_PROMPT)
            )
            reply = response.text.strip()
            
            # Save message to database
            _save_chat_message(student_id, concept_id, user_message, reply)
            return {
                "reply": reply,
                "pedagogical_phase": "explanation",
                "is_ai": True
            }
        except Exception as e:
            print(f"[AI Tutor] API unavailable: {e}")

    # High-Fidelity Pedagogical Heuristics (Demo Mode)
    msg_lower = user_message.lower()
    
    # Question: "Why can't I learn Probability?" or "Why is Probability locked?"
    if "probability" in msg_lower and ("lock" in msg_lower or "why" in msg_lower or "can't" in msg_lower or "cannot" in msg_lower):
        reply = (
            f"Hello {student_name}! 🚀 Probability is currently locked because your Statistics mastery "
            f"is currently at 43%, which is below our 70% prerequisite progression threshold.\n\n"
            f"In probability theory, concepts like sample spaces and expected values depend heavily on "
            f"measures of central tendency and variance from Statistics.\n\n"
            f"Here is your Recommended Recovery Path:\n"
            f"1. 📖 Review Functions & Coordinate Relations (FUNC-03)\n"
            f"2. 🎥 Watch the beginner video: 'Why Do We Square Differences in Variance?'\n"
            f"3. 🛰️ Complete the guided mission: 'Save the Space Station'\n"
            f"4. ✍️ Complete 3 scaffolded practice questions\n"
            f"5. 🎯 Reassess to cross 70% and unlock Probability!"
        )
        phase = "explanation"

    elif "hint" in msg_lower or "help" in msg_lower or "stuck" in msg_lower:
        if active_mission:
            reply = (
                f"💡 Hint for '{active_mission['title']}':\n"
                f"Remember to check your formula carefully. For variance, calculate the deviation of each module "
                f"from the mean, and remember to square that difference! E.g., if deviation is 20 units, 20² = 400. "
                f"Don't simply multiply by 2."
            )
            phase = "hint"
        else:
            reply = (
                f"💡 Concept Hint:\n"
                f"When calculating measures of central dispersion, think of the mean as the balance center. "
                f"Deviations sum to zero unless squared or taken in absolute terms. Try calculating the deviations first!"
            )
            phase = "hint"

    elif "career" in msg_lower or "pathway" in msg_lower:
        reply = (
            f"🌟 Based on your learning interests in Space & Technology and your course progress, "
            f"a strong pathway to explore is Aerospace Systems & Autonomous Guidance. "
            f"By mastering Variance, Probability, and Kinematics, you develop the mathematical and algorithmic "
            f"skills required for trajectory tracking and orbital telemetry!"
        )
        phase = "explanation"

    else:
        reply = (
            f"I am here to guide your learning, {student_name}! 📚\n"
            f"Whether you need a hint on your active mission, want to understand why a concept is locked, "
            f"or want to explore career pathways aligned with your interests, let me know how we can break it down step-by-step!"
        )
        phase = "general"

    # Save to chat_messages table
    _save_chat_message(student_id, concept_id, user_message, reply, phase)
    return {
        "reply": reply,
        "pedagogical_phase": phase,
        "is_ai": False
    }

def _save_chat_message(student_id, concept_id, student_msg, ai_reply, phase="general"):
    try:
        db.execute("""
            INSERT INTO chat_messages (student_id, concept_id, sender, message_text, pedagogical_phase)
            VALUES (%s, %s, 'student', %s, %s)
        """, (student_id, concept_id, student_msg, phase))
        db.execute("""
            INSERT INTO chat_messages (student_id, concept_id, sender, message_text, pedagogical_phase)
            VALUES (%s, %s, 'ai', %s, %s)
        """, (student_id, concept_id, ai_reply, phase))
    except Exception as e:
        print(f"[AI Tutor] Chat message save notice: {e}")
