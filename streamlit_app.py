import pandas as pd
import streamlit as st
from datetime import datetime as dt, timedelta as td
from bokeh.plotting import figure, column, show
from bokeh.models import HoverTool, NumeralTickFormatter
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="USDT_NGN Rates Tracker")

# load dataset
@st.cache_data
def load_dataset():
    df = pd.read_csv("USDT_NGN rates.csv", parse_dates=True)
    df['Date'] = pd.to_datetime(df['Date'])

    return df

original_df = load_dataset()


figure = go.Figure(
    data = [
        go.Candlestick(
            x = original_df['Date'],
            open = original_df['open'],
            high = original_df['high'],
            low = original_df['low'],
            close = original_df['close'],
            increasing_line_color = 'green',
            decreasing_line_color = 'red'
        )
    ]
)

figure.update_layout(xaxis_title='Date',
                     yaxis_title='Rates',
                     xaxis_tickformat='',
                     xaxis_rangeslider_visible=False)

# Dashboard
st.title("USDT_NGN Rates Tracker :tea: :coffee:")
st.sidebar.markdown("#### Date Range Selection")

st.plotly_chart(figure,theme='streamlit', use_container_width=True)

col1,col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(label="Start Date", value=dt(2023,1,1))
with col2:
    end_date = st.date_input(label="End Date", value=dt(2023,12,31))