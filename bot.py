import os
import krakenex
import time
import pandas as pd
from datetime import datetime

# === CONFIG ===
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ASSET_PAIR = 'SOLUSD'
BUY_DROP_PERCENT = 0.02   # Buy when price drops 2%
SELL_GAIN_PERCENT = 0.03  # Sell when price rises 3%
TRADE_AMOUNT = '10'       # $10 worth of SOL per trade
CHECK_INTERVAL = 300      # 5 minutes

# === INIT ===
k = krakenex.API()
k.key = API_KEY
k.secret = API_SECRET

price_history = []
holding = False
buy_price = 0

def get_current_price():
    try:
        response = k.query_public('Ticker', {'pair': ASSET_PAIR})
        return float(response['result'][list(response['result'].keys())[0]]['c'][0])
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def place_order(order_type, volume):
    try:
        return k.query_private('AddOrder', {
            'pair': ASSET_PAIR,
            'type': order_type,
            'ordertype': 'market',
            'volume': volume
        })
    except Exception as e:
        print(f"Order error: {e}")
        return None

def log_trade(action, price):
    timestamp = datetime.now().isoformat()
    df = pd.DataFrame([[timestamp, action, price]], columns=['Time', 'Action', 'Price'])
    df.to_csv('trade_log.csv', mode='a', header=False, index=False)

while True:
    print("🔄 Bot is alive and checking price...")

    price = get_current_price()
    print(f"Fetched price: {price}")

    if price:
        price_history.append(price)
        if len(price_history) > 20:
            price_history.pop(0)

        avg_price = sum(price_history) / len(price_history)
        print(f"Current: ${price:.2f} | Avg: ${avg_price:.2f} | Holding: {holding}")

        if not holding and price < avg_price * (1 - BUY_DROP_PERCENT):
            result = place_order('buy', TRADE_AMOUNT)
            if result and 'result' in result:
                buy_price = price
                holding = True
                log_trade('BUY', price)
                print(f"[BUY] at ${price:.2f}")

        elif holding and price > buy_price * (1 + SELL_GAIN_PERCENT):
            result = place_order('sell', TRADE_AMOUNT)
            if result and 'result' in result:
                holding = False
                log_trade('SELL', price)
                print(f"[SELL] at ${price:.2f}")

    time.sleep(CHECK_INTERVAL)
