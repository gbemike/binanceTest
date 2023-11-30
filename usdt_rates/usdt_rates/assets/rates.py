from dagster import asset, AssetExecutionContext

import json
import os
import requests

import pandas as pd
from datetime import datetime

import csv

@asset
def raw_rates():
    """
    Raw rates gotten straight from the Binance API
    """

    usdt_symbol = "USDTNGN"
    usdt_endpoint = f"https://api.binance.com/api/v3/ticker/price?symbol={usdt_symbol}"

    usdt_prices = requests.get(usdt_endpoint).json()

    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/raw_rates.json", "w+") as file:
        json.dump(usdt_prices, file)

@asset(
        deps=[raw_rates]
       )
def usdt_rates():
    """
    Reading raw_rates json file and converting to a DataFrame
    """

    with open("data/raw/raw_rates.json", "r") as file:
        raw_rates = json.loads(file.read())

    symbol = raw_rates['symbol']
    price = raw_rates['price']
    date = datetime.now()
    
    df = pd.DataFrame({
        'Symbol': [symbol],
        'Price': [price],
        'Date': [date]
    })

    df.to_csv("data/raw/usdt_prices.csv", mode="a",index=False, header=False)


@asset(
        deps=[usdt_rates]
        )
def ohlc_rates(context: AssetExecutionContext):
    usdt_rates = pd.read_csv("data/raw/usdt_prices.csv")

    usdt_rates['Date'] = pd.to_datetime(usdt_rates['Date'])
    usdt_rates["Price"] = usdt_rates["Price"].astype(float)

    usdt_rates = usdt_rates.set_index("Date")

    ohlc_df = usdt_rates["Price"].resample("15T").ohlc()
    ohlc_df['changes'] = ((ohlc_df['close']) - (ohlc_df['open']).shift(1)) * 100
    ohlc_df.to_csv("data/raw/binance_ohlc_rates.csv")
