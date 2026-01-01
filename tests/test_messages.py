"""
Tests for all bot messages and message-related functionality.
These tests ensure that messages are properly configured and accessible.
"""
import pytest
from hilanchor import messages as msg


class TestCommandMessages:
    """Test command-related messages."""

    def test_start_message_exists(self):
        assert msg.START_MESSAGE
        assert "HilAnchor" in msg.START_MESSAGE
        assert "/checkin" in msg.START_MESSAGE
        assert "/summary" in msg.START_MESSAGE

    def test_start_mode_question_exists(self):
        assert msg.START_MODE_QUESTION
        assert len(msg.START_MODE_QUESTION) > 0

    def test_checkin_manual_exists(self):
        assert msg.CHECKIN_MANUAL
        assert "עבדת" in msg.CHECKIN_MANUAL


class TestScheduledMessages:
    """Test scheduled message texts."""

    def test_morning_11_exists(self):
        assert msg.MORNING_11
        assert len(msg.MORNING_11) > 0

    def test_checkin_11_exists(self):
        assert msg.CHECKIN_11
        assert "עבדת" in msg.CHECKIN_11

    def test_checkin_14_exists(self):
        assert msg.CHECKIN_14
        assert "עבדת" in msg.CHECKIN_14

    def test_checkin_17_exists(self):
        assert msg.CHECKIN_17
        assert "עבדת" in msg.CHECKIN_17


class TestModeMessages:
    """Test mode selection messages."""

    def test_mode_kid_confirmed_exists(self):
        assert msg.MODE_KID_CONFIRMED
        assert "בת" in msg.MODE_KID_CONFIRMED or "אלה" in msg.MODE_KID_CONFIRMED

    def test_mode_work_confirmed_exists(self):
        assert msg.MODE_WORK_CONFIRMED
        assert len(msg.MODE_WORK_CONFIRMED) > 0

    def test_mode_first_checkin_exists(self):
        assert msg.MODE_FIRST_CHECKIN
        assert "עבדת" in msg.MODE_FIRST_CHECKIN


class TestWorkedResponses:
    """Test 'worked' response messages."""

    def test_worked_yes_exists(self):
        assert msg.WORKED_YES
        assert len(msg.WORKED_YES) > 0

    def test_worked_partial_exists(self):
        assert msg.WORKED_PARTIAL
        assert len(msg.WORKED_PARTIAL) > 0

    def test_worked_no_exists(self):
        assert msg.WORKED_NO
        assert len(msg.WORKED_NO) > 0


class TestReasonMessages:
    """Test reason (for not working) messages."""

    def test_reason_big_exists(self):
        assert msg.REASON_BIG
        assert len(msg.REASON_BIG) > 0

    def test_reason_stuck_exists(self):
        assert msg.REASON_STUCK
        assert len(msg.REASON_STUCK) > 0

    def test_reason_fear_exists(self):
        assert msg.REASON_FEAR
        assert len(msg.REASON_FEAR) > 0


class TestBigActionMessages:
    """Test big action breakdown messages."""

    def test_big_action_skip_exists(self):
        assert msg.BIG_ACTION_SKIP
        assert len(msg.BIG_ACTION_SKIP) > 0

    def test_big_action_do_exists(self):
        assert msg.BIG_ACTION_DO
        assert len(msg.BIG_ACTION_DO) > 0


class TestYesNextMessages:
    """Test continue/close messages."""

    def test_yes_what_did_received_exists(self):
        assert msg.YES_WHAT_DID_RECEIVED
        assert len(msg.YES_WHAT_DID_RECEIVED) > 0

    def test_close_for_day_exists(self):
        assert msg.CLOSE_FOR_DAY
        assert len(msg.CLOSE_FOR_DAY) > 0

    def test_continue_30min_exists(self):
        assert msg.CONTINUE_30MIN
        assert len(msg.CONTINUE_30MIN) > 0


