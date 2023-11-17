import requests
import pandas as pd
from datetime import datetime

symbols = 'USDTNGN'
endpoint = f'https://api.binance.com/api/v3/ticker/price?symbol={symbols}'

response = requests.get(endpoint)
data = response.json()

symbol = data['symbol']
price = data['price']
timestamp = datetime.now()

rawData = pd.DataFrame({
    'Symbol': [symbol],
    'Price': [price],
    'Date': [timestamp]
})

rawData.to_csv('binance_data.csv', mode='a', header=False, index = False)

df = pd.read_csv('binance_data.csv')
df['Date'] = pd.to_datetime(df['Date'], format='mixed')

df = df.set_index('Date')
ohlc_df = df.resample('15T').agg({'Price': 'ohlc'})

ohlc_df.to_csv('USDT_NGN ratesss.csv', mode='a', header=False)
