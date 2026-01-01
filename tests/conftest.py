"""
Pytest configuration and fixtures for HilAnchor bot tests.
"""
import pytest
import os
import sys
from unittest.mock import Mock, MagicMock

# Add parent directory to path so we can import hilanchor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def mock_telegram_update():
    """Create a mock Telegram Update object."""
    update = Mock()
    update.message = Mock()
    update.message.reply_text = Mock()
    update.message.text = "test message"
    update.effective_chat = Mock()
    update.effective_chat.id = 123456789
    update.callback_query = None
    return update


@pytest.fixture
def mock_telegram_callback_query():
    """Create a mock Telegram CallbackQuery object."""
    query = Mock()
    query.answer = Mock()
    query.edit_message_text = Mock()
    query.message = Mock()
    query.message.reply_text = Mock()
    query.message.chat_id = 123456789
    query.data = "test:data"
    return query


@pytest.fixture
def mock_telegram_context():
    """Create a mock Telegram Context object."""
    context = Mock()
    context.bot = Mock()
    context.bot.send_message = Mock()
    context.job_queue = Mock()
    return context


@pytest.fixture
def empty_state():
    """Create an empty state dict."""
    return {}


@pytest.fixture
def today_state():
    """Create a state dict with today's key."""
    from hilanchor.state_store import today_key
    return {
        today_key(): {
            "mode": "work",
            "worked": None,
            "done": False,
            "need_followup": True,
            "waiting_for": None,
            "fail_count": 0,
            "plan": None,
            "plan_ts": None,
            "events": []
        }
    }


@pytest.fixture
def state_with_events():
    """Create a state dict with some events."""
    from hilanchor.state_store import today_key
    from datetime import datetime

    return {
        today_key(): {
            "mode": "work",
            "worked": "yes",
            "done": False,
            "need_followup": False,
            "events": [
                {
                    "type": "mode_set",
                    "value": "work",
                    "ts": datetime.now().isoformat()
                },
                {
                    "type": "checkin_answer",
                    "value": "yes",
                    "ts": datetime.now().isoformat()
                },
                {
                    "type": "did",
                    "text": "Worked on feature X",
                    "ts": datetime.now().isoformat()
                }
            ]
        }
    }


@pytest.fixture(autouse=True)
def reset_config():
    """Reset config values before each test."""
    # This ensures each test starts with clean config
    yield
    # Cleanup after test if needed
