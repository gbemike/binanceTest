import pandas as pd
import streamlit as st
from datetime import datetime as dt, timedelta as td
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="USDT_NGN Rates Tracker")

# Load the dataset
@st.cache_data
def load_dataset():
    """Loads the OHLC data from the CSV file."""
    df = pd.read_csv("src/exchange_rate_tracker/defs/data/raw/daily_ohlc_rates.csv", parse_dates=True)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Create the candlestick chart
def create_chart(df):
    """Creates and displays the candlestick chart."""
    figure = go.Figure(
        data=[
            go.Candlestick(
                x=df['Date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                increasing_line_color='green',
                decreasing_line_color='red',
            )
        ]
    )

    # Add a line for the closing price
    figure.add_trace(go.Scatter(x=df['Date'], y=df['close'], mode='lines', name='Close Price'))

    figure.update_layout(
        xaxis_title='Date',
        yaxis_title='Rates',
        xaxis_rangeslider_visible=False,
        template='plotly_white'
    )

    st.plotly_chart(figure, theme='streamlit', use_container_width=True)

# --- Main Dashboard ---
st.title("USDT_NGN Rates Tracker")

# Load the data
original_df = load_dataset()

# --- Sidebar for Date Range Selection ---
st.sidebar.markdown("#### Date Range Selection")

# Default to the last day's data
default_end_date = original_df['Date'].max()
default_start_date = default_end_date - td(days=1)

col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(label="Start Date", value=default_start_date)
with col2:
    end_date = st.date_input(label="End Date", value=default_end_date)

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter the dataframe based on the selected date range
sub_df = original_df.loc[(original_df['Date'] >= start_date) & (original_df['Date'] <= end_date)]

# Display the chart
create_chart(sub_df)