"""
Cryptocurrency Trading Bot for Binance

This script is designed to automate trading on the Binance cryptocurrency exchange. It uses the Binance API to perform 
trades based on the Relative Strength Index (RSI) strategy. The script operates with the following key components and features:

1. Binance API Interaction: 
   - Utilizes the 'binance.client' module to interact with the Binance API.
   - Performs operations like fetching asset balances and executing trades.

2. RSI-Based Trading Logic:
   - Calculates the RSI for a specified cryptocurrency pair (default is BTCUSDT).
   - Makes buy or sell decisions based on predefined RSI thresholds (entry and exit points).

3. Account and Log Management:
   - Manages a virtual trading account stored in a JSON file at 'account_path'.
   - Logs trading activities and errors to designated log files.

4. Automated Trade Execution:
   - Continuously monitors RSI values and executes trades when conditions are met.
   - Implements a basic mechanism to alternate between buying and selling actions.

Usage:
- Set up Binance API credentials (API_KEY and SECRET_KEY) using the 'decouple' module for secure access.
- Define asset pairs, log paths, and RSI thresholds as per trading requirements.
- Run the script to start automated trading based on RSI strategy.
- The script logs all activities and trades, which can be monitored for performance and debugging purposes.

Note:
- This script is configured to run in test mode ('testnet=True'). 
- Ensure thorough testing and understanding of the code and trading strategies before live trading.
- Always review the Binance API documentation and use proper error handling for production use.

Dependencies:
- binance.client, pandas, pandas_ta, json, os, sys, time, datetime
"""

from decouple import config
from binance.client import Client
import pandas as pd
import pandas_ta as ta
import json
import os
import sys
import time
import datetime


asset = "BTCUSDT"
account_path = "path-to-account"
log_path = "path-to-log"
trades_path = (
    "path-to-trades-log"
)
log_format_monthly = "%Y-%m-%d"
log_format_daily = "%H:%M:%S"
entry = 38
exit = 78


client = Client(
    config("API_KEY"),
    config("SECRET_KEY"),
    testnet=True,
)  # to specify binance.us or binance.tr include tdl="us", etc.
# look through documentation before live trading
balance = client.get_asset_balance(asset="BTC")


def fetch_klines(asset):  # klines = candlestick data (binance)

    """
    Fetch the historical k-line (candlestick) data for a specified asset from Binance.
    
    Parameters:
    asset (str): The trading pair (e.g., 'BTCUSDT') for which to fetch the k-line data.
    
    Returns:
    DataFrame: A Pandas DataFrame containing the time and price data of the fetched k-lines.
    """
    
    klines = client.get_historical_klines(
        symbol=asset, interval=Client.KLINE_INTERVAL_1MINUTE, start_str="1 hour ago UTC"
    )

    klines = [[x[0], float(x[4])] for x in klines]

    klines = pd.DataFrame(klines, columns=["time", "price"])
    klines["time"] = pd.to_datetime(klines["time"], unit="ms")

    return klines


def get_rsi(asset):

    """
    Calculate the Relative Strength Index (RSI) for the latest data point of a specified asset.
    
    Parameters:
    asset (str): The trading pair (e.g., 'BTCUSDT') for which to calculate the RSI.
    
    Returns:
    float: The RSI value for the latest data point.
    """
    
    klines = fetch_klines(asset)
    klines["rsi"] = ta.rsi(close=klines["price"], length=14)

    return klines["rsi"].iloc[-1]


def create_account():

    """
    Create a new trading account configuration and store it in a file.
    
    The account is initialized with 'is_buying' set to True and an empty 'assets' dictionary.
    The configuration is saved to the path specified in 'account_path'.
    """
    
    account = {"is_buying": True, "assets": {}}

    with open(account_path, "w") as f:
        f.write(json.dumps(account))

def log(msg):

    """
    Log a message to both the console and a log file.
    
    Parameters:
    msg (str): The message to be logged.
    
    The function prints the message to the console and writes it to a log file
    located at 'log_path', organizing logs by date.
    """
    
    print(f"LOG: {msg}")

    if not os.path.isdir(log_path):
        os.mkdir(log_path)

    now = datetime.datetime.now()
    today = now.strftime(log_format_monthly)
    time = now.strftime(log_format_daily)

    with open(f"{log_path}/{today}.txt", "a+") as log_file:
        log_file.write(f"{time} : {msg}\n")


def trade_log(sym, side, price, amount):

     """
    Log details of a trade to both the console and a trade log file.
    
    Parameters:
    sym (str): The trading pair (e.g., 'BTCUSDT') involved in the trade.
    side (str): The side of the trade ('buy' or 'sell').
    price (float): The price at which the trade occurred.
    amount (float): The amount traded.
    
    The function logs the trade details in a CSV format in a file located at 'trades_path'.
    """
    
    log(f"{side} {amount} {sym} for {price}")

    if not os.path.isdir(trades_path):
        os.mkdir(trades_path)

    now = datetime.datetime.now()
    today = now.strftime(log_format_monthly)
    time = now.strftime(log_format_daily)

    if not os.path.isfile(f"{trades_path}/{today}.csv"):
        with open(f"{trades_path}/{today}.csv", "w") as trade_file:
            trade_file.write("sym,side,amount,price\n")

    with open(f"{trades_path}/{today}.csv", "a+") as trade_file:
        trade_file.write(f"{sym},{side},{amount},{price}\n")


def do_trade(account, client, asset, side, quantity):

    """
    Execute a trade on the Binance platform and log the trade details.
    
    Parameters:
    account (dict): The account configuration dictionary.
    client (Client): The Binance client object for API access.
    asset (str): The trading pair (e.g., 'BTCUSDT') to trade.
    side (str): The side of the trade ('buy' or 'sell').
    quantity (float): The quantity to trade.
    
    This function places a market order, waits for its completion, and logs the trade details.
    It also updates the account configuration based on the trade executed.
    """
    
    if side == "buy":
        order = client.order_market_buy(
            symbol=asset,
            quantity=quantity,
        )
        account["is_buying"] = False

    else:
        order = client.order_market_sell(
            symbol=asset,
            quantity=quantity,
        )
        account["is_buying"] = True

    order_id = order["orderId"]

    while order["status"] != "FILLED":
        order = client.get_order(symbol=asset, orderId=order_id)
        time.sleep(1)

    # print(order)   // optionally

    price_paid = sum(
        [float(fill["price"]) * float(fill["qty"]) for fill in order["fills"]]
    )

    # trade log
    trade_log(asset, side, price_paid, quantity)

    with open(account_path, "w") as f:
        f.write(json.dumps(account))


rsi = get_rsi(asset)
old_rsi = rsi


while True:
    try:
        if not os.path.exists(account_path):
            create_account()

        with open(account_path) as f:
            account = json.load(f)

        print(account)

        old_rsi = rsi
        rsi = get_rsi(asset)

        if account["is_buying"]:
            if rsi < entry and old_rsi > entry:
                do_trade(account, client, asset, "buy", 0.001)

        else:
            if rsi > exit and old_rsi < exit:
                do_trade(account, client, asset, "sell", 0.001)

        print(rsi)
        time.sleep(3)

    except Exception as e:
        log("ERROR" + str(e))
