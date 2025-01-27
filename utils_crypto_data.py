import streamlit as st
from goldhand import *
import pandas as pd
import plotly.express as px
from utils_data import get_tw

tw=get_tw()


# Functions
def get_market_cap_crypto(ticker):
    return (tw.crypto[tw.crypto['ticker'] == ticker]['market_cap'].values[0])

def process_one_ticker_crypto(ticker, view="market_cap", date_range=None):
    print(ticker)
    """Process data for a single ticker by calculating the desired metric."""
    t = GoldHand(ticker).df
    if view == "Market Capitalization":
        t['percent_change'] = t['close'] / list(t['close'])[-1]
        t['market_cap'] = get_market_cap_crypto(ticker) * t['percent_change']
        return t
    elif view == "Percentage Change":
        t['date'] = pd.to_datetime(t['date'])
        if date_range:
            start_date, end_date = date_range
            t = t[(t['date'] >= start_date) & (t['date'] <= end_date)]
            #percentage change from the first price
            t['percent_change'] = ((t['close'] / t['close'].iloc[0] ) -1 )*100
        return t

def get_crypto_compare_plot(tickers, view="market_cap", date_range=None):
    all_df = pd.concat(list(map(lambda t: process_one_ticker_crypto(t, view, date_range), tickers)))
    df = all_df.sort_values(by=['date'])
    if view == "Market Capitalization":
    # Create the line plot
        fig = px.line(
            df,
            x='date',
            y='market_cap',
            color='ticker',
            title="Market Capitalization by Ticker Over Time",
            labels={
                "date": "Date",
                "market_cap": "Market Cap",
                "ticker": "Ticker"
            }
        )
        
    elif view == "Percentage Change":
        fig = px.line(
            df,
            x='date',
            y='percent_change',
            color='ticker',
            title="Percent Change in Price by Ticker Over Time",
            labels={
                "date": "Date",
                "percent_change": "Percent Change",
                "ticker": "Ticker"
            }
        )

    fig.update_layout(
        title_font_size=20,
        font=dict(size=14),
        plot_bgcolor='white',
        height=900
    )
    return fig



