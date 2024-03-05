import numpy as np
from coinbase_advanced_trader.coinbase_client import getMarketTrades
import time
from coinbase_advanced_trader.config import set_api_credentials
from coinbase_advanced_trader.strategies.limit_order_strategies import fiat_limit_buy, fiat_limit_sell
from coinbase_advanced_trader.coinbase_client import listAccounts, getMarketTrades

# Set your API key and secret
API_KEY = "Od5pxQsRIEWatydN"
API_SECRET = "Qa7fQoXdmGn3beR888wpYOfEndObEPCd"

set_api_credentials(API_KEY, API_SECRET)

product_id = "BTC-USD"  
usd_size = 5  # Replace with your desired USD amount to spend

# Number of trades to consider for SMA
N = 10


def breakout_trading_strategy(product_id, usd_size, threshold):
    # Fetch the latest 100 trades for the given product to analyze
    latest_trades = getMarketTrades(product_id, 100)
    prices = [float(trade.get('price')) for trade in latest_trades.get('trades')]
    
    # Calculate the highest price in the last 100 trades
    high_price = np.max(prices)

    # Calculate the lowest price in the last 100 trades
    low_price = np.min(prices)

    # Calculate the breakout threshold
    breakout_threshold_high = high_price * (1 + threshold)
    breakout_threshold_low = low_price * (1 - threshold)

    # Get the latest price
    latest_price = prices[0]

    # Decision making
    if latest_price > breakout_threshold_high:
        # If the latest price is above the breakout threshold, place a buy order
        print("Breakout detected above the threshold, placing a buy order")
        order_result = fiat_limit_buy(product_id, usd_size)
        return order_result
    elif latest_price < breakout_threshold_low:
        # If the latest price is below the breakout threshold, place a sell order
        print("Breakout detected below the threshold, placing a sell order")
        order_result = fiat_limit_sell(product_id, usd_size)
        return order_result
    else:
        # If the latest price is within the threshold range, do nothing
        print("No breakout detected, no action taken")
        return None


threshold = 0.01  # 1% threshold for breakout detection

# Run the breakout trading strategy
while True:
    try:
        # Perform trading based on the SMA strategy
        trade_result = breakout_trading_strategy(product_id, usd_size, threshold)
        print(trade_result)

        # You can adjust the sleep time as needed to manage API call limits
        time.sleep(60)  # Sleep for 1 minute

    except Exception as e:
        print(f"An error occurred: {e}")
        # In case of an error, you can wait longer to prevent rapid-fire errors
        time.sleep(300)  # Wait for 5 minutes before trying again

