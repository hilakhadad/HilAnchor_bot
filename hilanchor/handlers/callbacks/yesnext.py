from telegram import Update
from telegram.ext import ContextTypes

from ...auth import reject_non_owner
from ...nudges import schedule_nudge, cancel_existing_nudge
from ...state_store import (
    load_state, save_state,
    mark_done, set_need_followup, append_event
)
from ...llm import humanize_message
from ... import messages as msg

async def on_yes_next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if await reject_non_owner(update, context):
        return

    _, choice = query.data.split(":", 1)
    state = load_state()

    if choice == "close":
        mark_done(state, True)
        set_need_followup(state, False)
        append_event(state, "closed", value=True)
        save_state(state)
        cancel_existing_nudge(context, query.message.chat_id)
        text = humanize_message(msg.CLOSE_FOR_DAY, context="user closing for the day - encouraging")
        await query.edit_message_text(text)
        return

    if choice == "flow":
        # User is in flow - cancel nudges but don't close the day
        set_need_followup(state, False)
        append_event(state, "in_flow", value=True)
        save_state(state)
        cancel_existing_nudge(context, query.message.chat_id)
        text = humanize_message(msg.IN_FLOW_CONFIRMED, context="user is in flow - no interruptions")
        await query.edit_message_text(text)
        return

    # choice == "continue"
    set_need_followup(state, True)
    append_event(state, "continue", value=True)
    save_state(state)
    text = humanize_message(msg.CONTINUE_30MIN, context="user wants to continue - scheduling 60min check-in")
    await query.edit_message_text(text)
    schedule_nudge(context, chat_id=query.message.chat_id, minutes=60)
