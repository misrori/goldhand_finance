import streamlit as st
from goldhand import *
import pandas as pd
import plotly.express as px

# Functions
def get_market_cap(ticker):
    """Retrieve the market capitalization for a given ticker."""
    return tw.stock[tw.stock['name'] == ticker]['market_cap_basic'].values[0]

def process_one_ticker(ticker, view="market_cap", date_range=None):
    """Process data for a single ticker by calculating the desired metric."""
    t = GoldHand(ticker).df
    if view == "Market Capitalization":
        t['percent_change'] = t['close'] / list(t['close'])[-1]
        t['market_cap'] = get_market_cap(ticker) * t['percent_change']
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

# Caching the Tw object to optimize performance
@st.cache_data()
def get_tw():
    tw = Tw()
    tw.stock['display_name'] = tw.stock['description'] + ' (' + tw.stock['name'] + ')'
    return tw
tw = get_tw()


@st.fragment
def cybersecurity_stock_compare_plot():
    """Display a stock comparison plot with market capitalization trends."""
    # Create the interface
    st.title("Stock Selector")
    st.write("Select multiple stocks to analyze their market capitalization trends.")

    # Select stocks using a multi-select dropdown
    with st.container(border=True):
        selected_stocks = st.multiselect(
            "Choose stocks:",
            options=tw.stock["display_name"].tolist(),
            default=[]
        )
    st.write("Selected stocks: ", '","'.join(selected_stocks))
    
    col1, col2 = st.columns([1.4, 2])
    with col1:   
        with st.container(border=True):
            view_option = st.radio(
            "View data by:",
            options=["Market Capitalization", "Percentage Change"],
            index=0, horizontal=True
            )
    with col2:
        with st.container(border=True):
            date_range = None
            if view_option == "Percentage Change":
                time_range = st.radio(
                    "Select time range:",
                    options=["1 Month", "3 Months", "6 Months", "1 Year", "3 Years", "Custom Date Range"], horizontal=True, index=3,
                )
                if time_range == "Custom Date Range":
                    start, end = st.columns(2)
                    with start:
                        start_date = st.date_input("Start date", pd.Timestamp.now() - pd.Timedelta(days=365))
                    with end:  
                        end_date = st.date_input("End date")
                    date_range = (str(start_date), str(end_date))
                else:
                    # Calculate date range based on selected option
                    date_map = {
                        "1 Month": 30,
                        "3 Months": 90,
                        "6 Months": 180,
                        "1 Year": 365,
                        "3 Years": 1095
                    }
                    days = date_map[time_range]
                    date_range = (pd.Timestamp.now() - pd.Timedelta(days=days)).strftime('%Y-%m-%d'), pd.Timestamp.now().strftime('%Y-%m-%d')

            
    # Generate the plot
    if st.button("Generate Plot"):
        # Retrieve IDs of the selected stocks
        selected_ids = [
            tw.stock.loc[tw.stock["display_name"] == stock, "name"].values[0]
            for stock in selected_stocks
        ]

        if selected_ids:
            with st.spinner("Generating plot..."):
                fig = get_plot(selected_ids, view=view_option, date_range=date_range)
                st.plotly_chart(fig, use_container_width=True, theme=None)
        else:
            st.warning("Please select at least one stock to generate the plot.")

cybersecurity_stock_compare_plot()
