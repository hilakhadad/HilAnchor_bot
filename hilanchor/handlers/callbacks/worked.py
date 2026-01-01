import logging
from telegram import Update
from telegram.ext import ContextTypes

from ...auth import reject_non_owner
from ...keyboards import kb_no_reason, kb_yes_next
from ...nudges import choose_nudge_minutes, schedule_nudge
from ...state_store import (
    load_state, save_state,
    set_worked, set_need_followup, reset_fail,
    set_waiting, append_event
)
from ...llm import humanize_message
from ... import messages as msg

logger = logging.getLogger(__name__)

async def on_worked_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if await reject_non_owner(update, context):
        return

    _, worked = query.data.split(":", 1)
    logger.info(f"✅ User answered check-in: {worked}")

    state = load_state()
    set_worked(state, worked)
    append_event(state, "checkin_answer", value=worked)

    if worked == "yes":
        logger.info("🎉 User worked - asking what they accomplished")
        set_need_followup(state, False)
        reset_fail(state)
        set_waiting(state, "yes_what_did")
        save_state(state)
        text = humanize_message(msg.WORKED_YES, context="user worked today - asking what they did")
        await query.edit_message_text(text)
        logger.info("📤 Sent 'what did you do' prompt")
        return

    if worked == "partial":
        logger.info("⚡ User worked partially - asking for next step")
        set_need_followup(state, True)
        reset_fail(state)
        set_waiting(state, "partial_plan")
        save_state(state)
        text = humanize_message(msg.WORKED_PARTIAL, context="user worked partially - asking for small next step")
        await query.edit_message_text(text)
        logger.info("📤 Sent partial work follow-up")
        return

    # worked == "no"
    logger.info("❌ User didn't work - asking for reason")
    set_need_followup(state, True)
    save_state(state)
    text = humanize_message(msg.WORKED_NO, context="user didn't work - asking why")
    await query.edit_message_text(text, reply_markup=kb_no_reason())
    logger.info("📤 Sent 'no work' reason selection")
