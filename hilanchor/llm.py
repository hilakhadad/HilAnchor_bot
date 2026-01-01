"""
LLM integration for humanizing bot responses using Ollama.
"""
import ollama
from typing import Optional
from .config import USE_LLM, LLM_MODEL
from . import messages as msg

DEFAULT_MODEL = LLM_MODEL


def humanize_message(
    original_message: str,
    context: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    fallback_on_error: bool = True
) -> str:
    """
    Takes a bot message and makes it more human, warm, and varied using Ollama.

    Args:
        original_message: The original bot message to humanize
        context: Optional context about the conversation (e.g., "user just completed a task")
        model: The Ollama model to use
        fallback_on_error: If True, return original message on error; if False, raise error

    Returns:
        Humanized version of the message, or original if error and fallback_on_error=True
    """
    # If LLM is disabled, return original message
    if not USE_LLM:
        return original_message

    try:
        prompt = f"""את עוזרת אישית תומכת ומעודדת בעברית.
המשימה שלך: לקחת הודעת בוט ולהפוך אותה להודעה אנושית, חמה ומגוונת.

הודעה מקורית: "{original_message}"
{f'הקשר: {context}' if context else ''}

הנחיות:
- כתבי בעברית בלבד
- שמרי על אותו תוכן ומשמעות, אבל עם וריאציה אנושית
- הוסיפי חום ותמיכה אמיתית
- השתמשי בסגנון דיבור טבעי ונעים
- אל תשני את המשמעות או הכוונה
- אל תוסיפי הסברים או מטא-טקסט
- אם יש אימוג׳י בהודעה המקורית, אפשר להשאיר או להחליף באימוג׳י אחר מתאים

רק התגובה המעובדת, ללא הסברים:"""

        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={
                "temperature": 0.8,  # Higher for more variation
                "top_p": 0.9,
            }
        )

        humanized = response['response'].strip()

        # Basic validation - if the response is suspiciously long, use original
        if len(humanized) > len(original_message) * 3:
            if fallback_on_error:
                return original_message
            raise ValueError("LLM response too long")

        return humanized if humanized else original_message

    except Exception as e:
        print(f"⚠️ LLM humanization failed: {e}")
        if fallback_on_error:
            return original_message
        raise


def humanize_nudge(minutes: int, model: str = DEFAULT_MODEL) -> str:
    """
    Generate a humanized nudge message based on the time interval.
    """
    base_msg = msg.nudge_message(minutes)
    context = f"nudge after {minutes} minutes"
    return humanize_message(base_msg, context=context, model=model)


def humanize_checkin(stage: str, model: str = DEFAULT_MODEL) -> str:
    """
    Generate a humanized check-in message based on the time of day.
    """
    checkin_messages = {
        "11": msg.CHECKIN_11,
        "14": msg.CHECKIN_14,
        "17": msg.CHECKIN_17
    }

    base_msg = checkin_messages.get(stage, msg.CHECKIN_MANUAL)
    context = f"check-in at {stage}:00"
    return humanize_message(base_msg, context=context, model=model)


# Utility function to test if Ollama is running and the model is available
def test_ollama_connection(model: str = DEFAULT_MODEL) -> bool:
    """Test if Ollama is running and the model is available."""
    try:
        ollama.generate(model=model, prompt="test", options={"num_predict": 1})
        return True
    except Exception as e:
        print(f"⚠️ Ollama connection test failed: {e}")
        print(f"💡 Make sure Ollama is running and model '{model}' is installed.")
        print(f"   Run: ollama pull {model}")
        return False
