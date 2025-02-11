import streamlit as st
from goldhand import *
import pandas as pd
import plotly.express as px
from utils_data import get_tw
from utils_stock_data import *


@st.fragment
def stock_compare_plot():
    """Display a stock comparison plot with market capitalization trends."""
    # Create the interface
    tw=get_tw()
    
    st.title("Stock Selector")
    st.write("Select multiple stocks to analyze their market capitalization trends.")

    # Select stocks using a multi-select dropdown
    with st.container(border=True):
        selected_stocks = st.multiselect(
            "Choose stocks:",
            options=tw.stock["display_name"].tolist(),
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

stock_compare_plot()
