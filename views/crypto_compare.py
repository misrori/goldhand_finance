import streamlit as st
from goldhand import *
import pandas as pd
import plotly.express as px

# Functions
def get_market_cap(ticker):
    """Retrieve the market capitalization for a given cryptocurrency ticker."""
    return tw.crypto[tw.crypto['ticker'] == ticker]['market_cap_calc'].values[0]

def process_one_ticker(ticker):
    """Process data for a single cryptocurrency ticker."""
    t = GoldHand(ticker).df
    t['percent_change'] = t['close'] / list(t['close'])[-1]
    t['market_cap'] = get_market_cap(ticker) * t['percent_change']
    t['ticker'] = ticker
    return t


def get_crypto_comapare_plot(tickers):
    all_df = pd.concat(list(map(process_one_ticker, tickers)))
    df = all_df.sort_values(by=['date'])
    # Create the line plot
    fig = px.line(
        df,
        x='date',
        y='market_cap',
        color='ticker',
        title="Cryptocurrency Market Capitalization Trends Over Time",
        labels={
            "date": "Date",
            "market_cap": "Market Cap",
            "ticker": "Ticker"
        }
    )

    # Adjust layout for a clean theme and bigger plot
    fig.update_layout(
        title_font_size=20,
        font=dict(size=14),
        plot_bgcolor='white',
        height=900
    )
    return fig

# Caching the Tw object to optimize performance
@st.cache_data
def get_tw():
    return Tw()
tw = get_tw()

@st.fragment
def crypto_compare_plot():
    """Display a cryptocurrency comparison plot with market capitalization trends."""
    # Create the interface
    st.title("Cryptocurrency Selector")
    st.write("Select multiple cryptocurrencies to analyze their market capitalization trends.")

    # Select cryptocurrencies using a multi-select dropdown
    selected_cryptos = st.multiselect(
        "Choose cryptocurrencies:",
        options=tw.crypto["base_currency_desc"].tolist(),
        default=[]
    )
    
    
    # Generate the plot
    if st.button("Generate Plot"):
        # Retrieve IDs of the selected cryptocurrencies
        selected_ids = [
            tw.crypto.loc[tw.crypto["base_currency_desc"] == crypto, "base_currency"].values[0] +"-USD"
            for crypto in selected_cryptos
        ]
        if selected_ids:
            with st.spinner("Generating plot..."):
                fig = get_crypto_comapare_plot(selected_ids)
                st.plotly_chart(fig, use_container_width=True, theme=None, key="crypto_compare_plotly_plot")
        else:
            st.warning("Please select at least one cryptocurrency to generate the plot.")

crypto_compare_plot()
