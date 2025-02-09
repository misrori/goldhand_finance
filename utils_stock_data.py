import streamlit as st
from goldhand import *
import pandas as pd
import plotly.express as px
from utils_data import get_tw

tw=get_tw()


def format_large_number(number):
    """
    Formats numbers in a human-readable way (e.g., 1B, 1M, 1T).
    """
    if number >= 1_000_000_000_000:
        return f"{round(number / 1_000_000_000_000, 2)}T"  # Trillions
    elif number >= 1_000_000_000:
        return f"{round(number / 1_000_000_000, 2)}B"  # Billions
    elif number >= 1_000_000:
        return f"{round(number / 1_000_000, 2)}M"  # Millions
    elif number >= 1_000:
        return f"{round(number / 1_000, 2)}K"
    else:
        return f"{round(number, 2)}"


def get_market_cap(ticker):
    """Retrieve the market capitalization for a given ticker."""
    return (tw.stock[tw.stock['name'] == ticker]['market_cap_basic'].values[0])

def process_one_ticker(ticker, view="market_cap", date_range=None):
    """Process data for a single ticker by calculating the desired metric."""
    t = GoldHand(ticker).df
    t['percent_change'] = t['close'] / list(t['close'])[-1]
    t['market_cap'] = get_market_cap(ticker) * t['percent_change']
    t['market_cap_formatted'] = t['market_cap'].apply(format_large_number)
    t['ticker_name'] = tw.stock[tw.stock['name'] == ticker]['display_name'].values[0]
    if view == "Market Capitalization":
        return t
    elif view == "Percentage Change":
        
        t['date'] = pd.to_datetime(t['date'])
        if date_range:
            start_date, end_date = date_range
            t = t[(t['date'] >= start_date) & (t['date'] <= end_date)]
            #percentage change from the first price
            t['percent_change'] = ((t['close'] / t['close'].iloc[0] ) -1 )*100
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
                "market_cap_formatted": "Market Cap",
                "ticker": "Ticker",
                "ticker_name": "Company Name"
            },
            hover_data={
                'ticker': True,                  # Include the ticker in the hover text
                'ticker_name': True,             # Include the company name in the hover text
                'market_cap_formatted': True,    # Include the formatted market_cap
                'market_cap': False,              # Do not Include the raw market_cap
                'date': '|%Y-%m-%d'              # Format date
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
                "market_cap_formatted": "Market Cap",
                "ticker": "Ticker",
                "ticker_name": "Company Name"
            },
            hover_data={
                'ticker': True,                  # Include the ticker in the hover text
                'ticker_name': True,             # Include the company name in the hover text
                'percent_change': ':.2f',        # Format percent_change with two decimal places
                'market_cap_formatted': True,    # Include the formatted market_cap
                'market_cap': False,              # Do not Include the raw market_cap
                'date': '|%Y-%m-%d'              # Format date
            }
        )

    fig.update_layout(
        title_font_size=20,
        font=dict(size=14),
        plot_bgcolor='white',
        height=900
    )
    return fig



def custom_colorscale(value):
    if value <= -15:
        return -15  # Mínusz 15%-nál a legpirosabb
    elif value >= 15:
        return 15  # Plusz 15%-nál a legzöldebb
    else:
        return value  # Minden ami -15 és 15 között van, megtartja az eredeti értéket
        


def get_market_plot():
     

    data = tw.stock[['sector', 'industry', 'display_name', 'name', 'market_cap_basic', 'change']]
    data['market_cap_basic'] = data['market_cap_basic'].astype(float)
    data['change'] = data['change'].astype(float)
    data['change_original'] = data['change']
    data['change'] = data['change'].apply(custom_colorscale)
    data['market_cap_text'] = data['market_cap_basic'].apply(format_large_number)
    data['Change_text'] = data['change_original'].apply(lambda x: f"{x:.2f}%")  # Két tizedesjegy

    # Oszlopok átnevezése
    data.columns = ['Sector', 'Industry', 'Name', 'Stock', 'Market_Cap', 'Change', 'change_original', 'market_cap_text' , 'Change_text']

    data['Color'] = data['Change'].apply(custom_colorscale)

    fig = px.treemap(
        data,
        path=['Sector', 'Industry', 'Stock'],  # Hierarchia, ID helyett Display Name használata
        values='Market_Cap',  # Méret a piaci kapitalizáció
        color='Change',  # Szín a változás alapján
        color_continuous_scale='RdYlGn',  # Piros-zöld skála
        title='Stock Market Heatmap',
        labels={
        "market_cap_text": "Market Cap",
        },
        hover_data={
            'Name': True,
            'Sector': True,
            'Industry': True,
            'market_cap_text': True,
            'Change_text': True,
        }
    )

    fig.data[0].update(
        hovertemplate='Name=%{customdata[0]}<br>Sector=%{customdata[1]}<br>Industry=%{customdata[2]}<br>Market Cap=%{customdata[3]}<br>Change_text=%{customdata[4]}'
    )

    fig.update_layout(height=2000, coloraxis_showscale=False)
    return (fig)

