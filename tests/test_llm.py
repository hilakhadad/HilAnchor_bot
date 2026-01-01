"""
Test script for LLM integration
"""
from hilanchor.llm import test_ollama_connection, humanize_message, humanize_checkin, humanize_nudge

print("=" * 50)
print("Testing Ollama Connection...")
print("=" * 50)

if test_ollama_connection():
    print("✅ Ollama is working!\n")

    print("=" * 50)
    print("Testing Message Humanization...")
    print("=" * 50)

    # Test simple message
    original = "עבדת היום?"
    humanized = humanize_message(original)
    print(f"\nOriginal: {original}")
    print(f"Humanized: {humanized}\n")

    # Test check-in messages
    print("=" * 50)
    print("Testing Check-in Messages...")
    print("=" * 50)

    for stage in ["11", "14", "17"]:
        msg = humanize_checkin(stage)
        print(f"\nStage {stage}:00")
        print(msg)
        print()

    # Test nudge messages
    print("=" * 50)
    print("Testing Nudge Messages...")
    print("=" * 50)

    for minutes in [5, 10, 30]:
        msg = humanize_nudge(minutes)
        print(f"\nNudge after {minutes} minutes:")
        print(msg)
        print()

else:
    print("❌ Ollama is not working.")
    print("\n📋 To fix this:")
    print("1. Make sure Ollama is installed and running")
    print("2. Install the model: ollama pull llama3.2:3b")
    print("3. Or change LLM_MODEL in .env to a model you have")
