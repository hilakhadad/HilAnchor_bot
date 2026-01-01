import logging
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters, ApplicationBuilder

from hilanchor.handlers import (
    start, checkin, summary, journal, journal_add, journal_info, on_free_text,
    on_mode_choice, on_worked_choice, on_no_reason, on_big_action, on_yes_next, on_nudge_progress,
    CB_MODE_PATTERN, CB_WORKED_PATTERN, CB_NO_REASON_PATTERN, CB_BIG_ACTION_PATTERN, CB_YES_NEXT_PATTERN, CB_NUDGE_PROGRESS_PATTERN
)
from hilanchor.config import BOT_TOKEN, PROXY_URL
from hilanchor.scheduler import register_jobs
import httpx

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

logger.info("🚀 Initializing HilAnchor bot...")

# Configure proxy if needed
builder = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .connect_timeout(30.0)
    .read_timeout(30.0)
    .write_timeout(30.0)
    .pool_timeout(30.0)
    .get_updates_connect_timeout(30.0)
    .get_updates_read_timeout(30.0)
)

if PROXY_URL:
    logger.info(f"🌐 Using proxy: {PROXY_URL}")
    # Create httpx client with proxy support
    proxy_client = httpx.AsyncClient(proxy=PROXY_URL, timeout=30.0)
    builder = builder.get_updates_http_version("1.1").http_version("1.1")
    from telegram.request import HTTPXRequest
    builder = builder.request(HTTPXRequest(http_version="1.1", proxy=PROXY_URL))
else:
    logger.info("🌐 No proxy configured - connecting directly to Telegram")

app = builder.build()

logger.info("📝 Registering command handlers...")
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("checkin", checkin))
app.add_handler(CommandHandler("summary", summary))
app.add_handler(CommandHandler("journal", journal))
app.add_handler(CommandHandler("journal_add", journal_add))
app.add_handler(CommandHandler("journal_info", journal_info))

logger.info("🔘 Registering callback handlers...")
app.add_handler(CallbackQueryHandler(on_mode_choice, pattern=CB_MODE_PATTERN))
app.add_handler(CallbackQueryHandler(on_worked_choice, pattern=CB_WORKED_PATTERN))
app.add_handler(CallbackQueryHandler(on_no_reason, pattern=CB_NO_REASON_PATTERN))
app.add_handler(CallbackQueryHandler(on_big_action, pattern=CB_BIG_ACTION_PATTERN))
app.add_handler(CallbackQueryHandler(on_yes_next, pattern=CB_YES_NEXT_PATTERN))
app.add_handler(CallbackQueryHandler(on_nudge_progress, pattern=CB_NUDGE_PROGRESS_PATTERN))

logger.info("💬 Registering message handlers...")
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_free_text))

logger.info("⏰ Registering scheduled jobs...")
register_jobs(app)

logger.info("✅ HilAnchor bot is running and listening for messages...")
print("🤖 HilAnchor bot is running...")

# Run polling with proper initialization settings
app.run_polling(
    drop_pending_updates=True,
    allowed_updates=["message", "callback_query"]
)
