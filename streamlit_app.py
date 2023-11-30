import pandas as pd
import streamlit as st
from datetime import datetime as dt, timedelta as td
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="USDT_NGN Rates Tracker")

# load dataset
@st.cache_data
def load_dataset():
    df = pd.read_csv("usdt_rates/data/raw/binance_ohlc_rates.csv", parse_dates=True)
    df['Date'] = pd.to_datetime(df['Date'])

    return df

original_df = load_dataset()

def create_chart(df):
    figure = go.Figure(
    data = [
    go.Candlestick(
        x = df['Date'],
        open = df['open'],
        high = df['high'],
        low = df['low'],
        close = df['close'],
        increasing_line_color = 'green',
        decreasing_line_color = 'red',
        increasing_line_width = 22,
        decreasing_line_width = 22,
    )
    ]
    )

    figure.update_layout(xaxis_title='Date',
                     yaxis_title='Rates',
                     xaxis_tickformat='',
                     xaxis_rangeslider_visible=False,
                     template='plotly_white')
    
    st.plotly_chart(figure, theme='streamlit', use_container_width=True)
    
    return df

# Add trace for close price line
#figure.add_trace(go.Scatter(x=original_df['Date'], y=original_df['close'], mode='lines', name='Close Price'))

# Dashboard
st.title("USDT_NGN Rates Tracker :tea: :coffee:")
st.sidebar.markdown("#### Date Range Selection")

#1.Issue: Need a placeholder for start_date and end_date

# Default to the last day's data
default_end_date = original_df['Date'].max()
default_start_date = default_end_date - td(days=1)

col1,col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(label="Start Date", value=default_start_date)
with col2:
    end_date = st.date_input(label="End Date", value=default_end_date)

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Date Range logic
sub_df =original_df.loc[(original_df['Date'] >= start_date) & (original_df['Date'] <= end_date)]
#sub_df = sub_df.reset_index()

sub_df = create_chart(sub_df)

