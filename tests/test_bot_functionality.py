"""
Tests for bot functionality - handlers, keyboards, summary, and state management.
These tests ensure the bot logic works correctly even when messages change.
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime
import json

from hilanchor.keyboards import (
    kb_day_mode,
    kb_worked,
    kb_no_reason,
    kb_yes_next,
    kb_big_action,
    kb_nudge_progress,
)
TELEGRAM_AVAILABLE = True

from hilanchor.summary import generate_daily_summary
from hilanchor.state_store import (
    load_state,
    save_state,
    today_key,
    set_mode,
    set_worked,
    append_event,
    get_mode,
    is_done,
    need_followup,
)
from hilanchor import messages as msg


@pytest.mark.skipif(not TELEGRAM_AVAILABLE, reason="telegram library not installed")
class TestKeyboards:
    """Test keyboard generation and structure."""

    def test_kb_day_mode_structure(self):
        """Test day mode keyboard has correct structure."""
        kb = kb_day_mode()
        assert kb is not None
        assert hasattr(kb, 'inline_keyboard')
        assert len(kb.inline_keyboard) == 1  # One row
        assert len(kb.inline_keyboard[0]) == 2  # Two buttons (kid/work)

    def test_kb_day_mode_callback_data(self):
        """Test day mode buttons have correct callback data."""
        kb = kb_day_mode()
        buttons = kb.inline_keyboard[0]
        callback_data = [btn.callback_data for btn in buttons]
        assert "on_mode_choice:kid" in callback_data
        assert "on_mode_choice:work" in callback_data

    def test_kb_worked_structure(self):
        """Test worked keyboard has correct structure."""
        kb = kb_worked()
        assert kb is not None
        assert len(kb.inline_keyboard) == 1  # One row
        assert len(kb.inline_keyboard[0]) == 3  # Three buttons (yes/partial/no)

    def test_kb_worked_callback_data(self):
        """Test worked buttons have correct callback data."""
        kb = kb_worked()
        buttons = kb.inline_keyboard[0]
        callback_data = [btn.callback_data for btn in buttons]
        assert "worked:yes" in callback_data
        assert "worked:partial" in callback_data
        assert "worked:no" in callback_data

    def test_kb_no_reason_structure(self):
        """Test no reason keyboard has correct structure."""
        kb = kb_no_reason()
        assert kb is not None
        assert len(kb.inline_keyboard) == 3  # Three rows
        assert all(len(row) == 1 for row in kb.inline_keyboard)  # One button per row

    def test_kb_no_reason_callback_data(self):
        """Test no reason buttons have correct callback data."""
        kb = kb_no_reason()
        callback_data = [row[0].callback_data for row in kb.inline_keyboard]
        assert "noreason:big" in callback_data
        assert "noreason:stuck" in callback_data
        assert "noreason:fear" in callback_data

    def test_kb_yes_next_structure(self):
        """Test yes/next keyboard has correct structure."""
        kb = kb_yes_next()
        assert kb is not None
        assert len(kb.inline_keyboard) == 1  # One row
        assert len(kb.inline_keyboard[0]) == 2  # Two buttons (continue/close)

    def test_kb_yes_next_callback_data(self):
        """Test yes/next buttons have correct callback data."""
        kb = kb_yes_next()
        buttons = kb.inline_keyboard[0]
        callback_data = [btn.callback_data for btn in buttons]
        assert "yesnext:continue" in callback_data
        assert "yesnext:close" in callback_data

    def test_kb_big_action_structure(self):
        """Test big action keyboard has correct structure."""
        kb = kb_big_action()
        assert kb is not None
        assert len(kb.inline_keyboard) == 1  # One row
        assert len(kb.inline_keyboard[0]) == 2  # Two buttons (do2/skip)

    def test_kb_big_action_callback_data(self):
        """Test big action buttons have correct callback data."""
        kb = kb_big_action()
        buttons = kb.inline_keyboard[0]
        callback_data = [btn.callback_data for btn in buttons]
        assert "bigaction:do2" in callback_data
        assert "bigaction:skip" in callback_data

    def test_kb_nudge_progress_structure(self):
        """Test nudge progress keyboard has correct structure."""
        kb = kb_nudge_progress()
        assert kb is not None
        assert len(kb.inline_keyboard) == 1  # One row
        assert len(kb.inline_keyboard[0]) == 3  # Three buttons (yes/partial/no)

    def test_kb_nudge_progress_callback_data(self):
        """Test nudge progress buttons have correct callback data."""
        kb = kb_nudge_progress()
        buttons = kb.inline_keyboard[0]
        callback_data = [btn.callback_data for btn in buttons]
        assert "nudge:yes" in callback_data
        assert "nudge:partial" in callback_data
        assert "nudge:no" in callback_data


class TestStateStore:
    """Test state management functionality."""

    def setup_method(self):
        """Setup test state before each test."""
        self.test_state = {}

    def test_today_key_format(self):
        """Test that today_key returns YYYY-MM-DD format."""
        key = today_key()
        assert isinstance(key, str)
        assert len(key) == 10  # YYYY-MM-DD
        assert key.count('-') == 2
        # Verify it's a valid date
        datetime.strptime(key, "%Y-%m-%d")

    def test_set_mode(self):
        """Test setting mode in state."""
        state = {today_key(): {}}
        set_mode(state, "work")
        assert get_mode(state) == "work"

        set_mode(state, "kid")
        assert get_mode(state) == "kid"

    def test_set_worked(self):
        """Test setting worked status in state."""
        today = today_key()
        state = {today: {}}

        set_worked(state, "yes")
        assert state[today]["worked"] == "yes"

        set_worked(state, "partial")
        assert state[today]["worked"] == "partial"

        set_worked(state, "no")
        assert state[today]["worked"] == "no"

    def test_append_event(self):
        """Test appending events to state."""
        state = {today_key(): {"events": []}}

        append_event(state, "checkin_answer", value="yes")
        events = state[today_key()]["events"]

        assert len(events) == 1
        assert events[0]["type"] == "checkin_answer"
        assert events[0]["value"] == "yes"
        assert "ts" in events[0]

    def test_append_event_with_text(self):
        """Test appending events with text."""
        state = {today_key(): {"events": []}}

        append_event(state, "free_note", text="Test note")
        events = state[today_key()]["events"]

        assert len(events) == 1
        assert events[0]["type"] == "free_note"
        assert events[0]["text"] == "Test note"

    def test_is_done(self):
        """Test checking if day is done."""
        state = {today_key(): {"done": False}}
        assert not is_done(state)

        state = {today_key(): {"done": True}}
        assert is_done(state)

    def test_need_followup(self):
        """Test checking if followup is needed."""
        state = {today_key(): {"need_followup": True}}
        assert need_followup(state)

        state = {today_key(): {"need_followup": False}}
        assert not need_followup(state)


class TestSummary:
    """Test summary generation."""

    def test_summary_no_data(self):
        """Test summary when there's no data for today."""
        with patch('hilanchor.summary.load_state') as mock_load:
            mock_load.return_value = {}
            summary = generate_daily_summary()
            assert msg.SUMMARY_NO_DATA in summary or "לא היה פעילות" in summary

    def test_summary_with_mode_work(self):
        """Test summary includes work mode."""
        today = today_key()
        mock_state = {
            today: {
                "mode": "work",
                "events": []
            }
        }
        with patch('hilanchor.summary.load_state') as mock_load:
            mock_load.return_value = mock_state
            summary = generate_daily_summary()
            assert msg.SUMMARY_MODE_WORK in summary or "עבודה" in summary

    def test_summary_with_mode_kid(self):
        """Test summary includes kid mode."""
        today = today_key()
        mock_state = {
            today: {
                "mode": "kid",
                "events": []
            }
        }
        with patch('hilanchor.summary.load_state') as mock_load:
            mock_load.return_value = mock_state
            summary = generate_daily_summary()
            assert msg.SUMMARY_MODE_KID in summary or "בת" in summary or "אלה" in summary

    def test_summary_with_worked_yes(self):
        """Test summary shows worked status."""
        today = today_key()
        mock_state = {
            today: {
                "mode": "work",
                "worked": "yes",
                "events": []
            }
        }
        with patch('hilanchor.summary.load_state') as mock_load:
            mock_load.return_value = mock_state
            summary = generate_daily_summary()
            assert msg.SUMMARY_WORKED_YES in summary or "עבדת" in summary

    def test_summary_with_events(self):
        """Test summary includes events."""
        today = today_key()
        mock_state = {
            today: {
                "mode": "work",
                "worked": "yes",
                "events": [
                    {
                        "type": "checkin_answer",
                        "value": "yes",
                        "ts": datetime.now().isoformat()
                    },
                    {
                        "type": "free_note",
                        "text": "Test note",
                        "ts": datetime.now().isoformat()
                    }
                ]
            }
        }
        with patch('hilanchor.summary.load_state') as mock_load:
            mock_load.return_value = mock_state
            summary = generate_daily_summary()
            assert msg.SUMMARY_EVENTS_HEADER in summary or "מה קרה" in summary
            assert "Test note" in summary

    def test_summary_with_plan(self):
        """Test summary includes plan."""
        today = today_key()
        mock_state = {
            today: {
                "mode": "work",
                "plan": "Work on feature X",
                "events": []
            }
        }
        with patch('hilanchor.summary.load_state') as mock_load:
            mock_load.return_value = mock_state
            summary = generate_daily_summary()
            assert "Work on feature X" in summary

    def test_summary_day_done(self):
        """Test summary shows day is done."""
        today = today_key()
        mock_state = {
            today: {
                "mode": "work",
                "done": True,
                "events": []
            }
        }
        with patch('hilanchor.summary.load_state') as mock_load:
            mock_load.return_value = mock_state
            summary = generate_daily_summary()
            assert msg.SUMMARY_DAY_DONE in summary or "הושלם" in summary

    def test_summary_day_open(self):
        """Test summary shows day is still open."""
        today = today_key()
        mock_state = {
            today: {
                "mode": "work",
                "done": False,
                "events": []
            }
        }
        with patch('hilanchor.summary.load_state') as mock_load:
            mock_load.return_value = mock_state
            summary = generate_daily_summary()
            assert msg.SUMMARY_DAY_OPEN in summary or "פתוח" in summary


