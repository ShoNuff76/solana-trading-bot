import os
import time

print("🧪 DEBUG: Script started")

# Confirm environment keys exist
api_key = os.getenv("KRAKEN_API_KEY")
api_secret = os.getenv("KRAKEN_API_SECRET")

print(f"KRAKEN_API_KEY exists? {'Yes' if api_key else 'No'}")
print(f"KRAKEN_API_SECRET exists? {'Yes' if api_secret else 'No'}")

print("⚙️ Attempting to import ccxt...")
try:
    import ccxt
    print("✅ ccxt imported successfully")
except Exception as e:
    print(f"❌ Failed to import ccxt: {e}")
    raise SystemExit

print("⚙️ Attempting to initialize Kraken...")
try:
    kraken = ccxt.kraken({
        'apiKey': api_key,
        'secret': api_secret,
        'enableRateLimit': True
    })
    print("✅ Kraken connection initialized.")
except Exception as e:
    print(f"❌ Failed to initialize Kraken: {e}")
    raise SystemExit

print("🔁 Entering main loop...")

while True:
    print("📊 Still running...")
    time.sleep(30)
