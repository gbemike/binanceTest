import os
import csv
import json
import requests

import dagster as dg
import pandas as pd

from datetime import datetime
from dagster_slack import SlackResource


TICKER = "USDTNGN"

@dg.asset
def raw_rates(context: dg.AssetExecutionContext):
    """
    Raw rates gotten straight from the Binance API
    """
    usdt_endpoint = f"https://api.binance.com/api/v3/ticker/price?symbol={TICKER}"
    
    usdt_prices = requests.get(usdt_endpoint).json()

    # creates the data/raw directory if it doesn't exsit
    os.makedirs("exchange_rate_tracker/src/exchange_rate_tracker/defs/data/raw", exist_ok=True)

    # raw_rates.json is created in the data/raw directory, the file contains the endpoint data
    with open("exchange_rate_tracker/src/exchange_rate_tracker/defs/data/raw/raw_rates.json", "w+") as file:
        json.dump(usdt_prices, file)

@dg.asset(deps=[raw_rates])
def usdt_rates(context: dg.AssetExecutionContext):
    """
    Reading raw_rates json file and converting to a DataFrame
    """

    with open("exchange_rate_tracker/src/exchange_rate_tracker/defs/data/raw/raw_rates.json", "r") as file:
        raw_rates = json.loads(file.read())

    symbol = raw_rates['symbol']
    price = raw_rates['price']
    date = datetime.now()

    usdt_rates = pd.DataFrame({
        'Symbol': [symbol],
        'Price': [price],
        'Date': [date]
    })
    usdt_rates['Date'] = pd.to_datetime(usdt_rates['Date'])
 
    usdt_rates["Price"] = usdt_rates["Price"].astype(float)

    usdt_rates.to_csv("exchange_rate_tracker/src/exchange_rate_tracker/defs/data/raw/usdt_prices.csv", mode="a",index=False, header=False)

@dg.asset(deps=[usdt_rates])
def ohlc_rates(context: dg.AssetExecutionContext):
    """
    Produces ohlc and price change values
    """

    usdt_rates = pd.read_csv("exchange_rate_tracker/src/exchange_rate_tracker/defs/data/raw/usdt_prices.csv")

    # set dataframe index to Date, this makes it a DateTime index
    # we can only use the resample() function on dataframes with DateTime index
    usdt_rates = usdt_rates.set_index("Date")

    # convert all price entries to its corresponding ohlc values and aggregate it by 15 minutes
    ohlc_df = usdt_rates["Price"].resample("15T").ohlc()

    ohlc_df.to_csv("exchange_rate_tracker/src/exchange_rate_tracker/defs/data/raw/binance_ohlc_rates.csv")

@dg.asset(deps=['usdt_rates'])
# SlackResource enables sending messages to a slack channel
def rate_change(context: dg.AssetExecutionContext, slack_resource: SlackResource):
    """
    sends slack message on price changes
    """

    usdt_rates = pd.read_csv("exchange_rate_tracker/src/exchange_rate_tracker/defs/data/raw/usdt_prices.csv")

    usdt_rates['Date'] = pd.to_datetime(usdt_rates['Date'])

    usdt_rates["Price"] = usdt_rates["Price"].astype(float)

    usdt_rates = usdt_rates.set_index("Date")

    # convert all price entries to its corresponding ohlc values and aggregate it by 24 hours/ 1 day
    ohlc_df = usdt_rates["Price"].resample("24H").ohlc()

    # creating a new column called "changes" that represents price change for each day
    ohlc_df['changes'] = (((ohlc_df['close']) - (ohlc_df['close']).shift(1)) / (ohlc_df['close']).shift(1)) * 100

    ohlc_df.to_csv("exchange_rate_tracker/src/exchange_rate_tracker/defs/data/raw/daily_ohlc_rates.csv")

    # price threshold 
    threshold = 0.5

    # comparing the latest value(ohlc_df['changes'].iloc[-1]) to the threshold
    # if the above condition is true a message is sent to slack
    if abs(ohlc_df['changes'].iloc[-1]) < threshold:
        # checks whether change is a decrease or increase
        direction = "increased" if ohlc_df['changes'].iloc[-1] > 0 else "decreased"
        # message variable contaisn the string value that will be sent as a message to the slack channel
        message = f"Threshold crossed, price {direction} from {ohlc_df['close'].iloc[-2]} to {ohlc_df['close'].iloc[-1]}, indicating a {(ohlc_df['changes'].iloc[-1]).round(2)} change"
        # our message is sent using the SlackResource class
        slack_resource.get_client().chat_postMessage(channel='#rate_updates', text=message)
    else:
        pass