class TestPlanFunctions:
    """Test dynamic plan messages (functions)."""

    def test_plan_received_function(self):
        result = msg.plan_received(10)
        assert isinstance(result, str)
        assert "10" in result
        assert len(result) > 0

    def test_plan_received_different_minutes(self):
        result5 = msg.plan_received(5)
        result30 = msg.plan_received(30)
        assert "5" in result5
        assert "30" in result30
        assert result5 != result30

    def test_stuck_received_function(self):
        result = msg.stuck_received(10)
        assert isinstance(result, str)
        assert "10" in result
        assert len(result) > 0

    def test_fear_reframe_received_function(self):
        result = msg.fear_reframe_received(5)
        assert isinstance(result, str)
        assert "5" in result
        assert len(result) > 0


class TestBulletsMessage:
    """Test bullets received message."""

    def test_bullets_received_exists(self):
        assert msg.BULLETS_RECEIVED
        assert len(msg.BULLETS_RECEIVED) > 0


class TestNudgeMessages:
    """Test nudge-related messages."""

    def test_nudge_message_function(self):
        result = msg.nudge_message(15)
        assert isinstance(result, str)
        assert "15" in result
        assert len(result) > 0

    def test_nudge_message_different_times(self):
        result5 = msg.nudge_message(5)
        result30 = msg.nudge_message(30)
        assert "5" in result5
        assert "30" in result30

    def test_nudge_yes_progress_exists(self):
        assert msg.NUDGE_YES_PROGRESS
        assert len(msg.NUDGE_YES_PROGRESS) > 0

    def test_nudge_partial_progress_exists(self):
        assert msg.NUDGE_PARTIAL_PROGRESS
        assert len(msg.NUDGE_PARTIAL_PROGRESS) > 0

    def test_nudge_no_progress_exists(self):
        assert msg.NUDGE_NO_PROGRESS
        assert len(msg.NUDGE_NO_PROGRESS) > 0

    def test_nudge_give_up_exists(self):
        assert msg.NUDGE_GIVE_UP
        assert len(msg.NUDGE_GIVE_UP) > 0


class TestFreeNoteMessages:
    """Test free note messages."""

    def test_free_note_saved_exists(self):
        assert msg.FREE_NOTE_SAVED
        assert len(msg.FREE_NOTE_SAVED) > 0


class TestSummaryMessages:
    """Test summary component messages."""

    def test_summary_no_data_exists(self):
        assert msg.SUMMARY_NO_DATA
        assert "סיכום" in msg.SUMMARY_NO_DATA

    def test_summary_header_exists(self):
        assert msg.SUMMARY_HEADER
        assert "סיכום" in msg.SUMMARY_HEADER

    def test_summary_mode_work_exists(self):
        assert msg.SUMMARY_MODE_WORK
        assert "עבודה" in msg.SUMMARY_MODE_WORK

    def test_summary_mode_kid_exists(self):
        assert msg.SUMMARY_MODE_KID
        assert len(msg.SUMMARY_MODE_KID) > 0

    def test_summary_worked_yes_exists(self):
        assert msg.SUMMARY_WORKED_YES
        assert len(msg.SUMMARY_WORKED_YES) > 0

    def test_summary_worked_partial_exists(self):
        assert msg.SUMMARY_WORKED_PARTIAL
        assert len(msg.SUMMARY_WORKED_PARTIAL) > 0

    def test_summary_worked_no_exists(self):
        assert msg.SUMMARY_WORKED_NO
        assert len(msg.SUMMARY_WORKED_NO) > 0

    def test_summary_events_header_exists(self):
        assert msg.SUMMARY_EVENTS_HEADER
        assert len(msg.SUMMARY_EVENTS_HEADER) > 0

    def test_summary_last_plan_exists(self):
        assert msg.SUMMARY_LAST_PLAN
        assert len(msg.SUMMARY_LAST_PLAN) > 0

    def test_summary_day_done_exists(self):
        assert msg.SUMMARY_DAY_DONE
        assert len(msg.SUMMARY_DAY_DONE) > 0

    def test_summary_day_open_exists(self):
        assert msg.SUMMARY_DAY_OPEN
        assert len(msg.SUMMARY_DAY_OPEN) > 0


