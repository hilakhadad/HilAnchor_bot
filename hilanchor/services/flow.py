# hilanchor/services/flow.py

from __future__ import annotations

from ..state_store import (
    save_state,
    clear_waiting,
    set_last_plan,
    append_event,
    mark_done,
    set_need_followup,
)
from ..nudges import choose_nudge_minutes, schedule_nudge, cancel_existing_nudge


def record_text_and_close_waiting(state: dict, event_name: str, text: str) -> None:
    """
    Save free text, append event, clear waiting, save state.
    """
    set_last_plan(state, text)
    append_event(state, event_name, text=text)
    clear_waiting(state)
    save_state(state)


def record_text_schedule_nudge(
    *,
    state: dict,
    context,
    chat_id: int,
    text: str,
    event_name: str,
    default_minutes: int,
) -> int:
    """
    Save text, append event(s), schedule nudge, clear waiting, save state.
    Returns chosen minutes.
    """
    set_last_plan(state, text)

    mins = choose_nudge_minutes(text, default_minutes=default_minutes)

    append_event(state, event_name, text=text)
    append_event(state, "nudge_scheduled", value=mins)

    clear_waiting(state)
    save_state(state)

    schedule_nudge(context, chat_id=chat_id, minutes=mins)
    return mins


def finish_day(
    *,
    state: dict,
    context,
    chat_id: int,
) -> None:
    """
    Mark day as done, cancel existing nudge, save.
    """
    mark_done(state, True)
    set_need_followup(state, False)
    append_event(state, "closed", value=True)
    save_state(state)

    cancel_existing_nudge(context, chat_id)


def continue_and_nudge(
    *,
    state: dict,
    context,
    chat_id: int,
    minutes: int,
) -> None:
    """
    Continue flow: mark need_followup and schedule a nudge.
    """
    set_need_followup(state, True)
    append_event(state, "continue", value=True)
    save_state(state)

    schedule_nudge(context, chat_id=chat_id, minutes=minutes)
