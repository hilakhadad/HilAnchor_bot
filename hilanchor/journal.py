"""Personal journal management for tracking thoughts, reflections, and work notes."""

import logging
from datetime import datetime
from pathlib import Path
from .config import JOURNAL_PATH

logger = logging.getLogger(__name__)


def ensure_journal_exists() -> None:
    """Create journal file if it doesn't exist."""
    journal_file = Path(JOURNAL_PATH)
    if not journal_file.exists():
        logger.info(f"📓 Creating new journal file at {JOURNAL_PATH}")
        journal_file.touch()


def read_journal() -> str:
    """Read the entire journal content."""
    ensure_journal_exists()
    journal_file = Path(JOURNAL_PATH)

    try:
        content = journal_file.read_text(encoding="utf-8")
        logger.info(f"📖 Read journal file ({len(content)} characters)")
        return content if content.strip() else "היומן שלך ריק כרגע 📝"
    except Exception as e:
        logger.error(f"❌ Error reading journal: {e}")
        return f"שגיאה בקריאת היומן: {e}"


def append_to_journal(text: str, include_timestamp: bool = True) -> bool:
    """
    Append text to the journal.

    Args:
        text: The text to append
        include_timestamp: Whether to add a timestamp before the text

    Returns:
        True if successful, False otherwise
    """
    ensure_journal_exists()
    journal_file = Path(JOURNAL_PATH)

    try:
        with journal_file.open("a", encoding="utf-8") as f:
            if include_timestamp:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                f.write(f"\n[{timestamp}]\n")

            f.write(f"{text}\n")

        logger.info(f"✍️ Appended {len(text)} characters to journal")
        return True
    except Exception as e:
        logger.error(f"❌ Error writing to journal: {e}")
        return False


def get_journal_summary() -> str:
    """Get a summary of the journal (line count, size, etc.)."""
    ensure_journal_exists()
    journal_file = Path(JOURNAL_PATH)

    try:
        content = journal_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]
        size_kb = journal_file.stat().st_size / 1024

        return (
            f"📊 סטטיסטיקת היומן:\n"
            f"• {len(non_empty_lines)} שורות\n"
            f"• {len(content)} תווים\n"
            f"• {size_kb:.2f} KB\n"
            f"• נתיב: {JOURNAL_PATH}"
        )
    except Exception as e:
        logger.error(f"❌ Error getting journal summary: {e}")
        return f"שגיאה בקבלת סטטיסטיקות: {e}"
