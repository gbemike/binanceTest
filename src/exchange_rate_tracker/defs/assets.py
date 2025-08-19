import csv
import json
import os
from datetime import datetime

import dagster as dg
import pandas as pd
import requests
from dagster_slack import SlackResource

from exchange_rate_tracker.defs.constants import (
    BINANCE_OHLC_CSV,
    DAILY_OHLC_CSV, RAW_DATA_DIR,
    RAW_RATES_JSON,
    SLACK_ALERT_CHANNEL, TICKER,
    USDT_PRICES_CSV
)


@dg.asset
def raw_rates(context: dg.AssetExecutionContext):
    """
    Raw rates gotten straight from the Binance API
    """
    usdt_endpoint = f"https://api.binance.com/api/v3/ticker/price?symbol={TICKER}"
    
    try:
        usdt_prices = requests.get(usdt_endpoint).json()
    except requests.RequestException as e:
        context.log.error("Failed to fetch data from Binance API.")
        raise

    # creates the data/raw directory if it doesn't exsit
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    # raw_rates.json is created in the data/raw directory, the file contains the endpoint data
    with open(RAW_RATES_JSON, "w+") as file:
        json.dump(usdt_prices, file)

@dg.asset(deps=[raw_rates])
def usdt_rates(context: dg.AssetExecutionContext):
    """
    Reading raw_rates json file and converting to a DataFrame
    """

    with open(RAW_RATES_JSON, "r") as file:
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
    
    file_exists = os.path.isfile(USDT_PRICES_CSV)
    usdt_rates.to_csv(USDT_PRICES_CSV, mode="a",index=False, header=not file_exists)

@dg.asset(deps=[usdt_rates])
def ohlc_rates(context: dg.AssetExecutionContext):
    """
    Produces ohlc and price change values
    """

    usdt_rates = pd.read_csv(USDT_PRICES_CSV)

    # set dataframe index to Date, this makes it a DateTime index
    usdt_rates['Date'] = pd.to_datetime(usdt_rates['Date'])
    usdt_rates = usdt_rates.set_index("Date")

    # resample to 15-minute intervals and compute OHLC values
    ohlc_df = usdt_rates["Price"].resample("15T").ohlc()

    ohlc_df.to_csv(BINANCE_OHLC_CSV)


@dg.asset(deps=[usdt_rates])
# SlackResource enables sending messages to a slack channel
def rate_change(context: dg.AssetExecutionContext, slack_resource: SlackResource):
    """
    sends slack message on price changes
    """

    usdt_rates = pd.read_csv(USDT_PRICES_CSV)

    usdt_rates['Date'] = pd.to_datetime(usdt_rates['Date'])
    usdt_rates["Price"] = usdt_rates["Price"].astype(float)
    usdt_rates = usdt_rates.set_index("Date")

    # convert all price entries to its corresponding ohlc values and aggregate it by 24 hours/ 1 day
    ohlc_df = usdt_rates["Price"].resample("24H").ohlc()

    # creating a new column called "changes" that represents price change for each day
    ohlc_df['changes'] = (((ohlc_df['close']) - (ohlc_df['close']).shift(1)) / (ohlc_df['close']).shift(1)) * 100

    ohlc_df.to_csv(DAILY_OHLC_CSV)

    # set the threshold
    threshold = 0.5  

    # get the last two close prices
    prev_close, latest_close = ohlc_df['close'].iloc[-2], ohlc_df['close'].iloc[-1]

    # get the latest percent change
    latest_change = ohlc_df['changes'].iloc[-1]

    # only trigger alert if change exceeds threshold
    if abs(latest_change) >= threshold:
        direction = "increased" if latest_change > 0 else "decreased"
        message = (
            f"Threshold crossed: Price {direction} from {prev_close} "
            f"to {latest_close}, a {latest_change:.2f}% change."
        )

        slack_resource.get_client().chat_postMessage(
            channel=SLACK_ALERT_CHANNEL,
            text=message
        )
