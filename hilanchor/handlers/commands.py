import logging
from telegram import Update
from telegram.ext import ContextTypes

from ..auth import reject_non_owner
from ..keyboards import kb_worked, kb_day_mode
from ..state_store import (
    load_state, save_state,
    set_mode, append_event, set_waiting
)
from ..summary import generate_daily_summary
from ..journal import read_journal, append_to_journal, get_journal_summary
from .. import messages as msg

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id if update.effective_user else "Unknown"
    logger.info(f"📥 Received /start command from user {user_id}")

    if await reject_non_owner(update, context):
        logger.warning(f"⛔ Rejected /start from unauthorized user {user_id}")
        return

    logger.info("✅ Sending welcome message and mode selection")
    await update.message.reply_text(msg.START_MESSAGE)
    await update.message.reply_text(msg.START_MODE_QUESTION, reply_markup=kb_day_mode())
    logger.info("📤 Start sequence completed")



async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id if update.effective_user else "Unknown"
    logger.info(f"📥 Received /checkin command from user {user_id}")

    if await reject_non_owner(update, context):
        logger.warning(f"⛔ Rejected /checkin from unauthorized user {user_id}")
        return

    logger.info("📤 Sending manual check-in prompt")
    await update.message.reply_text(msg.CHECKIN_MANUAL, reply_markup=kb_worked())


async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show daily summary on demand."""
    user_id = update.effective_user.id if update.effective_user else "Unknown"
    logger.info(f"📥 Received /summary command from user {user_id}")

    if await reject_non_owner(update, context):
        logger.warning(f"⛔ Rejected /summary from unauthorized user {user_id}")
        return

    logger.info("📊 Generating daily summary...")
    summary_text = generate_daily_summary()
    logger.info("📤 Sending daily summary")
    await update.message.reply_text(summary_text, parse_mode="Markdown")


async def journal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show journal content."""
    user_id = update.effective_user.id if update.effective_user else "Unknown"
    logger.info(f"📥 Received /journal command from user {user_id}")

    if await reject_non_owner(update, context):
        logger.warning(f"⛔ Rejected /journal from unauthorized user {user_id}")
        return

    logger.info("📖 Reading journal content...")
    journal_content = read_journal()

    # Telegram message limit is 4096 characters
    if len(journal_content) > 4000:
        # Send in chunks
        chunks = [journal_content[i:i+4000] for i in range(0, len(journal_content), 4000)]
        logger.info(f"📤 Sending journal in {len(chunks)} chunks")
        for i, chunk in enumerate(chunks, 1):
            header = f"📓 יומן אישי (חלק {i}/{len(chunks)}):\n\n" if i == 1 else ""
            await update.message.reply_text(header + chunk)
    else:
        logger.info("📤 Sending journal content")
        await update.message.reply_text(f"📓 יומן אישי:\n\n{journal_content}")


async def journal_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Prompt user to add content to journal."""
    user_id = update.effective_user.id if update.effective_user else "Unknown"
    logger.info(f"📥 Received /journal_add command from user {user_id}")

    if await reject_non_owner(update, context):
        logger.warning(f"⛔ Rejected /journal_add from unauthorized user {user_id}")
        return

    state = load_state()
    set_waiting(state, "journal_add")
    save_state(state)

    logger.info("✍️ Waiting for journal entry...")
    await update.message.reply_text(
        "✍️ כתבי את מה שאת רוצה להוסיף ליומן האישי שלך.\n"
        "הטקסט יישמר עם חותמת זמן."
    )


async def journal_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show journal statistics."""
    user_id = update.effective_user.id if update.effective_user else "Unknown"
    logger.info(f"📥 Received /journal_info command from user {user_id}")

    if await reject_non_owner(update, context):
        logger.warning(f"⛔ Rejected /journal_info from unauthorized user {user_id}")
        return

    logger.info("📊 Getting journal info...")
    info = get_journal_summary()
    logger.info("�� Sending journal info")
    await update.message.reply_text(info)