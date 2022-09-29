from unittest.loader import VALID_MODULE_NAME
import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time
import ccxt
from datetime import datetime
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Use ccxt Criptocurrency Exchange Trading Library
exchange = ccxt.ftx ()
exchange.enableRateLimit = True  # enable

#----------------------------------------------------------------------------#
# Page expands to full width
st.set_page_config(layout="wide")
#----------------------------------------------------------------------------#
# Title

image = Image.open('./images/logo.jpg')

st.image(image, width=300)

#st.title('Crypto Top Ten Web App')
st.markdown("""
This app retrieves cryptocurrency prices for the top 10 cryptocurrencies

""")

#----------------------------------------------------------------------------#
# About

expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** pandas, streamlit, ccxt, numpy, plotly, matplotlib, seaborn, json, time, datetime, requests, PIL
* **Data source:** [FTX](https://ftx.com/).
* **Trading Library:** [ccxt](https://github.com/ccxt/ccxt)
* This application uses ccxt library to get information from FTX about ten cryptocurrencies
  considered by the author as the most relevant in the crypto market and resume basis
  information for analysis, visualization and currency convertion.
""")


#----------------------------------------------------------------------------#
# page layout
## Divide page to 3 columns
col1 = st.sidebar
col2, col3 = st.columns((2,1))
#----------------------------------------------------------------------------#
# Sidebar + Main panel
col1.header('Currency Select')

## Sidebar - Currency price unit
#currency_price_Unit = col1.selectbox('Select currency for price', ('USD', 'BTC'))

## Sidebar - Cryptocurrency selections

#----------------------------------------------------------------------------#
# Functions
@st.cache
def load_data_markets():
    marketsDF = pd.DataFrame(exchange.load_markets())
    marketscut = marketsDF.drop(marketsDF.index[4:25])
    return marketscut

@st.cache
def load_historical_data(symbol):
    hd = pd.DataFrame(exchange.fetch_ohlcv(symbol), 
    columns=['Date','Open','High','Low','Close','Volume'])
    hd['Date'] = (hd['Date']/1000)
    hd['Date'] = pd.to_datetime(hd['Date'], unit='s')
    hd['MA'] = hd['Close'].rolling(15).mean()
    return hd

def currency_df(symbol):
    currency = pd.DataFrame.from_dict(markets[symbol]['info'], orient='index')
    return currency

def get_candlestick_chart(hd: pd.DataFrame, symbol):

    # Create a graph object
    fig = go.Figure()

    # Set up the layout
    fig.update_layout(
        title = {
            'text' : f"{symbol}",
            'x': 0.5,
            'xanchor':'center'  
        },
        xaxis_title = "Date",
        yaxis_title = "Price",
        xaxis_rangeslider_visible = False
    )

    # Add candlestick chart 
    fig.add_trace(
        go.Candlestick(
            x=hd['Date'],
            open=hd['Open'],
            high=hd['High'],
            low=hd['Low'],
            close=hd['Close']
        )
    )
    return fig

# Show the information corresponding to the crypto data chosen
def make_stuff(symbol):
    hd = load_historical_data(symbol)
    col2.plotly_chart(get_candlestick_chart(hd,symbol)) 
    df = currency_df(symbol)
    currency_dict = markets[symbol]['info']
    col1.metric("Price Change 1h", currency_dict['price'], currency_dict['change1h'])
    col1.metric('Price Change 24h', currency_dict['price'], currency_dict['change24h'])
    col1.header('Volume USD 24h')
    col1.subheader(currency_dict['volumeUsd24h'])
    col3.dataframe(df)
#----------------------------------------------------------------------------#

# Get Markets DataFrame full
markets = load_data_markets()


# List of our preferred currencies for the col1 sidebar
selected_coin = col1.radio('Cryptocurrency 👇',
                ['BTC', 'ETH', 'BNB', 'XRP', 'SOL', 'DOGE', 'DOT', 'MATIC','TRX', 'LTC' ], 
                )

if selected_coin == 'BTC':
    symbol = 'BTC/USD'
    make_stuff(symbol) 
elif selected_coin == 'ETH':
    symbol= 'ETH/USD'
    make_stuff(symbol) 
elif selected_coin == 'BNB':
    symbol = "BNB/USD"
    make_stuff(symbol) 
elif selected_coin == 'XRP':
    symbol = "XRP/USD"
    make_stuff(symbol)
elif selected_coin == 'SOL':
    symbol = "SOL/USD"
    make_stuff(symbol)
elif selected_coin == 'DOGE':
    symbol = "DOGE/USD"
    make_stuff(symbol)
elif selected_coin == 'DOT':
    symbol = "DOT/USD"
    make_stuff(symbol)
elif selected_coin == 'MATIC':
    symbol = "MATIC/USD"
    make_stuff(symbol)
elif selected_coin == 'TRX':
    symbol = "TRX/USD"
    make_stuff(symbol)
elif selected_coin == 'LTC':
    symbol = 'LTC/USD'
    make_stuff(symbol) 
else:
    symbol = 'BTC/USD'
    make_stuff(symbol)


col2.write('Currency Calculator')
value = float(col2.number_input('Enter Currency value:'))
df = currency_df(symbol)
currency_dict = markets[symbol]['info']
price_now = float(currency_dict['price'])
value_to_USD = value * price_now
col2.write(value)
col2.write(selected_coin)
col2.text('is equivalent to:')
col2.write(value_to_USD)
col2.write('USD')

expander_bar = st.expander("App Data Report")
expander_bar.markdown("""
**Steps to get the Information:**
1. Using CCXT library when opening the application the function load_data_markets() loads a dataframe with the information
of all cryptocurrencies managed in the exchange FTX.

2. By default the BTC currency information is shown in the 3 columns in which the application is divided.

3. There is another function load_historical_data() to load OHLCV info in other dataframe which is used to show the candlestick chart.
""")