import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time

#----------------------------------------------------------------------------#
# Page expands to ull width
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
col2, col3 = st.columns((2,1))
#----------------------------------------------------------------------------#
# Sidebar + Main panel
col1.header('Input Options')

## Sidebar - Currency price unit
currency_price_Unit = col1.selectbox('Select currency for price', ('USD', 'BTC'))

