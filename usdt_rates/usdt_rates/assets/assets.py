from dagster import asset, AssetExecutionContext

import json
import os
import requests

import pandas as pd
from datetime import datetime

import csv

@asset
def usdt_rates():
    """
    Rates gotten straight from the Binance API
    """

    usdt_symbol = "USDTNGN"
    usdt_endpoint = f"https://api.binance.com/api/v3/ticker/price?symbol={usdt_symbol}"

    usdt_prices = requests.get(usdt_endpoint).json()

    symbol = usdt_prices['symbol']
    price = usdt_prices['price']
    date = datetime.now()

    os.makedirs("data/raw", exist_ok=True)
    
    df = pd.DataFrame({
        'Symbol': [symbol],
        'Price': [price],
        'Date': [date]
    })

    df.to_csv("data/raw/usdt_prices.csv", mode="a",index=False, header=False)
    #with open("data/raw/usdt_prices.json", "w") as f:
    #    json.dump(usdt_prices, f)

@asset(deps=[usdt_rates])
def ohlc_rates(context: AssetExecutionContext):
    usdt_rates = pd.read_csv("data/raw/usdt_prices.csv")

    usdt_rates['Date'] = pd.to_datetime(usdt_rates['Date'])
    usdt_rates["Price"] = usdt_rates["Price"].astype(float)

    usdt_rates = usdt_rates.set_index("Date")

    ohlc_df = usdt_rates["Price"].resample("15T").ohlc() 
    ohlc_df.to_csv("data/raw/binance_ohlc_rates.csv")
