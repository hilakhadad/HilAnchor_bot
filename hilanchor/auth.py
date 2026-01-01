from telegram import Update
from telegram.ext import ContextTypes

from .config import OWNER_USER_ID_INT
from .state_store import load_state, has_notified_non_owner, mark_notified_non_owner


def is_owner(update: Update) -> bool:
    return (
        update.effective_user is not None
        and update.effective_user.id == OWNER_USER_ID_INT
    )


async def reject_non_owner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if is_owner(update):
        return False

    user = update.effective_user
    if not user:
        return True

    state = load_state()
    if has_notified_non_owner(state, user.id):
        # Silent ignore after the first time
        return True

    msg = "היי 🙂 זה בוט פרטי שנבנה לצרכים אישיים, אז הוא לא פעיל עבורך."
    mark_notified_non_owner(state, user.id)

    if update.message:
        await update.message.reply_text(msg)
    elif update.callback_query:
        await update.callback_query.answer("בוט פרטי 🙂", show_alert=True)
        try:
            await update.callback_query.edit_message_text(msg)
        except Exception:
            pass

    return True
