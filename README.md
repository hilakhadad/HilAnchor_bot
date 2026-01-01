# HilAnchor Bot 🙂

A personal Telegram bot for gentle daily progress tracking.

**English** | [עברית](README_HE.md)

## Key Features

- ✅ **Daily Tracking** - Automatic check-ins at 11:00, 14:00, 17:00
- 📊 **Daily Summaries** - Summary of all activities and progress
- 📓 **Personal Journal** - Save private thoughts and feelings
- 💬 **Free Text** - Send thoughts anytime
- 🎯 **Supportive Coaching** - Help breaking down large tasks and tracking progress
- 🔒 **Full Privacy** - Bot is limited to a single user (OWNER_USER_ID)

## Development Environment

- **Python**: 3.9.7
- **Operating System**: Windows
- **Main Libraries**:
  - `python-telegram-bot` - Telegram API interface
  - `httpx` - HTTP requests (proxy support)
  - `python-dotenv` - Environment variable management
  - `pytz` - Timezone management
  - `ollama` - LLM integration (optional)

## Installation

### 1. Clone the project
```bash
git clone https://github.com/YOUR_USERNAME/HilAnchor_bot.git
cd HilAnchor_bot
```

### 2. Create virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure .env file
Create a `.env` file in the project directory:

```env
# Required - Basic Configuration
BOT_TOKEN=your_telegram_bot_token_here
OWNER_USER_ID=your_telegram_user_id_here

# Optional - Custom paths (defaults shown)
STATE_PATH=state.json
JOURNAL_PATH=personal_journal.txt

# Optional - LLM Integration (Ollama)
USE_LLM=false
LLM_MODEL=llama3.2:3b

# Optional - Proxy Configuration
# PROXY_URL=http://your-proxy:port
# PROXY_URL=socks5://your-proxy:port
```

#### How to get BOT_TOKEN?
1. Open chat with [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and answer the questions
3. Copy the TOKEN you receive

#### How to get OWNER_USER_ID?
1. Open chat with [@userinfobot](https://t.me/userinfobot)
2. The bot will send you your ID

### 5. Run the bot
```bash
python run.py
```

## Available Commands

- `/start` - Start the bot and select day mode
- `/checkin` - Manual check-in
- `/summary` - Summary of the day so far
- `/journal` - Read personal journal
- `/journal_add` - Add entry to personal journal
- `/journal_info` - Journal statistics

## Creating EXE File

### Install PyInstaller
```bash
pip install pyinstaller
```

### Create EXE with icon
```bash
pyinstaller --onefile --icon=handshake.ico --name=HilAnchor run.py
```

#### Parameters:
- `--onefile` - Creates a single EXE file
- `--noconsole` - Hides console window (optional, depends if you want to see logs)
- `--icon=handshake.ico` - Sets the EXE icon
- `--name=HilAnchor` - Final file name

The file will be saved in `dist\HilAnchor.exe`

### Important Notes:
1. **.env file**: Copy the `.env` file to the same directory as the EXE
2. **State files**: `state.json` and `personal_journal.txt` will be created automatically
3. **Ollama** (if USE_LLM=true): Must be installed and running on the machine

## Project Structure

```
HilAnchor_bot/
├── run.py                    # Main entry point
├── handshake.ico            # Bot icon
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
├── state.json              # Bot state (created automatically)
├── personal_journal.txt    # Personal journal (created automatically)
└── hilanchor/
    ├── __init__.py
    ├── config.py           # Configuration and environment variables
    ├── auth.py             # User authentication
    ├── state_store.py      # Bot state management
    ├── keyboards.py        # Interactive keyboards
    ├── messages.py         # All bot messages
    ├── scheduler.py        # Scheduled tasks
    ├── summary.py          # Summary generation
    ├── journal.py          # Personal journal management
    ├── llm.py             # LLM integration
    ├── nudges.py          # Reminders
    ├── services/
    │   └── flow.py        # Bot flow logic
    └── handlers/
        ├── __init__.py
        ├── commands.py    # Command handlers
        ├── free_text.py   # Free text handler
        ├── patterns.py    # Callback patterns
        └── callbacks/     # Button handlers
            ├── mode.py
            ├── worked.py
            ├── noreason.py
            ├── bigaction.py
            ├── yesnext.py
            └── nudge.py
```

## Proxy Configuration

If your network blocks Telegram, you can configure a proxy in `.env`:

```env
# HTTP Proxy
PROXY_URL=http://your-proxy-server:port

# OR SOCKS5 Proxy
PROXY_URL=socks5://your-proxy-server:port
```

## Common Troubleshooting

### Bot not responding
- Verify BOT_TOKEN is correct
- Check internet connection
- If Telegram is blocked, try configuring a proxy

### OWNER_USER_ID error
- Ensure you entered a valid number (digits only)
- Verify you received the correct ID from @userinfobot

### LLM not working
- Verify Ollama is installed and running (`ollama serve`)
- Check the model exists (`ollama list`)
- If you don't need LLM, leave `USE_LLM=false`

## Deployment

For detailed deployment instructions to remote servers, see [DEPLOYMENT.md](DEPLOYMENT.md).

Quick start for Linux server:

```bash
git clone https://github.com/YOUR_USERNAME/HilAnchor_bot.git
cd HilAnchor_bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env  # Add your BOT_TOKEN and OWNER_USER_ID
python run.py
```

## License

Private project for personal use.

## Contact

For questions and issues, please contact the project developer.
