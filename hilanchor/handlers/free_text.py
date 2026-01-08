# hilanchor/handlers/free_text.py

import logging
from telegram import Update
from telegram.ext import ContextTypes

from ..auth import reject_non_owner
from ..keyboards import kb_yes_next, kb_timing_choice
from ..state_store import load_state, get_waiting, save_state, set_last_plan, append_event, clear_waiting
from ..llm import humanize_message
from .. import messages as msg

logger = logging.getLogger(__name__)


def _save_text_and_ask_timing(state: dict, event_name: str, text: str) -> None:
    """Save the user's text and prepare to ask for timing choice."""
    set_last_plan(state, text)
    append_event(state, event_name, text=text)
    clear_waiting(state)
    save_state(state)


async def _handle_yes_what_did(update, context, state, text: str):
    _save_text_and_ask_timing(state, event_name="did", text=text)
    response = humanize_message(
        msg.TIMING_CHOICE_QUESTION,
        context="user shared what they did - asking when to check in"
    )
    await update.message.reply_text(response, reply_markup=kb_timing_choice())


async def _handle_partial_plan(update, context, state, text: str):
    _save_text_and_ask_timing(state, event_name="plan", text=text)
    response = humanize_message(
        msg.TIMING_CHOICE_QUESTION,
        context="user shared plan - asking when to check in"
    )
    await update.message.reply_text(response, reply_markup=kb_timing_choice())


async def _handle_no_stuck_first_action(update, context, state, text: str):
    _save_text_and_ask_timing(state, event_name="first_action", text=text)
    response = humanize_message(
        msg.TIMING_CHOICE_QUESTION,
        context="user identified first action - asking when to check in"
    )
    await update.message.reply_text(response, reply_markup=kb_timing_choice())


async def _handle_no_fear_reframe(update, context, state, text: str):
    _save_text_and_ask_timing(state, event_name="fear_reframe", text=text)
    response = humanize_message(
        msg.TIMING_CHOICE_QUESTION,
        context="user reframed fear - asking when to check in"
    )
    await update.message.reply_text(response, reply_markup=kb_timing_choice())


async def _handle_big_3_bullets(update, context, state, text: str):
    _save_text_and_ask_timing(state, event_name="bullets", text=text)
    response = humanize_message(
        msg.TIMING_CHOICE_QUESTION,
        context="user wrote bullets - asking when to check in"
    )
    await update.message.reply_text(response, reply_markup=kb_timing_choice())


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
