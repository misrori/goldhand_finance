from goldhand import *
import pandas as pd
import plotly.express as px
import streamlit as st


# Caching the Tw object to optimize performance
@st.cache_data(ttl=600)
def get_tw():
    tw = Tw()
    tw.stock['display_name'] = tw.stock['description'] + ' (' + tw.stock['name'] + ')'
    tw.crypto['display_name'] = tw.crypto['base_currency_desc'] + ' (' + tw.crypto['base_currency'] + ')'
    tw.crypto['market_cap'] = tw.crypto['market_cap_calc'].astype(float)    
    return tw
