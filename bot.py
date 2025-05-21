import os

# DEBUG TEST - show raw environment keys before any imports
print("🚨 DEBUG: Raw environment keys check")
print(f"KRAKEN_API_KEY: {repr(os.getenv('KRAKEN_API_KEY'))}")
print(f"KRAKEN_API_SECRET: {repr(os.getenv('KRAKEN_API_SECRET'))}")

import ccxt
import time

print("🚀 Bot is starting...")

# === SET UP KRAKEN CONNECTION ===
try:
    kraken = ccxt.kraken({
        'apiKey': os.getenv('KRAKEN_API_KEY'),
        'secret': os.getenv('KRAKEN_API_SECRET'),
        'enableRateLimit': True
    })
    print("✅ Kraken connection initialized.")
except Exception as e:
    print(f"❌ Failed to initialize Kraken: {e}")
    raise SystemExit

# Don't continue — this is a debug version
raise SystemExit("🧪 Debug complete. Awaiting next instruction.")
