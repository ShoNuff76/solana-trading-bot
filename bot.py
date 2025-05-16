import os
import krakenex
import time
from datetime import datetime

# === CONFIG ===
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ASSET_PAIR = 'SOLUSD'
BUY_DROP_PERCENT = 0.08   # Buy if price drops 8% from recent high
SELL_GAIN_PERCENT = 0.05  # Sell if price rises 5% from buy price
TRADE_AMOUNT = '10'       # $10 per trade
CHECK_INTERVAL = 60       # 1 minute

# === INIT ===
k = krakenex.API()
k.key = API_KEY
k.secret = API_SECRET

recent_high = None
holding = False
buy_price = 0

def get_current_price():
    try:
        response = k.query_public('Ticker', {'pair': ASSET_PAIR})
        return float(response['result'][list(response['result'].keys())[0]]['c'][0])
    except Exception as e:
        print(f"Error fetching price: {e}", flush=True)
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
        print(f"Order error: {e}", flush=True)
        return None

def log_trade(action, price):
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] {action} at ${price:.2f}", flush=True)

while True:
    price = get_current_price()
    if price:
        if not recent_high or price > recent_high:
            recent_high = price

        print(f"Price: ${price:.2f} | Recent High: ${recent_high:.2f} | Holding: {holding}", flush=True)

        if not holding and price < recent_high * (1 - BUY_DROP_PERCENT):
            result = place_order('buy', TRADE_AMOUNT)
            if result and 'result' in result:
                holding = True
                buy_price = price
                log_trade('BUY', price)

        elif holding and price > buy_price * (1 + SELL_GAIN_PERCENT):
            result = place_order('sell', TRADE_AMOUNT)
            if result and 'result' in result:
                holding = False
                log_trade('SELL', price)
                recent_high = price  # reset high after sell

    time.sleep(CHECK_INTERVAL)

