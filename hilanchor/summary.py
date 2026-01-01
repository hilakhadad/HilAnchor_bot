"""
Daily summary generation from state
"""
import datetime as dt
from typing import Dict, Any, List
from .state_store import load_state, today_key
from . import messages as msg


def generate_daily_summary() -> str:
    """Generate a human-readable summary of today's activities."""
    state = load_state()
    today = today_key()

    if today not in state:
        return msg.SUMMARY_NO_DATA

    day_data = state[today]

    # Build summary
    lines = [msg.SUMMARY_HEADER, ""]

    # Mode
    mode = day_data.get("mode", "work")
    if mode == "kid":
        lines.append(msg.SUMMARY_MODE_KID)
    else:
        lines.append(msg.SUMMARY_MODE_WORK)

    lines.append("")

    # Work status
    worked = day_data.get("worked")
    if worked:
        if worked == "yes":
            lines.append(msg.SUMMARY_WORKED_YES)
        elif worked == "partial":
            lines.append(msg.SUMMARY_WORKED_PARTIAL)
        else:
            lines.append(msg.SUMMARY_WORKED_NO)

    # Events
    events = day_data.get("events", [])
    if events:
        lines.append("")
        lines.append(msg.SUMMARY_EVENTS_HEADER)
        for event in events:
            event_type = event.get("type")
            value = event.get("value")
            text = event.get("text")
            timestamp = event.get("ts", "")

            time_str = ""
            if timestamp:
                try:
                    ts = dt.datetime.fromisoformat(timestamp)
                    time_str = ts.strftime("%H:%M")
                except:
                    pass

            if event_type == "checkin_answer":
                if value == "yes":
                    lines.append(f"  • {time_str} ✅ ענית שעבדת")
                elif value == "partial":
                    lines.append(f"  • {time_str} 🤏 ענית שעבדת חלקית")
                else:
                    lines.append(f"  • {time_str} ❌ ענית שלא עבדת")

            elif event_type == "did" and text:
                lines.append(f"  • {time_str} 💪 מה עשית: {text}")

            elif event_type == "plan" and text:
                lines.append(f"  • {time_str} 📋 תכנית: {text}")

            elif event_type == "first_action" and text:
                lines.append(f"  • {time_str} 🚀 פעולה ראשונה: {text}")

            elif event_type == "fear_reframe" and text:
                lines.append(f"  • {time_str} 💙 שינוי מסגור של פחד: {text}")

            elif event_type == "bullets" and text:
                lines.append(f"  • {time_str} 📌 3 נקודות: {text}")

            elif event_type == "context":
                if value == "overwhelmed":
                    lines.append(f"  • {time_str} 😰 הרגשת המום/ה - המשימה גדולה מדי")
                elif value == "stuck":
                    lines.append(f"  • {time_str} 🤔 הרגשת תקוע/ה - לא ידעת איך להתחיל")
                elif value == "fear":
                    lines.append(f"  • {time_str} 😨 פחד מכשלון")

            elif event_type == "big_action" and value == "do2":
                lines.append(f"  • {time_str} ⏱️ הסכמת למשימת 2 דקות")

            elif event_type == "nudge_scheduled" and value:
                lines.append(f"  • {time_str} ⏰ תזכורת נקבעה ל-{value} דקות")

            elif event_type == "closed" and value:
                lines.append(f"  • {time_str} 🏁 סגרת את היום")

            elif event_type == "continue" and value:
                lines.append(f"  • {time_str} ▶️ בחרת להמשיך")

            elif event_type == "mode_set":
                pass  # Already shown at top

            elif event_type == "free_note" and text:
                # Free text notes from user
                lines.append(f"  • {time_str} 💭 הערה: {text}")

    # Plan
    plan = day_data.get("plan")
    if plan:
        lines.append("")
        lines.append(f"{msg.SUMMARY_LAST_PLAN} {plan}")

    # Done status
    done = day_data.get("done", False)
    lines.append("")
    if done:
        lines.append(msg.SUMMARY_DAY_DONE)
    else:
        lines.append(msg.SUMMARY_DAY_OPEN)

    # Fail count (internal tracking)
    fail_count = day_data.get("fail_count", 0)
    if fail_count > 0:
        lines.append(f"⚠️ נסיונות כושלים: {fail_count}")

    return "\n".join(lines)


def get_raw_state_for_day(date_str: str = None) -> Dict[str, Any]:
    """Get the raw state data for a specific day (for advanced users)."""
    state = load_state()
    day_key = date_str or today_key()
    return state.get(day_key, {})
