import streamlit as st
from goldhand import *
import pandas as pd
import plotly.express as px
from utils_data import get_tw

tw=get_tw()


def get_market_cap(ticker):
    """Retrieve the market capitalization for a given ticker."""
    return (tw.stock[tw.stock['name'] == ticker]['market_cap_basic'].values[0])

def process_one_ticker(ticker, view="market_cap", date_range=None):
    """Process data for a single ticker by calculating the desired metric."""
    t = GoldHand(ticker).df
    if view == "Market Capitalization":
        t['percent_change'] = t['close'] / list(t['close'])[-1]
        t['market_cap'] = get_market_cap(ticker) * t['percent_change']
        t['ticker_name'] = tw.stock[tw.stock['name'] == ticker]['display_name'].values[0]
        return t
    elif view == "Percentage Change":
        
        t['date'] = pd.to_datetime(t['date'])
        if date_range:
            start_date, end_date = date_range
            t = t[(t['date'] >= start_date) & (t['date'] <= end_date)]
            #percentage change from the first price
            t['percent_change'] = ((t['close'] / t['close'].iloc[0] ) -1 )*100
            t['ticker_name'] = tw.stock[tw.stock['name'] == ticker]['display_name'].values[0]
        return t


def get_plot(tickers, view="market_cap", date_range=None):
    all_df = pd.concat(list(map(lambda t: process_one_ticker(t, view, date_range), tickers)))
    df = all_df.sort_values(by=['date'])
    # add the company name on the hower text

    
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
                "ticker": "Ticker",
                "ticker_name": "Company Name"
            },
            hover_data={
                'ticker': True,             # Include the ticker in the hover text
                'ticker_name': True,        # Include the company name in the hover text
                'market_cap': ':.2f',       # Format market_cap with two decimal places
                'date': '|%Y-%m-%d'         # Format date
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
                "ticker": "Ticker",
                "ticker_name": "Company Name"
            },
                        hover_data={
                'ticker': True,             # Include the ticker in the hover text
                'ticker_name': True,        # Include the company name in the hover text
                'percent_change': ':.2f',       # Format market_cap with two decimal places
                'date': '|%Y-%m-%d'         # Format date
            } 
        )

    fig.update_layout(
        title_font_size=20,
        font=dict(size=14),
        plot_bgcolor='white',
        height=900
    )
    return fig

