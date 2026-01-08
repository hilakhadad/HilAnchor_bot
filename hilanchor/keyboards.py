from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from . import messages as msg

def kb_day_mode() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(msg.BTN_KID_MODE, callback_data="on_mode_choice:kid"),
            InlineKeyboardButton(msg.BTN_WORK_MODE, callback_data="on_mode_choice:work"),
        ]
    ])


def kb_worked() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(msg.BTN_WORKED_YES, callback_data="worked:yes"),
            InlineKeyboardButton(msg.BTN_WORKED_PARTIAL, callback_data="worked:partial"),
            InlineKeyboardButton(msg.BTN_WORKED_NO, callback_data="worked:no"),
        ]
    ])


def kb_no_reason() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(msg.BTN_REASON_BIG, callback_data="noreason:big")],
        [InlineKeyboardButton(msg.BTN_REASON_STUCK, callback_data="noreason:stuck")],
        [InlineKeyboardButton(msg.BTN_REASON_FEAR, callback_data="noreason:fear")],
    ])


def kb_yes_next() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(msg.BTN_CONTINUE, callback_data="yesnext:continue"),
            InlineKeyboardButton(msg.BTN_CLOSE, callback_data="yesnext:close"),
        ],
        [
            InlineKeyboardButton(msg.BTN_IN_FLOW, callback_data="yesnext:flow"),
        ]
    ])


def kb_big_action() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(msg.BTN_BIG_DO2, callback_data="bigaction:do2"),
            InlineKeyboardButton(msg.BTN_BIG_SKIP, callback_data="bigaction:skip"),
        ]
    ])


def kb_nudge_progress() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(msg.BTN_WORKED_YES, callback_data="nudge:yes"),
            InlineKeyboardButton(msg.BTN_WORKED_PARTIAL, callback_data="nudge:partial"),
            InlineKeyboardButton(msg.BTN_WORKED_NO, callback_data="nudge:no"),
        ]
    ])
