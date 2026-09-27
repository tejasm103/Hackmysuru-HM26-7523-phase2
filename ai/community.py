"""
AdaptiveLearn AI - AI Community & Peer Collaboration Assistant
Generates hints, checks question relevance, and supports peer discussions.
"""

from database.db import db
from config import Config

def generate_peer_hint(post_id, user_question):
    """Generates an intuitive, guiding peer hint without solving the problem outright."""
    # Check if Gemini API is available
    if Config.GEMINI_API_KEY:
        try:
            import google.genai as genai
            client = genai.Client(api_key=Config.GEMINI_API_KEY)
            prompt = (
                f"You are a helpful, encouraging peer tutor on an educational community board. "
                f"Provide a friendly, insightful hint for this question without giving away the final numerical answer:\n\n{user_question}"
            )
            res = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            if res.text:
                return res.text.strip()
        except Exception:
            pass

    # Heuristic fallback hint
    return (
        "💡 Helpful Peer Hint: Think about what the question is asking in terms of energy/variance balance! "
        "Try isolating the known quantities first, and verify whether the formula calls for squaring deviations "
        "or dividing by degrees of freedom (N-1). That usually unblocks the solution!"
    )