class TestLLMIntegration:
    """Test LLM integration functions."""

    def test_humanize_message_with_llm_disabled(self):
        """Test that humanize_message returns original when LLM is disabled."""
        from hilanchor.llm import humanize_message
        from hilanchor.config import USE_LLM

        if not USE_LLM:
            original = "Test message"
            result = humanize_message(original)
            assert result == original

    def test_humanize_checkin_returns_string(self):
        """Test that humanize_checkin returns a string."""
        from hilanchor.llm import humanize_checkin

        result11 = humanize_checkin("11")
        result14 = humanize_checkin("14")
        result17 = humanize_checkin("17")

        assert isinstance(result11, str)
        assert isinstance(result14, str)
        assert isinstance(result17, str)
        assert len(result11) > 0
        assert len(result14) > 0
        assert len(result17) > 0

    def test_humanize_nudge_returns_string(self):
        """Test that humanize_nudge returns a string."""
        from hilanchor.llm import humanize_nudge

        result = humanize_nudge(15)
        assert isinstance(result, str)
        assert len(result) > 0


class TestMessageFunctions:
    """Test dynamic message functions."""

    def test_plan_received_formatting(self):
        """Test plan_received includes the minutes."""
        result = msg.plan_received(10)
        assert "10" in result

    def test_stuck_received_formatting(self):
        """Test stuck_received includes the minutes."""
        result = msg.stuck_received(15)
        assert "15" in result

    def test_fear_reframe_received_formatting(self):
        """Test fear_reframe_received includes the minutes."""
        result = msg.fear_reframe_received(5)
        assert "5" in result

    def test_nudge_message_formatting(self):
        """Test nudge_message includes the minutes."""
        result = msg.nudge_message(20)
        assert "20" in result


