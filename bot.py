import ccxt
import time

# === SET UP KRAKEN CONNECTION ===
kraken = ccxt.kraken({
    'apiKey': 'YOUR_API_KEY_HERE',
    'secret': 'YOUR_API_SECRET_HERE',
    'enableRateLimit': True
})

symbol = 'SOL/USD'  # Kraken uses USD, not USDT for SOL

# === CONFIGURABLE PARAMETERS ===
buy_drop_1 = 0.03    # 3% drop triggers 1st buy
buy_drop_2 = 0.05    # 5% drop triggers 2nd buy
sell_gain = 0.03     # Sell when up 3% from avg buy
stop_loss = 0.06     # Stop loss at 6% drop from avg buy
trade_amount = 0.5   # Adjust to how much SOL to buy each time

# === STATE TRACKING ===
recent_high = None
first_buy_price = None
second_buy_price = None
holding = 0  # 0 = no position, 1 = partial, 2 = full

def fetch_price():
    ticker = kraken.fetch_ticker(symbol)
    return ticker['last']

def place_order(side, amount):
    order = kraken.create_market_order(symbol, side, amount)
    print(f"{side.upper()} ORDER EXECUTED: {order}")
    return order

while True:
    try:
        price = fetch_price()
        print(f"Current Price: ${price:.2f}")

        # Update recent high
        if recent_high is None or price > recent_high:
            recent_high = price
            print(f"New high set: {recent_high}")

        # Buy 1st position
        if holding == 0 and price <= recent_high * (1 - buy_drop_1):
            order = place_order('buy', trade_amount)
            first_buy_price = price
            holding = 1

        # Buy 2nd position
        elif holding == 1 and price <= recent_high * (1 - buy_drop_2):
            order = place_order('buy', trade_amount)
            second_buy_price = price
            holding = 2

        # Sell logic
        if holding == 2:
            avg_buy = (first_buy_price + second_buy_price) / 2

            if price >= avg_buy * (1 + sell_gain):
                order = place_order('sell', trade_amount * 2)
                print(f"Sold for profit at ${price:.2f}")
                holding = 0
                recent_high = price
                first_buy_price = None
                second_buy_price = None

            elif price <= avg_buy * (1 - stop_loss):
                order = place_order('sell', trade_amount * 2)
                print(f"Stop-loss triggered at ${price:.2f}")
                holding = 0
                recent_high = price
                first_buy_price = None
                second_buy_price = None

        time.sleep(60)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)
