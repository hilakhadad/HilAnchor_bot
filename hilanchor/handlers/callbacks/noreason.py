from telegram import Update
from telegram.ext import ContextTypes

from ...auth import reject_non_owner
from ...keyboards import kb_big_action
from ...state_store import (
    load_state, save_state,
    set_context, set_waiting, append_event
)
from ...llm import humanize_message
from ... import messages as msg

async def on_no_reason(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if await reject_non_owner(update, context):
        return

    _, reason = query.data.split(":", 1)
    state = load_state()

    if reason == "big":
        set_context(state, "overwhelmed")
        append_event(state, "context", value="overwhelmed")
        save_state(state)
        text = humanize_message(
            msg.REASON_BIG,
            context="task too big - suggesting to break it down"
        )
        await query.edit_message_text(text, reply_markup=kb_big_action())
        return

    if reason == "stuck":
        set_context(state, "stuck")
        append_event(state, "context", value="stuck")
        set_waiting(state, "no_stuck_first_action")
        save_state(state)
        text = humanize_message(
            msg.REASON_STUCK,
            context="user stuck - asking for first technical step"
        )
        await query.edit_message_text(text)
        return

    # reason == "fear"
    set_context(state, "fear")
    append_event(state, "context", value="fear")
    set_waiting(state, "no_fear_reframe")
    save_state(state)
    text = humanize_message(
        msg.REASON_FEAR,
        context="user afraid of failure - reframing expectations"
    )
    await query.edit_message_text(text)
