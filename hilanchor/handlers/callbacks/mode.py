import logging
from telegram import Update
from telegram.ext import ContextTypes

from ...auth import reject_non_owner
from ...keyboards import kb_worked
from ...state_store import (
    load_state, save_state,
    set_mode, append_event
)
from ...llm import humanize_message
from ... import messages as msg

logger = logging.getLogger(__name__)

async def on_mode_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if await reject_non_owner(update, context):
        return

    _, today_mode = query.data.split(":", 1)
    logger.info(f"🎯 User selected mode: {today_mode}")

    state = load_state()
    set_mode(state, today_mode)
    append_event(state, "mode_set", value=today_mode)
    save_state(state)
    logger.info(f"💾 Saved mode '{today_mode}' to state")

    if today_mode == "kid":
        text = humanize_message(msg.MODE_KID_CONFIRMED, context="confirming kid mode")
        await query.edit_message_text(text)
        logger.info("📤 Sent kid mode confirmation")
    else:
        text = humanize_message(msg.MODE_WORK_CONFIRMED, context="confirming work mode")
        await query.edit_message_text(text)
        logger.info("📤 Sent work mode confirmation")

    checkin_msg = humanize_message(msg.MODE_FIRST_CHECKIN, context="first check-in after mode selection")
    await query.message.reply_text(checkin_msg, reply_markup=kb_worked())
    logger.info("📤 Sent first check-in prompt")