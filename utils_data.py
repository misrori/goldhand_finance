from goldhand import *
import pandas as pd
import plotly.express as px
import streamlit as st
import datetime

# Caching the Tw object to optimize performance
@st.cache_data(ttl=120)
def get_tw():
    tw = Tw()
    print(datetime.datetime.now())
    print(tw.stock.head())
    tw.stock['display_name'] = tw.stock['description'] + ' (' + tw.stock['name'] + ')'
    tw.crypto['display_name'] = tw.crypto['base_currency_desc'] + ' (' + tw.crypto['base_currency'] + ')'
    tw.crypto['market_cap'] = tw.crypto['market_cap_calc'].astype(float)    
    return tw


