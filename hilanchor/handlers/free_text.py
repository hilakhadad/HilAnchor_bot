# hilanchor/handlers/free_text.py

import logging
from telegram import Update
from telegram.ext import ContextTypes

from ..auth import reject_non_owner
from ..keyboards import kb_yes_next
from ..state_store import load_state, get_waiting
from ..services.flow import (
    record_text_and_close_waiting,
    record_text_schedule_nudge,
)
from ..llm import humanize_message
from .. import messages as msg

logger = logging.getLogger(__name__)


async def _handle_yes_what_did(update, context, state, text: str):
    record_text_and_close_waiting(state, event_name="did", text=text)
    response = humanize_message(
        msg.YES_WHAT_DID_RECEIVED,
        context="user shared what they did - asking if continue or close"
    )
    await update.message.reply_text(response, reply_markup=kb_yes_next())


async def _handle_partial_plan(update, context, state, text: str):
    mins = record_text_schedule_nudge(
        state=state,
        context=context,
        chat_id=update.effective_chat.id,
        text=text,
        event_name="plan",
        default_minutes=30,
    )
    response = humanize_message(
        msg.plan_received(mins),
        context=f"scheduled {mins} min nudge for partial work plan"
    )
    await update.message.reply_text(response)


async def _handle_no_stuck_first_action(update, context, state, text: str):
    mins = record_text_schedule_nudge(
        state=state,
        context=context,
        chat_id=update.effective_chat.id,
        text=text,
        event_name="first_action",
        default_minutes=20,
    )
    response = humanize_message(
        msg.stuck_received(mins),
        context=f"user identified first action when stuck - scheduled {mins} min"
    )
    await update.message.reply_text(response)


async def _handle_no_fear_reframe(update, context, state, text: str):
    mins = record_text_schedule_nudge(
        state=state,
        context=context,
        chat_id=update.effective_chat.id,
        text=text,
        event_name="fear_reframe",
        default_minutes=15,
    )
    response = humanize_message(
        msg.fear_reframe_received(mins),
        context=f"user reframed fear - scheduled gentle {mins} min nudge"
    )
    await update.message.reply_text(response)


async def _handle_big_3_bullets(update, context, state, text: str):
    mins = record_text_schedule_nudge(
        state=state,
        context=context,
        chat_id=update.effective_chat.id,
        text=text,
        event_name="bullets",
        default_minutes=15,
    )
    response = humanize_message(
        msg.BULLETS_RECEIVED,
        context="user wrote 3 bullets - asking to pick one for 5 min start"
    )
    await update.message.reply_text(response)


async def _handle_journal_add(update, context, state, text: str):
    """Handle adding text to personal journal."""
    from ..journal import append_to_journal
    from ..state_store import set_waiting, save_state

    success = append_to_journal(text, include_timestamp=True)

    if success:
        await update.message.reply_text(msg.JOURNAL_ADD_SUCCESS)
    else:
        await update.message.reply_text(msg.JOURNAL_ADD_ERROR)

    # Clear waiting state
    set_waiting(state, None)
    save_state(state)


WAITING_HANDLERS = {
    "yes_what_did": _handle_yes_what_did,
    "partial_plan": _handle_partial_plan,
    "no_stuck_first_action": _handle_no_stuck_first_action,
    "no_fear_reframe": _handle_no_fear_reframe,
    "big_3_bullets": _handle_big_3_bullets,
    "journal_add": _handle_journal_add,
}


async def _handle_free_note(update, context, state, text: str):
    """Handle free text notes - always available for user to add thoughts."""
    from ..state_store import append_event, save_state

    append_event(state, "free_note", text=text)
    save_state(state)

    await update.message.reply_text(msg.FREE_NOTE_SAVED)


async def on_free_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_non_owner(update, context):
        return

    text = (update.message.text or "").strip()
    if not text:
        return

    user_id = update.effective_user.id if update.effective_user else "Unknown"
    logger.info(f"💬 Received text message from user {user_id}: '{text[:50]}...'")

    state = load_state()
    waiting = get_waiting(state)

    # If we're waiting for specific input, handle it
    if waiting:
        logger.info(f"⏳ Processing text for waiting state: {waiting}")
        handler = WAITING_HANDLERS.get(waiting)
        if handler:
            await handler(update, context, state, text)
            logger.info(f"✅ Completed handling for state: {waiting}")
            return

    # Otherwise, treat as a free note - user adding thoughts/reflections
    logger.info("📝 Processing as free note")
    await _handle_free_note(update, context, state, text)
