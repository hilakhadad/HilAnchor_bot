# Deployment Guide

> **Note**: This guide is in English. For Hebrew documentation, see [README.md](README.md).

## Upload to GitHub

### 1. Create a new repository on GitHub
1. Go to https://github.com/new
2. Repository name: `HilAnchor_bot` (or any name you prefer)
3. Choose **Private** (recommended - contains personal bot configuration)
4. **DO NOT** initialize with README, .gitignore, or license (we already have them)
5. Click "Create repository"

### 2. Push your code to GitHub
```bash
cd c:\Users\hilak\HilAnchor_bot

# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/HilAnchor_bot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Verify the upload
- Go to your GitHub repository
- Verify all files are there
- **IMPORTANT**: Check that `.env` is NOT uploaded (only `.env.example` should be visible)

---

## Deploy to Remote Server

### Option 1: Linux Server (Recommended for 24/7 operation)

#### 1. Clone the repository on the server
```bash
# SSH into your server
ssh user@your-server.com

# Clone the repository
git clone https://github.com/YOUR_USERNAME/HilAnchor_bot.git
cd HilAnchor_bot
```

#### 2. Install Python and dependencies
```bash
# Install Python 3.9+ if not already installed
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure environment variables
```bash
# Copy the example env file
cp .env.example .env

# Edit with your credentials
nano .env
```

Add your bot token and user ID:
```env
BOT_TOKEN=your_actual_bot_token
OWNER_USER_ID=your_actual_telegram_user_id
```

#### 4. Test the bot
```bash
python run.py
```

Press `Ctrl+C` to stop when you verify it works.

#### 5. Run as a background service using systemd

Create a systemd service file:
```bash
sudo nano /etc/systemd/system/hilanchor.service
```

Add the following content (adjust paths and username):
```ini
[Unit]
Description=HilAnchor Telegram Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/HilAnchor_bot
Environment="PATH=/home/YOUR_USERNAME/HilAnchor_bot/.venv/bin"
ExecStart=/home/YOUR_USERNAME/HilAnchor_bot/.venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable hilanchor

# Start the service
sudo systemctl start hilanchor

# Check status
sudo systemctl status hilanchor

# View logs
sudo journalctl -u hilanchor -f
```

Service management commands:
```bash
# Stop the bot
sudo systemctl stop hilanchor

# Restart the bot
sudo systemctl restart hilanchor

# Check if running
sudo systemctl status hilanchor
```

---

### Option 2: Screen/tmux (Alternative method)

If you don't have systemd access, you can use `screen` or `tmux`:

```bash
# Install screen
sudo apt install screen

# Start a new screen session
screen -S hilanchor

# Activate venv and run bot
source .venv/bin/activate
python run.py

# Detach from screen: Press Ctrl+A, then D

# Re-attach to screen later
screen -r hilanchor

# List all screen sessions
screen -ls
```

---

### Option 3: Docker (Advanced)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  hilanchor:
    build: .
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./state.json:/app/state.json
      - ./personal_journal.txt:/app/personal_journal.txt
```

Run with Docker:
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Updating the Bot on Server

When you make changes and want to update the server:

```bash
# On your local machine - commit and push changes
git add .
git commit -m "Description of changes"
git push

# On the server - pull and restart
cd HilAnchor_bot
git pull

# If using systemd
sudo systemctl restart hilanchor

# If using screen
screen -r hilanchor
# Press Ctrl+C to stop
python run.py
# Press Ctrl+A, then D to detach
```

---

## Security Best Practices

1. **Never commit `.env` file** - It contains your bot token
2. **Use private repository** - Especially if you customize messages
3. **Restrict server access** - Use SSH keys, disable password auth
4. **Keep dependencies updated** - Run `pip install --upgrade -r requirements.txt` regularly
5. **Monitor logs** - Check for unusual activity

---

## Troubleshooting

### Bot not responding
```bash
# Check if bot is running
sudo systemctl status hilanchor

# Check logs
sudo journalctl -u hilanchor -n 50

# Restart
sudo systemctl restart hilanchor
```

### "Module not found" errors
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Permission errors
```bash
# Make sure the user has permissions
sudo chown -R YOUR_USERNAME:YOUR_USERNAME /home/YOUR_USERNAME/HilAnchor_bot
```

---

## Monitoring

### Check bot uptime
```bash
# See when the service started
sudo systemctl status hilanchor | grep "Active:"
```

### View recent logs
```bash
# Last 100 lines
sudo journalctl -u hilanchor -n 100

# Follow logs in real-time
sudo journalctl -u hilanchor -f

# Logs from today
sudo journalctl -u hilanchor --since today
```

### Check if bot is using too much CPU/Memory
```bash
# See resource usage
top -p $(pgrep -f "python run.py")
```

---

## Backup Strategy

Important files to backup:
- `state.json` - Daily progress data
- `personal_journal.txt` - Personal journal entries
- `.env` - Configuration (keep secure)

Backup script example:
```bash
#!/bin/bash
BACKUP_DIR="$HOME/hilanchor_backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"
cd /home/YOUR_USERNAME/HilAnchor_bot

tar -czf "$BACKUP_DIR/hilanchor_$DATE.tar.gz" \
    state.json \
    personal_journal.txt \
    .env

# Keep only last 30 days of backups
find "$BACKUP_DIR" -name "hilanchor_*.tar.gz" -mtime +30 -delete
```

Add to crontab for daily backups:
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * /home/YOUR_USERNAME/backup_hilanchor.sh
```
