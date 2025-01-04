import streamlit as st
from goldhand import *
import pandas as pd
import plotly.express as px

# Functions
def get_market_cap(ticker):
    """Retrieve the market capitalization for a given ticker."""
    return tw.stock[tw.stock['name'] == ticker]['market_cap_basic'].values[0]

def process_one_ticker(ticker):
    """Process data for a single ticker by calculating percentage change and market capitalization."""
    t = GoldHand(ticker).df
    t['percent_change'] = t['close'] / list(t['close'])[-1]
    t['market_cap'] = get_market_cap(ticker) * t['percent_change']
    return t

def get_plot(tickers):
    """Generate a line plot of market capitalization trends over time for selected tickers."""
    all_df = pd.concat(list(map(process_one_ticker, tickers)))
    df = all_df.sort_values(by=['date'])

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

    # Adjust layout for a white theme and bigger plot
    fig.update_layout(
        title_font_size=20,  # Adjust title font size
        font=dict(size=14),
        plot_bgcolor='white',
        height=900
    )
    return fig

# Caching the Tw object to optimize performance
@st.cache_data()
def get_tw():
    tw = Tw()
    return tw
tw = get_tw()


@st.fragment
def stock_compare_plot():
    """Display a stock comparison plot with market capitalization trends."""
    # Create the interface
    st.title("Stock Selector")
    st.write("Select multiple stocks to analyze their market capitalization trends.")

    # Select stocks using a multi-select dropdown
    selected_stocks = st.multiselect(
        "Choose stocks:",
        options=tw.stock["description"].tolist(),
        default=[]
    )

    # Generate the plot
    if st.button("Generate Plot"):
        # Retrieve IDs of the selected stocks
        selected_ids = [
            tw.stock.loc[tw.stock["description"] == stock, "name"].values[0]
            for stock in selected_stocks
        ]

        if selected_ids:
            with st.spinner("Generating plot..."):
                fig = get_plot(selected_ids)
                st.plotly_chart(fig, use_container_width=True, theme=None)
        else:
            st.warning("Please select at least one stock to generate the plot.")

stock_compare_plot()
