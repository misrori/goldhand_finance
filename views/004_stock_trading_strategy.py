
import streamlit as st
from goldhand import *
import pandas as pd
from utils_data import get_tw
tw=get_tw()


def update_index():
    st.session_state.stt_current_index = int(tw.stock[tw.stock['display_name'] == st.session_state.sttstock].index[0])

# Initialize session state for sw_current_index
if "stt_current_index" not in st.session_state:
    st.session_state.stt_current_index = 0
    

@st.fragment
def show_strategy_tester():
    """Display the trading strategy tester interface."""

    # Introduction section
    st.title("Trading Strategies")
    st.write("Select a company and explore the results of various trading strategies applied to it.")

    # Layout: Company selector and number of days in a single row
    col1, col2, col3 = st.columns([2, 1, 4])

    with col1:
        with st.container(border=True):
            # Dropdown for selecting a company
            selected_description = st.selectbox(
                "Select a company:", 
                tw.stock["display_name"], 
                key="sttstock", 
                index=st.session_state.stt_current_index, 
                on_change=lambda: update_index()
                )
            company_name = tw.stock.loc[tw.stock["display_name"] == selected_description, "name"].values[0]

    with col2:
        with st.container(border=True):
            # Input for selecting the number of days
            ndays = st.number_input("Number of days:", min_value=1, max_value=10000, value=800, step=50)

    # Layout: Strategies displayed in a single row
    with col3:
        with st.container(border=True):
            # Radio buttons for selecting a trading strategy
            strategy = st.radio(
                "Select a strategy:",
                [
                    "Base Plot",
                    "Goldhand Line Plot",
                    "RSI Strategy",
                    "Goldhand Line Strategy",
                ],
                index=0,
                horizontal=True,  # Displayed in a horizontal row
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
        # Default values for thresholds if not using RSI strategy
        buy_threshold = 30
        sell_threshold = 70

    # Display strategy results
    if company_name:
        if strategy == "Base Plot":
            # Display a basic plot for the selected company
            t = GoldHand(company_name)
            fig = t.plotly_last_year(plot_title=tw.get_plotly_title(company_name), ndays=ndays)

        elif strategy == "Goldhand Line Plot":
            # Display a Goldhand line plot for the selected company
            t = GoldHand(company_name)
            fig = t.plot_goldhand_line(plot_title=tw.get_plotly_title(company_name), ndays=ndays)

        elif strategy == "RSI Strategy":
            # Display results for RSI strategy
            fig = show_indicator_rsi_strategy(
                ticker=company_name,
                buy_threshold=buy_threshold,
                sell_threshold=sell_threshold,
                plot_title=f"RSI Strategy for {company_name}",
                plot_height=1000,
                ndays=ndays
            )

        elif strategy == "Goldhand Line Strategy":
            # Display results for Goldhand Line strategy
            fig = show_indicator_goldhand_line_strategy(
                ticker=company_name,
                plot_title=f"Goldhand Line Strategy for {company_name}",
                plot_height=1000,
                ndays=ndays
            )

        else:
            st.error("Unknown strategy selected!")
            
        # Third row: Stock price chart
        col1, col2 = st.columns([1.5, 2])
        with col1: 
            st.markdown(f"### {strategy} for {selected_description}")
        with col2:
            label_of_next_button = f'Next: {tw.stock["display_name"][(st.session_state.stt_current_index + 1) % len(tw.stock)]}'

            if st.button(label_of_next_button):
                st.session_state.stt_current_index = (st.session_state.stt_current_index + 1) % len(tw.stock)
                st.rerun(scope="fragment")

        # Display the results
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True, theme=None)

    else:
        st.warning("Please select a company.")

# Run the strategy tester
show_strategy_tester()


                
#        elif strategy == "RSI Strategy":
#           
#            data = GoldHand(company_name).df
#            trade_res = Backtest( data, rsi_strategy, plot_title=tw.get_plotly_title(company_name),  buy_threshold=buy_threshold, sell_threshold=sell_threshold)
#            fig = trade_res.show_trades()
#            trade_df = trade_res.trades
#            summary_df = pd.DataFrame(trade_res.trades_summary, index=['Strategy summary']).T
#            
#            with st.container(border=True):
#                st.markdown("### Trades")
#                st.plotly_chart(fig, use_container_width=True, theme=None)
#            with st.container(border=True):
#                st.dataframe(trade_df)
#            with st.container(border=True):
#                st.dataframe(summary_df)
