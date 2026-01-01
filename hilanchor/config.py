import os
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_USER_ID = os.getenv("OWNER_USER_ID")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env")

if not OWNER_USER_ID or not OWNER_USER_ID.isdigit():
    raise ValueError("OWNER_USER_ID is not set or invalid in .env")

OWNER_USER_ID_INT = int(OWNER_USER_ID)
OWNER_CHAT_ID_INT = OWNER_USER_ID_INT  # assuming chat ID is same as user ID for private chats

STATE_PATH = os.getenv("STATE_PATH", "state.json")
JOURNAL_PATH = os.getenv("JOURNAL_PATH", "personal_journal.txt")

# LLM Configuration - DISABLED by default (set USE_LLM=true in .env to enable)
USE_LLM = os.getenv("USE_LLM", "false").lower() in ("true", "1", "yes")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")

# Proxy Configuration - Optional (for networks that block Telegram)
# Set in .env: PROXY_URL=http://your-proxy:port or socks5://your-proxy:port
PROXY_URL = os.getenv("PROXY_URL", None)
