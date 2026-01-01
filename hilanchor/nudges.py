import logging
from telegram.ext import ContextTypes

from .state_store import today_key
from .keyboards import kb_nudge_progress
from .llm import humanize_nudge

logger = logging.getLogger(__name__)

NUDGE_JOB_NAME_PREFIX = "nudge_"


def choose_nudge_minutes(plan_text: str, default_minutes: int = 10) -> int:
    t = (plan_text or "").lower()

    keywords_5 = ["2", "שתיים", "two", "רק לפתוח", "בקטנה", "bullet", "נקודות", "פשוט לפתוח"]
    keywords_10 = ["10", "עשר", "להתחיל", "להמשיך", "start", "continue"]
    keywords_30 = ["30", "חצי שעה", "באמצע", "זורם", "נשאבתי", "in the middle", "flow"]

    if any(k in t for k in keywords_30):
        return 30
    if any(k in t for k in keywords_5):
        return 5
    if any(k in t for k in keywords_10):
        return 10
    return default_minutes


def nudge_job_name(chat_id: int) -> str:
    return f"{NUDGE_JOB_NAME_PREFIX}{chat_id}_{today_key()}"


def cancel_existing_nudge(context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> None:
    for job in context.job_queue.get_jobs_by_name(nudge_job_name(chat_id)):
        job.schedule_removal()


async def nudge_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    data = context.job.data or {}
    chat_id = data.get("chat_id")
    minutes = data.get("minutes", 10)
    if not chat_id:
        logger.warning("⚠️ Nudge job triggered but no chat_id found")
        return

    logger.info(f"⏰ Sending {minutes}-minute nudge to chat {chat_id}")
    message_text = humanize_nudge(minutes)

    await context.bot.send_message(
        chat_id=chat_id,
        text=message_text,
        reply_markup=kb_nudge_progress()
    )
    logger.info("📤 Nudge message sent")


def schedule_nudge(context: ContextTypes.DEFAULT_TYPE, chat_id: int, minutes: int) -> None:
    cancel_existing_nudge(context, chat_id)
    logger.info(f"⏱️ Scheduling nudge for chat {chat_id} in {minutes} minutes")
    context.job_queue.run_once(
        nudge_job,
        when=max(1, minutes) * 60,
        data={"chat_id": chat_id, "minutes": minutes},
        name=nudge_job_name(chat_id),
    )
    logger.info(f"✅ Nudge scheduled successfully")
