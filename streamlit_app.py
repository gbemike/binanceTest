import pandas as pd
import streamlit as st
from datetime import datetime as dt
from bokeh.plotting import figure, column


st.set_page_config(layout="wide", page_title="USDT_NGN Rates Tracker")

# load dataset
@st.cache_data
def load_dataset():
    df = pd.read_csv("USDT_NGN rates.csv")
    df['Date'] = df.index
    df['BarColor'] = df[['open', 'close']].apply(lambda x: 'red' if x.open > x.close else 'green', axis=1)
    df['DateStr'] = df.Date.astype(str) 

    return df

df = load_dataset()

# create chart
def chart(df, close_line = False):
    # candlestick figure
    candle =figure(x_axis_type='datetime', 
                   x_range=(df.Date.values[0], 
                            df.Date.values[-1]), 
                            width='', height=500, 
                            title='USDT_NGN', tool_tips=[('Date','@Date'), ('open','@open'), ('high','@high'), ('low','@low'), ('close','@close')])
    
    # creates a black line between low and high values
    candle.segement('Date', 'low','Date', 'high', color='black', line_width=0.5, source=df)
    # creates ....
    candle.segement('Date', 'open','Date', 'close', line_color='BarColor', line_width=2 if len(df)>100 else 6, source=df)

# Dashboard
st.title("USDT_NGN Rates Tracker :tea: :coffee:")
st.sidebar.markdown("#### Date Range Selection")

col1,col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(label="Start Date", value=dt(2023,1,1))
with col2:
    end_date = st.date_input(label="End Date", value=dt(2023,12,31))


#st.write(data)