@pytest.mark.skipif(not TELEGRAM_AVAILABLE, reason="telegram library not installed")
class TestCallbackDataPatterns:
    """Test callback data patterns for consistency."""

    def test_mode_choice_pattern(self):
        """Test mode choice callback data follows pattern."""
        from hilanchor.handlers.patterns import CB_MODE_PATTERN
        import re

        pattern = re.compile(CB_MODE_PATTERN)
        assert pattern.match("on_mode_choice:kid")
        assert pattern.match("on_mode_choice:work")
        assert not pattern.match("on_mode_choice:invalid")

    def test_worked_pattern(self):
        """Test worked callback data follows pattern."""
        from hilanchor.handlers.patterns import CB_WORKED_PATTERN
        import re

        pattern = re.compile(CB_WORKED_PATTERN)
        assert pattern.match("worked:yes")
        assert pattern.match("worked:partial")
        assert pattern.match("worked:no")
        assert not pattern.match("worked:invalid")

    def test_no_reason_pattern(self):
        """Test no reason callback data follows pattern."""
        from hilanchor.handlers.patterns import CB_NO_REASON_PATTERN
        import re

        pattern = re.compile(CB_NO_REASON_PATTERN)
        assert pattern.match("noreason:big")
        assert pattern.match("noreason:stuck")
        assert pattern.match("noreason:fear")
        assert not pattern.match("noreason:invalid")

    def test_yes_next_pattern(self):
        """Test yes/next callback data follows pattern."""
        from hilanchor.handlers.patterns import CB_YES_NEXT_PATTERN
        import re

        pattern = re.compile(CB_YES_NEXT_PATTERN)
        assert pattern.match("yesnext:continue")
        assert pattern.match("yesnext:close")
        assert not pattern.match("yesnext:invalid")

    def test_big_action_pattern(self):
        """Test big action callback data follows pattern."""
        from hilanchor.handlers.patterns import CB_BIG_ACTION_PATTERN
        import re

        pattern = re.compile(CB_BIG_ACTION_PATTERN)
        assert pattern.match("bigaction:do2")
        assert pattern.match("bigaction:skip")
        assert not pattern.match("bigaction:invalid")

    def test_nudge_pattern(self):
        """Test nudge callback data follows pattern."""
        from hilanchor.handlers.patterns import CB_NUDGE_PROGRESS_PATTERN
        import re

        pattern = re.compile(CB_NUDGE_PROGRESS_PATTERN)
        assert pattern.match("nudge:yes")
        assert pattern.match("nudge:partial")
        assert pattern.match("nudge:no")
        assert not pattern.match("nudge:invalid")


class TestEventTypes:
    """Test that event types are consistent."""

    def test_all_event_types_handled_in_summary(self):
        """Ensure summary handles all event types."""
        # These are all the event types the bot creates
        event_types = [
            "mode_set",
            "checkin_answer",
            "did",
            "plan",
            "first_action",
            "fear_reframe",
            "bullets",
            "context",
            "big_action",
            "nudge_scheduled",
            "closed",
            "continue",
            "free_note",
        ]

        # Read summary.py to check all types are handled
        import hilanchor.summary as summary_module
        import inspect

        summary_source = inspect.getsource(summary_module.generate_daily_summary)

        for event_type in event_types:
            # Each event type should be referenced in the summary function
            assert event_type in summary_source or event_type == "mode_set", \
                f"Event type '{event_type}' not handled in summary"
