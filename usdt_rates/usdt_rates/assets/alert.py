from dagster import asset, AssetExecutionContext
from dagster_slack import SlackResource

import json
import os
import requests

import pandas as pd
from datetime import datetime

import csv

@asset(deps=['usdt_rates'])
def rate_change(context, slack: SlackResource):
    usdt_rates = pd.read_csv("data/raw/usdt_prices.csv")
    usdt_rates['Date'] = pd.to_datetime(usdt_rates['Date'])
    usdt_rates["Price"] = usdt_rates["Price"].astype(float)

    usdt_rates = usdt_rates.set_index("Date")

    ohlc_df = usdt_rates["Price"].resample("24H").ohlc()
    ohlc_df['changes'] = (((ohlc_df['close']) - (ohlc_df['close']).shift(1)) / (ohlc_df['close']).shift(1)) * 100
    ohlc_df.to_csv("data/raw/daily_ohlc_rates.csv")

    if ohlc_df['changes'].iloc[-1] < 0.5:
        message = f"Threshold crossed, price changed from {ohlc_df['close'].iloc[-2]} to {ohlc_df['close'].iloc[-1]}, indicating a {(ohlc_df['changes'].iloc[-1]).round(2)} change"
        slack.get_client().chat_postMessage(channel='#rate_updates', text=message)
    else:
        pass
