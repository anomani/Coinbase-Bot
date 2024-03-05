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
# Threshold to determine if the latest price is significantly lower or higher than the SMA
threshold = 0.02  # 2%

def simple_trading_strategy(product_id, usd_size, N, threshold):
    # Fetch the latest N trades for the given product
    latest_trades = getMarketTrades(product_id, N)

    sum_of_prices = 0
    for trade in latest_trades.get('trades'):
        sum_of_prices += float(trade.get('price'))


    #Calculate the SMA of the last N trades
    sma = sum_of_prices / N

    # Get the latest trade price as a float
    latest_price = float(latest_trades.get('trades')[0].get('price'))

    # Decision making
    if latest_price < sma * (1 - threshold):
        # If the latest price is significantly lower than the SMA, buy
        print("Performing a limit buy")
        limit_buy_order = fiat_limit_buy(product_id, usd_size)
        return limit_buy_order
    elif latest_price > sma * (1 + threshold):
        # If the latest price is significantly higher than the SMA, sell
        print("Performing a limit sell")
        limit_sell_order = fiat_limit_sell(product_id, usd_size)
        return limit_sell_order
    else:
        # If the price is close to the SMA, do nothing
        print("No action required based on the SMA strategy")
        return None

# print(trade_result)

while True:
    try:
        # Perform trading based on the SMA strategy
        trade_result = simple_trading_strategy(product_id, usd_size, N, threshold)
        print(trade_result)

        # You can adjust the sleep time as needed to manage API call limits
        time.sleep(60)  # Sleep for 1 minute

    except Exception as e:
        print(f"An error occurred: {e}")
        # In case of an error, you can wait longer to prevent rapid-fire errors
        time.sleep(300)  # Wait for 5 minutes before trying again
