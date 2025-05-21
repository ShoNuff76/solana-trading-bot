import os
import time
import ccxt

print("🧪 DEBUG: Script has started")

api_key = os.getenv("KRAKEN_API_KEY")
api_secret = os.getenv("KRAKEN_API_SECRET")

print(f"KRAKEN_API_KEY exists? {'Yes' if api_key else 'No'}")
print(f"KRAKEN_API_SECRET exists? {'Yes' if api_secret else 'No'}")

print("⚙️ Attempting Kraken init...")
try:
    kraken = ccxt.kraken({
        'apiKey': api_key,
        'secret': api_secret,
        'enableRateLimit': True
    })
    print("✅ Kraken initialized")
except Exception as e:
    print(f"❌ Kraken init failed: {e}")
    raise SystemExit

print("🔁 Starting loop...")

while True:
    print("📊 Still running...")
    time.sleep(30)