class TestButtonLabels:
    """Test button label texts."""

    def test_btn_kid_mode_exists(self):
        assert msg.BTN_KID_MODE
        assert len(msg.BTN_KID_MODE) > 0

    def test_btn_work_mode_exists(self):
        assert msg.BTN_WORK_MODE
        assert len(msg.BTN_WORK_MODE) > 0

    def test_btn_worked_yes_exists(self):
        assert msg.BTN_WORKED_YES
        assert len(msg.BTN_WORKED_YES) > 0

    def test_btn_worked_partial_exists(self):
        assert msg.BTN_WORKED_PARTIAL
        assert len(msg.BTN_WORKED_PARTIAL) > 0

    def test_btn_worked_no_exists(self):
        assert msg.BTN_WORKED_NO
        assert len(msg.BTN_WORKED_NO) > 0

    def test_btn_reason_big_exists(self):
        assert msg.BTN_REASON_BIG
        assert len(msg.BTN_REASON_BIG) > 0

    def test_btn_reason_stuck_exists(self):
        assert msg.BTN_REASON_STUCK
        assert len(msg.BTN_REASON_STUCK) > 0

    def test_btn_reason_fear_exists(self):
        assert msg.BTN_REASON_FEAR
        assert len(msg.BTN_REASON_FEAR) > 0

    def test_btn_big_do2_exists(self):
        assert msg.BTN_BIG_DO2
        assert len(msg.BTN_BIG_DO2) > 0

    def test_btn_big_skip_exists(self):
        assert msg.BTN_BIG_SKIP
        assert len(msg.BTN_BIG_SKIP) > 0

    def test_btn_continue_exists(self):
        assert msg.BTN_CONTINUE
        assert len(msg.BTN_CONTINUE) > 0

    def test_btn_close_exists(self):
        assert msg.BTN_CLOSE
        assert len(msg.BTN_CLOSE) > 0

    def test_btn_continue_10_exists(self):
        assert msg.BTN_CONTINUE_10
        assert len(msg.BTN_CONTINUE_10) > 0


class TestMessageConsistency:
    """Test that messages are consistent and properly formatted."""

    def test_no_empty_messages(self):
        """Ensure no message is an empty string."""
        # Get all string attributes from messages module
        message_attrs = [attr for attr in dir(msg) if not attr.startswith('_')]

        for attr_name in message_attrs:
            attr_value = getattr(msg, attr_name)
            # Only check string attributes (skip functions)
            if isinstance(attr_value, str):
                assert len(attr_value.strip()) > 0, f"{attr_name} is empty or whitespace only"

    def test_dynamic_functions_accept_integers(self):
        """Ensure dynamic message functions accept integer parameters."""
        # Test with various minute values
        for minutes in [1, 5, 10, 15, 30, 60]:
            assert msg.plan_received(minutes)
            assert msg.stuck_received(minutes)
            assert msg.fear_reframe_received(minutes)
            assert msg.nudge_message(minutes)

    def test_button_labels_are_short(self):
        """Ensure button labels are reasonably short for UI."""
        button_labels = [
            msg.BTN_KID_MODE,
            msg.BTN_WORK_MODE,
            msg.BTN_WORKED_YES,
            msg.BTN_WORKED_PARTIAL,
            msg.BTN_WORKED_NO,
            msg.BTN_REASON_BIG,
            msg.BTN_REASON_STUCK,
            msg.BTN_REASON_FEAR,
            msg.BTN_BIG_DO2,
            msg.BTN_BIG_SKIP,
            msg.BTN_CONTINUE,
            msg.BTN_CLOSE,
            msg.BTN_CONTINUE_10,
        ]

        for label in button_labels:
            # Most buttons should be under 30 characters for good UX
            assert len(label) < 50, f"Button label too long: {label}"


class TestHebrewContent:
    """Test that messages contain Hebrew content."""

    def test_messages_contain_hebrew(self):
        """Verify messages contain Hebrew characters."""
        hebrew_range = range(0x0590, 0x05FF)  # Hebrew Unicode block

        test_messages = [
            msg.START_MESSAGE,
            msg.WORKED_YES,
            msg.WORKED_NO,
            msg.REASON_BIG,
            msg.CLOSE_FOR_DAY,
        ]

        for message in test_messages:
            has_hebrew = any(ord(char) in hebrew_range for char in message)
            assert has_hebrew, f"Message doesn't contain Hebrew: {message[:50]}..."
