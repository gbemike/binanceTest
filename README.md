# USDT rates retrieval 
This workspacde contains scripts that retrieve the USDT_NGN rates to be schedules every 15 minutes and retrieve the
ohlc values so it can plotted on a candlestick chart and show live trends and analysis


# API
The API is the initial point of the workspace, it provides the USDT_NGN prices we need.


# app.py
Retrieves the latest price information for the specified currency pairs from the Binance API, formats the data then 
appends the data to the  initial dataframe. Subsequently, the transformed dataframe, now featuring Open-High-Low-Close (OHLC) values, is appended to a new CSV file for comprehensive and organized data storage.


# streamlit_app.py
The USDT_NGN Rates Tracker is a Streamlit web application designed to visualize and analyze USDT_NGN rates over a specified date range. The app uses Plotly for interactive candlestick charting and offers a date range selection through Streamlit's user-friendly interface.

