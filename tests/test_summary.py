"""
Test script for summary functionality
"""
from hilanchor.summary import generate_daily_summary
from hilanchor.state_store import load_state, today_key

# Print current state
print("=" * 60)
print("Current state for today:")
print("=" * 60)

state = load_state()
today = today_key()

if today in state:
    import json
    print(json.dumps(state[today], indent=2, ensure_ascii=False))
else:
    print("No data for today yet.")

print("\n" + "=" * 60)
print("Daily Summary:")
print("=" * 60)

summary = generate_daily_summary()
print(summary)
