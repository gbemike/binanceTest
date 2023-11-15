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

"""sumary_line

1. Streamlit graphs with KPIS
2. Start scheduling

"""
