from telegram import Update
from telegram.ext import ContextTypes

from ...auth import reject_non_owner
from ...state_store import load_state, save_state, set_waiting, append_event
from ...llm import humanize_message
from ... import messages as msg

async def on_big_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if await reject_non_owner(update, context):
        return

    _, action = query.data.split(":", 1)
    if action == "skip":
        text = humanize_message(msg.BIG_ACTION_SKIP, context="user skipping 2min task")
        await query.edit_message_text(text)
        return

    state = load_state()
    set_waiting(state, "big_3_bullets")
    append_event(state, "big_action", value="do2")
    save_state(state)

    text = humanize_message(msg.BIG_ACTION_DO, context="user agreed to 2min task - asking for 3 bullet points")
    await query.edit_message_text(text)
