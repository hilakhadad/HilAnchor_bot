import logging
from telegram import Update
from telegram.ext import ContextTypes

from ...auth import reject_non_owner
from ...nudges import schedule_nudge, cancel_existing_nudge
from ...state_store import (
    load_state, save_state,
    set_need_followup, append_event
)
from ...llm import humanize_message
from ... import messages as msg

logger = logging.getLogger(__name__)


async def on_timing_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if await reject_non_owner(update, context):
        return

    _, choice = query.data.split(":", 1)
    state = load_state()
    chat_id = query.message.chat_id

    if choice == "next":
        # User doesn't want nudges until next scheduled check-in
        set_need_followup(state, False)
        append_event(state, "timing_choice", value="next_checkin")
        save_state(state)
        cancel_existing_nudge(context, chat_id)
        text = humanize_message(
            msg.TIMING_NEXT_CHECKIN_CONFIRMED,
            context="user chose to wait until next scheduled check-in"
        )
        await query.edit_message_text(text)
        logger.info("⏰ User chose to wait until next scheduled check-in")
        return

    # User chose a specific time
    minutes = int(choice)
    set_need_followup(state, True)
    append_event(state, "timing_choice", value=minutes)
    save_state(state)

    schedule_nudge(context, chat_id=chat_id, minutes=minutes)

    text = humanize_message(
        msg.timing_confirmed(minutes),
        context=f"user chose {minutes} min check-in"
    )
    await query.edit_message_text(text)
    logger.info(f"⏰ User chose {minutes} minute check-in")
