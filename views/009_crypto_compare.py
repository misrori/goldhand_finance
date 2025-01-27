import streamlit as st
from goldhand import *
import pandas as pd
import plotly.express as px
from utils_data import get_tw
from utils_crypto_data import *

tw=get_tw()




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
        # Retrieve IDs of the selected cryptocurrencies
        selected_ids = [
            tw.crypto.loc[tw.crypto["base_currency_desc"] == crypto, "base_currency"].values[0] +"-USD"
            for crypto in selected_cryptos
        ]
        if selected_ids:
            with st.spinner("Generating plot..."):
                fig = get_crypto_compare_plot(selected_ids, view_option, date_range)
                st.plotly_chart(fig, use_container_width=True, theme=None, key="crypto_compare_plotly_plot")
        else:
            st.warning("Please select at least one cryptocurrency to generate the plot.")

crypto_compare_plot()
