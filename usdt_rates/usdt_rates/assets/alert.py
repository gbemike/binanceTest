from dagster import asset, AssetExecutionContext, WeeklyPartitionsDefinition
from dagster_slack import SlackResource

import json
import os
import requests

import pandas as pd
from datetime import datetime

import csv

@asset(deps=['usdt_rates'], partitions_def=WeeklyPartitionsDefinition(start_date="2023-12-01"))
# slack_resource from usdt_rates/__init__.py contains the API TOKEN,
# SlackResource enables sending messages to a slack channel
def rate_change(context: AssetExecutionContext, slack_resource: SlackResource):
    """
    sends slack message on price changes
    """
    
    usdt_rates = pd.read_csv("data/raw/usdt_prices.csv")

    usdt_rates['Date'] = pd.to_datetime(usdt_rates['Date'])

    usdt_rates["Price"] = usdt_rates["Price"].astype(float)

    usdt_rates = usdt_rates.set_index("Date")

    # convert all price entries to its corresponding ohlc values and aggregate it by 24 hours/ 1 day
    ohlc_df = usdt_rates["Price"].resample("24H").ohlc()

    # creating a new column called "changes" that represents price change for each day
    ohlc_df['changes'] = (((ohlc_df['close']) - (ohlc_df['close']).shift(1)) / (ohlc_df['close']).shift(1)) * 100

    ohlc_df.to_csv("data/raw/daily_ohlc_rates.csv")

    # price threshold 
    threshold = 0.5

    # comparing the latest value(ohlc_df['changes'].iloc[-1]) to the threshold
    # if the above condition is true a message is sent to slack
    if ohlc_df['changes'].iloc[-1] < threshold:
        # message variable contaisn the string value that will be sent as a message to the slack channel
        message = f"Threshold crossed, price changed from {ohlc_df['close'].iloc[-2]} to {ohlc_df['close'].iloc[-1]}, indicating a {(ohlc_df['changes'].iloc[-1]).round(2)} change"
        # our message is sent using the SlackResource class
        slack_resource.get_client().chat_postMessage(channel='#rate_updates', text=message)
    else:
        pass
