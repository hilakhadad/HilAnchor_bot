import logging
import datetime as dt
import zoneinfo
from telegram.ext import ContextTypes

from .config import OWNER_USER_ID_INT, OWNER_CHAT_ID_INT
from .state_store import load_state, is_done, get_mode, need_followup
from .keyboards import kb_worked, kb_day_mode
from .llm import humanize_checkin
from .summary import generate_daily_summary
from . import messages as msg

logger = logging.getLogger(__name__)

ISRAEL_TZ = zoneinfo.ZoneInfo("Asia/Jerusalem")

DAILY_STAGE_11 = "11"
DAILY_STAGE_14 = "14"
DAILY_STAGE_17 = "17"


async def send_checkin(chat_id: int, context: ContextTypes.DEFAULT_TYPE, stage: str) -> None:
    logger.info(f"⏰ Scheduled check-in triggered for stage {stage}")

    # Skip on Friday (4) and Saturday (5)
    now = dt.datetime.now(ISRAEL_TZ)
    if now.weekday() in (4, 5):
        logger.info(f"🕊️ Shabbat/Weekend (day {now.weekday()}) - skipping stage {stage} check-in")
        return

    state = load_state()

    if is_done(state):
        logger.info(f"✅ User already marked as done - skipping stage {stage} check-in")
        return

    mode = get_mode(state)
    if stage == DAILY_STAGE_17 and mode == "kid":
        logger.info(f"👶 Kid mode active - skipping stage {stage} check-in")
        return

    if stage in (DAILY_STAGE_14, DAILY_STAGE_17) and not need_followup(state):
        logger.info(f"🎯 No follow-up needed - skipping stage {stage} check-in")
        return

    logger.info(f"📤 Sending stage {stage} check-in to chat {chat_id}")
    text = humanize_checkin(stage)
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=kb_worked())


async def job_11(context):
    logger.info("⏰ Running 11:00 morning job - sending mode selection")

    # Skip on Friday (4) and Saturday (5)
    now = dt.datetime.now(ISRAEL_TZ)
    if now.weekday() in (4, 5):
        logger.info(f"🕊️ Shabbat/Weekend (day {now.weekday()}) - skipping morning message")
        return

    await context.bot.send_message(
        chat_id=OWNER_CHAT_ID_INT,
        text=msg.MORNING_11,
        reply_markup=kb_day_mode()
    )
    logger.info("📤 Sent morning mode selection message")


async def job_14(context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("⏰ Running 14:00 check-in job")
    await send_checkin(chat_id=OWNER_USER_ID_INT, context=context, stage=DAILY_STAGE_14)


async def job_17(context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("⏰ Running 17:00 check-in job")
    await send_checkin(chat_id=OWNER_USER_ID_INT, context=context, stage=DAILY_STAGE_17)


async def job_22_summary(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send daily summary at 22:00."""
    logger.info("⏰ Running 22:00 summary job")

    # Skip on Friday (4) and Saturday (5)
    now = dt.datetime.now(ISRAEL_TZ)
    if now.weekday() in (4, 5):
        logger.info(f"🕊️ Shabbat/Weekend (day {now.weekday()}) - skipping summary")
        return

    summary = generate_daily_summary()
    logger.info("📊 Generated daily summary - sending to user")
    await context.bot.send_message(
        chat_id=OWNER_CHAT_ID_INT,
        text=summary,
        parse_mode="Markdown"
    )
    logger.info("📤 Sent daily summary")


def register_jobs(app) -> None:
    logger.info("📅 Registering daily scheduled jobs:")
    logger.info("   - 11:00 (Israel time): Morning mode selection")
    logger.info("   - 14:00 (Israel time): Afternoon check-in")
    logger.info("   - 17:00 (Israel time): Evening check-in")
    logger.info("   - 22:00 (Israel time): Daily summary")

    app.job_queue.run_daily(job_11, time=dt.time(hour=11, minute=0, tzinfo=ISRAEL_TZ))
    app.job_queue.run_daily(job_14, time=dt.time(hour=14, minute=0, tzinfo=ISRAEL_TZ))
    app.job_queue.run_daily(job_17, time=dt.time(hour=17, minute=0, tzinfo=ISRAEL_TZ))
    app.job_queue.run_daily(job_22_summary, time=dt.time(hour=22, minute=0, tzinfo=ISRAEL_TZ))

    logger.info("✅ All scheduled jobs registered successfully")
