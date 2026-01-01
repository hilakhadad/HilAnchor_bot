import json
import datetime as dt
from pathlib import Path
from typing import Any, Dict, Optional, Set

from .config import STATE_PATH

_STATE_PATH = Path(STATE_PATH)


def today_key() -> str:
    return dt.date.today().isoformat()


def load_state() -> Dict[str, Any]:
    if not _STATE_PATH.exists():
        return {}
    try:
        return json.loads(_STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state: Dict[str, Any]) -> None:
    _STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print("DEBUG saving to:", _STATE_PATH.resolve())


def day_state(state: Dict[str, Any]) -> Dict[str, Any]:
    k = today_key()
    state.setdefault(k, {})
    return state[k]


def set_waiting(state: Dict[str, Any], waiting_for: str) -> None:
    d = day_state(state)
    d["waiting_for"] = waiting_for
    save_state(state)


def clear_waiting(state: Dict[str, Any]) -> None:
    d = day_state(state)
    if "waiting_for" in d:
        del d["waiting_for"]
    save_state(state)


def get_waiting(state: Dict[str, Any]) -> Optional[str]:
    return state.get(today_key(), {}).get("waiting_for")


def set_mode(state: Dict[str, Any], mode: str) -> None:
    d = day_state(state)
    d["mode"] = mode
    save_state(state)


def get_mode(state: Dict[str, Any]) -> str:
    return state.get(today_key(), {}).get("mode", "work")


def mark_done(state: Dict[str, Any], done: bool = True) -> None:
    d = day_state(state)
    d["done"] = bool(done)
    save_state(state)


def is_done(state: Dict[str, Any]) -> bool:
    return bool(state.get(today_key(), {}).get("done", False))


def set_need_followup(state: Dict[str, Any], need: bool) -> None:
    d = day_state(state)
    d["need_followup"] = bool(need)
    save_state(state)


def need_followup(state: Dict[str, Any]) -> bool:
    return bool(state.get(today_key(), {}).get("need_followup", True))


def bump_fail(state: Dict[str, Any]) -> int:
    d = day_state(state)
    d["fail_count"] = int(d.get("fail_count", 0)) + 1
    save_state(state)
    return d["fail_count"]


def reset_fail(state: Dict[str, Any]) -> None:
    d = day_state(state)
    d["fail_count"] = 0
    save_state(state)


def set_last_plan(state: Dict[str, Any], text: str) -> None:
    d = day_state(state)
    d["plan"] = text
    d["plan_ts"] = dt.datetime.now().isoformat(timespec="seconds")
    save_state(state)


def set_worked(state: Dict[str, Any], worked: str) -> None:
    d = day_state(state)
    d["worked"] = worked
    d["worked_ts"] = dt.datetime.now().isoformat(timespec="seconds")
    save_state(state)

def _notified_set(state: Dict[str, Any]) -> Set[str]:
    state.setdefault("notified_non_owner_user_ids", [])
    return set(str(x) for x in state["notified_non_owner_user_ids"])

def has_notified_non_owner(state: Dict[str, Any], user_id: int) -> bool:
    return str(user_id) in _notified_set(state)

def mark_notified_non_owner(state: Dict[str, Any], user_id: int) -> None:
    s = _notified_set(state)
    s.add(str(user_id))
    state["notified_non_owner_user_ids"] = sorted(s)
    save_state(state)

def set_context(state, context: str):
    state.setdefault("context", context)
    save_state(state)

def append_event(state: Dict[str, Any], event_type: str, value: Any = None, text: Optional[str] = None) -> None:
    d = day_state(state)

    ev: Dict[str, Any] = {
        "ts": dt.datetime.now().isoformat(timespec="seconds"),
        "type": event_type,
    }
    if value is not None:
        ev["value"] = value
    if text is not None:
        ev["text"] = text

    d.setdefault("events", []).append(ev)
    save_state(state)