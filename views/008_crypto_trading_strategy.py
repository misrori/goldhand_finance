# Write the Streamlit app to a file
import streamlit as st
from goldhand import *

# Caching the Tw object to optimize performance
@st.cache_data()
def get_tw():
    tw = Tw()
    return tw
tw = get_tw()


@st.fragment
def show_crypto_strategy_tester():

    # Introduction section
    st.title("Cryptocurrency Trading Strategies")
    st.write("Select a cryptocurrency and explore the results of various trading strategies applied to it.")

    # Layout: Cryptocurrency selector and number of days in one row
    col1, col2, col3 = st.columns([2, 1, 4])

    with col1:
        with st.container(border=True):
            selected_description = st.selectbox("Select a cryptocurrency:", tw.crypto["base_currency_desc"])
            crypto_name = tw.crypto.loc[tw.crypto["base_currency_desc"] == selected_description, "base_currency"].values[0] + '-USD'

    with col2:
        with st.container(border=True):
            ndays = st.number_input("Number of days:", min_value=1, max_value=5000, value=800, step=10)

    # Layout: Strategies in one row
    with col3:
        with st.container(border=True):
            strategy = st.radio(
                "Select a strategy:",
                [
                    "Base Plot",
                    "Goldhand Line Plot",
                    "RSI Strategy",
                    "Goldhand Line Strategy",
                ],
                index=0,
                horizontal=True,  # Displayed in one line
            )

    # RSI Strategy parameters
    if strategy == "RSI Strategy":
        st.divider()
        st.markdown("### RSI Parameters")
        col4, col5 = st.columns(2)
        with col4:
            buy_threshold = st.slider("Buy Threshold:", min_value=10, max_value=50, value=30, step=1)
        with col5:
            sell_threshold = st.slider("Sell Threshold:", min_value=60, max_value=100, value=70, step=1)
    else:
        buy_threshold = 30
        sell_threshold = 70

    # Displaying the results of the strategies
    if crypto_name:
        if strategy == "Base Plot":
            t = GoldHand(crypto_name)
            fig = t.plotly_last_year(plot_title=tw.get_plotly_title(crypto_name), ndays=ndays)
        elif strategy == "Goldhand Line Plot":
            t = GoldHand(crypto_name)
            fig = t.plot_goldhand_line(plot_title=tw.get_plotly_title(crypto_name), ndays=ndays)
        elif strategy == "RSI Strategy":
            fig = show_indicator_rsi_strategy(
                ticker=crypto_name,
                buy_threshold=buy_threshold,
                sell_threshold=sell_threshold,
                plot_title=f"RSI Strategy for {crypto_name}",
                plot_height=1000,
                ndays=ndays
            )
        elif strategy == "Goldhand Line Strategy":
            fig = show_indicator_goldhand_line_strategy(
                ticker=crypto_name,
                plot_title=f"Goldhand Line Strategy for {crypto_name}",
                plot_height=1000,
                ndays=ndays
            )
        else:
            st.error("Unknown strategy selected!")

        # Displaying the results
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True, theme=None)
    else:
        st.warning("Please enter a cryptocurrency name.")

show_crypto_strategy_tester()