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

st.title('Crypto Top Ten Web App')
st.markdown("""
This app retrieves cryptocurrecy prices for the top 10 cryptocurrencies

""")

#----------------------------------------------------------------------------#
# About

expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** pandas, streamlit, numpy, matplotlib, seaborn, json, time, datetime, requests
* **Data source:** [FTX](https://ftx.com/).
""")


#----------------------------------------------------------------------------#
# page layout
## Divide page to 3 columns
col1 = st.sidebar
col3, col3 = st.columns((2,1))
#----------------------------------------------------------------------------#
# Sidebar + Main panel
col1.header('Currency Select')

## Sidebar - Currency price unit
#currency_price_Unit = col1.selectbox('Select currency for price', ('USD', 'BTC'))

## Sidebar - Cryptocurrency selections

@st.cache
def load_data():
    marketsDF = pd.DataFrame(exchange.load_markets())
    marketscut = marketsDF.drop(marketsDF.index[4:25])
    return marketscut

def get_info_currency(symbol):
    currency = pd.DataFrame.from_dict(markets[symbol]['info'], orient='index')
    return currency

markets = load_data()



selected_coin = col1.radio('Cryptocurrency 👇',
                ['BTC', 'ETH', 'USDT', 'BNB', 'XRP', 'SOL', 'DOGE', 'DOT', 'MATIC','TRX' ], 
                )

if selected_coin == 'BTC':
    col3.dataframe(get_info_currency('BTC/USD'))
elif selected_coin == 'ETH':
    col3.dataframe(get_info_currency('ETH/USD'))
elif selected_coin == 'USDT':
    col3.dataframe(get_info_currency('USDT/USD'))
elif selected_coin == 'BNB':
    col3.dataframe(get_info_currency('BNB/USD'))
elif selected_coin == 'XRP':
    col3.dataframe(get_info_currency('XRP/USD'))
elif selected_coin == 'SOL':
    col3.dataframe(get_info_currency('SOL/USD'))
elif selected_coin == 'DOGE':
    col3.dataframe(get_info_currency('DOGE/USD'))
elif selected_coin == 'DOT':
    col3.dataframe(get_info_currency('DOT/USD'))
elif selected_coin == 'MATIC':
    col3.dataframe(get_info_currency('MATIC/USD'))
elif selected_coin == 'TRX':
    col3.dataframe(get_info_currency('TRX/USD'))
else:
    pass
