import streamlit as st
from goldhand import *

from utils_data import get_tw

tw=get_tw()



def update_index():
    st.session_state.sw_current_index = int(tw.stock[tw.stock['display_name'] == st.session_state.swstock].index[0])

# Initialize session state for sw_current_index
if "sw_current_index" not in st.session_state:
    st.session_state.sw_current_index = 0
    
    

@st.fragment
def stock_dashboard():
    """Stock Dashboard for displaying stock details and visualizations."""

    # First row: Dropdown menu for stock selection and additional info
    col1, col2, col3,  = st.columns([2, 1.4, 1.3], vertical_alignment="center")
    with col1:
        with st.container(border=True):
            st.markdown("##### Select a Stock")
            selected_description = st.selectbox(
                "", 
                tw.stock["display_name"], 
                key="swstock",
                index=st.session_state.sw_current_index, 
                on_change=lambda: update_index()
            )
            



    #user_ticker = tw.stock.loc[tw.stock["display_name"] == selected_description, "name"].values[0]
    #company_data = tw.stock.loc[tw.stock["display_name"] == selected_description].iloc[0]
    user_ticker = tw.stock.loc[st.session_state.sw_current_index, "name"]
    company_data = tw.stock.loc[st.session_state.sw_current_index]
    

    with col2:
        with st.container(border=True):
            st.markdown("##### More Info")
            tradingview_url = f"https://www.tradingview.com/chart/?symbol={user_ticker}"
            st.markdown(
                f'<a href="{tradingview_url}" target="_blank" style="text-decoration:none;">'
                f'<button style="background-color:#1E90FF; color:white; border:none; border-radius:5px; padding:10px 15px; font-size:16px;">'
                f'Open TradingView</button></a>',
                unsafe_allow_html=True,
            )

    # Second row: Displaying stock metrics
    with st.expander('### Stock Metrics', expanded=True):
        metrics = [
            {"label": "Price", "value": round(company_data["close"], 2)},
            {"label": "Price-to-Earnings (P/E)", "value": round(company_data["price_earnings_ttm"], 2)},
            {"label": "52-Week High", "value": f"${round(company_data['price_52_week_high'], 2)}"},
            {"label": "52-Week Low", "value": f"${round(company_data['price_52_week_low'], 2)}"},
            {"label": "RSI", "value": int(company_data["RSI7"])},
        ]

        col1, col2, col3, col4, col5 = st.columns(5)

        # Displaying metrics in containers
        for col, metric in zip([col1, col2, col3, col4, col5], metrics):
            with col:
                with st.container(border=True):
                    st.metric(label=metric["label"], value=metric["value"])

        st.divider()
 

    # Third row: Stock price chart
    col1, col2 = st.columns([1.5, 2])
    with col1: 
        st.markdown("### Stock Price Over the Last Year")
    with col2:
        label_of_next_button = f'Next: {tw.stock["display_name"][(st.session_state.sw_current_index + 1) % len(tw.stock)]}'

        if st.button(label_of_next_button):
            st.session_state.sw_current_index = (st.session_state.sw_current_index + 1) % len(tw.stock)
            st.rerun(scope="fragment")
        
    with st.container(border=True):
        t = GoldHand(user_ticker)
        st.plotly_chart(t.plotly_last_year(tw.get_plotly_title(user_ticker)), use_container_width=False, theme=None)

    # Fourth row: Sector and industry analysis plots
    st.divider()
    st.markdown("### Sector and Industry Location Analysis")
    col5, col6 = st.columns(2)

    with col5:
        st.plotly_chart(tw.get_sec_plot(user_ticker), use_container_width=True)

    with col6:
        st.plotly_chart(tw.get_ind_plot(user_ticker), use_container_width=True)

    st.divider()

# Run the stock dashboard
stock_dashboard()
