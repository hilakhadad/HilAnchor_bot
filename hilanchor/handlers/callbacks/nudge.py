from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from ...auth import reject_non_owner
from ...keyboards import kb_yes_next
from ...nudges import cancel_existing_nudge
from ...state_store import (
    load_state, save_state,
    reset_fail, bump_fail,
    mark_done, set_need_followup, set_waiting, append_event
)
from ...llm import humanize_message
from ... import messages as msg

async def on_nudge_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if await reject_non_owner(update, context):
        return

    _, prog = query.data.split(":", 1)
    state = load_state()

    if prog == "flow":
        # User is in flow - cancel nudges but don't close the day
        set_need_followup(state, False)
        append_event(state, "in_flow", value=True)
        save_state(state)
        cancel_existing_nudge(context, query.message.chat_id)
        text = humanize_message(msg.IN_FLOW_CONFIRMED, context="user is in flow - no interruptions")
        await query.edit_message_text(text)
        return

    if prog in ("yes", "partial"):
        reset_fail(state)
        save_state(state)
        if prog == "yes":
            text = humanize_message(msg.NUDGE_YES_PROGRESS, context="user made progress - asking continue or close")
            await query.edit_message_text(text, reply_markup=kb_yes_next())
        else:
            text = humanize_message(
                msg.NUDGE_PARTIAL_PROGRESS,
                context="user made partial progress - offering more time or close"
            )
            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(msg.BTN_CONTINUE_10, callback_data="yesnext:continue"),
                        InlineKeyboardButton(msg.BTN_CLOSE, callback_data="yesnext:close"),
                    ],
                    [
                        InlineKeyboardButton(msg.BTN_IN_FLOW, callback_data="nudge:flow"),
                    ]
                ])
            )
        return

    fail = bump_fail(state)
    if fail >= 2:
        mark_done(state, True)
        set_need_followup(state, False)
        save_state(state)
        text = humanize_message(msg.NUDGE_GIVE_UP, context="user struggled twice - releasing for the day with compassion")
        await query.edit_message_text(text)
        return

    text = humanize_message(msg.NUDGE_NO_PROGRESS, context="user didn't progress - asking for smallest possible 2min task")
    await query.edit_message_text(text)
    set_waiting(state, "partial_plan")
    save_state(state)
