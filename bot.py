import os
import ccxt
import time

print("🚀 Bot is starting...")

# === Check environment variables ===
api_key = os.getenv("KRAKEN_API_KEY")
api_secret = os.getenv("KRAKEN_API_SECRET")

print(f"🔐 KRAKEN_API_KEY: {api_key}")
print(f"🔐 KRAKEN_API_SECRET: {api_secret}")

if not api_key or not api_secret:
    raise SystemExit("❌ API Key or Secret not found. Check Render environment variables.")

# === SET UP KRAKEN CONNECTION ===
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

print("🔐 API Key Loaded")
print("🔐 API Secret Loaded")

# === SET UP KRAKEN CONNECTION ===
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

symbol = 'SOL/USD'

# === CONFIG ===
buy_drop_1 = 0.03
buy_drop_2 = 0.05
sell_gain = 0.03
stop_loss = 0.06
trade_amount = 0.5

# === STATE ===
recent_high = None
first_buy_price = None
second_buy_price = None
holding = 0

def fetch_price():
    try:
        ticker = kraken.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        print(f"❌ Failed to fetch price: {e}")
        return None

print("🔁 Entering price check loop...")

while True:
    try:
        price = fetch_price()
        if price is None:
            time.sleep(60)
            continue

        print(f"📊 Current Price: ${price:.2f}")

        # Update recent high
        if recent_high is None or price > recent_high:
            recent_high = price
            print(f"📈 New recent high set: {recent_high}")

        # Buy 1st
        if holding == 0 and price <= recent_high * (1 - buy_drop_1):
            kraken.create_market_buy_order(symbol, trade_amount)
            first_buy_price = price
            holding = 1
            print(f"🟢 Bought 1st position at: ${first_buy_price:.2f}")

        # Buy 2nd
        elif holding == 1 and price <= recent_high * (1 - buy_drop_2):
            kraken.create_market_buy_order(symbol, trade_amount)
            second_buy_price = price
            holding = 2
            print(f"🟢 Bought 2nd position at: ${second_buy_price:.2f}")

        # Sell logic
        if holding == 2:
            avg_buy = (first_buy_price + second_buy_price) / 2
            if price >= avg_buy * (1 + sell_gain):
                kraken.create_market_sell_order(symbol, trade_amount * 2)
                print(f"💰 Sold for profit at: ${price:.2f}")
                holding = 0
                recent_high = price
                first_buy_price = None
                second_buy_price = None
            elif price <= avg_buy * (1 - stop_loss):
                kraken.create_market_sell_order(symbol, trade_amount * 2)
                print(f"🛑 Stop-loss triggered at: ${price:.2f}")
                holding = 0
                recent_high = price
                first_buy_price = None
                second_buy_price = None

        time.sleep(60)

    except Exception as e:
        print(f"⚠️ Error in main loop: {e}")
        time.sleep(60)
