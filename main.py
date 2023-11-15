import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

df = pd.read_csv('binance_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')
ohlc_df = df['Price'].resample('24H').ohlc()
ohlc_df.to_csv('USDT_NGN rates.csv', mode='a', header=False)