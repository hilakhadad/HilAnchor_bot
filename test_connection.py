"""Test script to diagnose Telegram API connectivity issues."""
import os
import sys
from dotenv import load_dotenv

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN not found in .env file")
    sys.exit(1)

print(f"✓ Bot token loaded (starts with: {BOT_TOKEN[:10]}...)")
print("\n🔍 Testing connectivity to Telegram API...")

# Test 1: Basic HTTP connectivity
print("\n1️⃣ Testing basic HTTPS connectivity...")
try:
    import httpx
    response = httpx.get("https://api.telegram.org", timeout=10.0)
    print(f"   ✓ Telegram API is reachable (status: {response.status_code})")
except Exception as e:
    print(f"   ❌ Cannot reach Telegram API: {e}")
    print("\n💡 Possible solutions:")
    print("   - Check your internet connection")
    print("   - Check if a firewall is blocking access")
    print("   - Try using a VPN or proxy")
    sys.exit(1)

# Test 2: Validate bot token
print("\n2️⃣ Testing bot token validity...")
try:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    response = httpx.get(url, timeout=10.0)
    data = response.json()

    if response.status_code == 200 and data.get("ok"):
        bot_info = data.get("result", {})
        print(f"   ✓ Bot token is VALID")
        print(f"   ✓ Bot username: @{bot_info.get('username')}")
        print(f"   ✓ Bot name: {bot_info.get('first_name')}")
        print(f"   ✓ Bot ID: {bot_info.get('id')}")
    else:
        print(f"   ❌ Bot token is INVALID")
        print(f"   Response: {data}")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Error validating token: {e}")
    sys.exit(1)

print("\n✅ All connectivity tests passed!")
print("Your bot should work. If run.py still fails, try:")
print("   - Restart your terminal/IDE")
print("   - Check Windows Firewall settings")
print("   - Temporarily disable antivirus")
