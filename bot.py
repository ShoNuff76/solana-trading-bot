print("🧪 DEBUG: Script started")  # ← EARLY DEBUG

import os
import ccxt
import time

print("🚀 Bot is starting...")  # ← Confirm we're past imports

try:
    print(f"KRAKEN_API_KEY exists? {'KRAKEN_API_KEY' in os.environ}")
    print(f"KRAKEN_API_SECRET exists? {'KRAKEN_API_SECRET' in os.environ}")
except Exception as e:
    print(f"❌ CRASHED EARLY: {e}")
