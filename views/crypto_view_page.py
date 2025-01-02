import streamlit as st
from goldhand import *

@st.cache_data
def get_tw():
    return Tw()
tw = get_tw()

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
    else:
        return f"{round(number, 2)}"

@st.fragment
def crypto_dashboard():
    
    col1, col2, col3 = st.columns([2, 1.4, 2])
    with col1:
        with st.container(border=True):
            st.markdown("#### Explore detailed insights about your selected cryptocurrency.")
            selected_description = st.selectbox("", tw.crypto["base_currency_desc"])

    # Retrieve the selected ticker ID
    user_ticker = tw.crypto.loc[tw.crypto["base_currency_desc"] == selected_description, "base_currency"].values[0] + '-USD'

    # Data for the selected cryptocurrency
    crypto_data = tw.crypto.loc[tw.crypto["base_currency_desc"] == selected_description].iloc[0]

    with col2:
        with st.container(border=True):
            st.markdown("##### More info")

            tradingview_url = f"https://www.tradingview.com/chart/?symbol={user_ticker}"
            st.markdown(
                f'<a href="{tradingview_url}" target="_blank" style="text-decoration:none;">'
                f'<button style="background-color:#1E90FF; color:white; border:none; border-radius:5px; padding:10px 15px; font-size:16px;">'
                f'Open TradingView</button></a>',
                unsafe_allow_html=True,
            )

    # Second row: Display four metrics
    st.markdown("### Cryptocurrency Metrics")
    metrics = [
        {"label": "Market Capitalization", "value": f"${format_large_number(crypto_data['market_cap_calc'])}"},
        {"label": "24h Volume", "value": f"${format_large_number(crypto_data['24h_vol_cmc'])}"},
        {"label": "24h Change", "value": format_large_number(crypto_data["24h_close_change|5"])},
        {"label": "Circulating Supply", "value": format_large_number(crypto_data["circulating_supply"])},
        {"label": "Ticker", "value": crypto_data["ticker"]},
    ]

    col1, col2, col3, col4, col5 = st.columns(5)

    # Display metrics in their respective containers
    with col1:
        with st.container(border=True):
            st.metric(label=metrics[0]["label"], value=metrics[0]["value"])

    with col2:
        with st.container(border=True):
            st.metric(label=metrics[1]["label"], value=metrics[1]["value"])

    with col3:
        with st.container(border=True):
            st.metric(label=metrics[2]["label"], value=metrics[2]["value"])

    with col4:
        with st.container(border=True):
            st.metric(label=metrics[3]["label"], value=metrics[3]["value"])

    with col5:
        with st.container(border=True):
            st.metric(label=metrics[4]["label"], value=metrics[4]["value"])
    st.divider()

    # Third row: Cryptocurrency price evolution over the last year
    st.markdown("### Cryptocurrency Price Over the Last Year")
    with st.container(border=True):
        t = GoldHand(user_ticker)
        st.plotly_chart(t.plotly_last_year(tw.get_plotly_title(user_ticker)), use_container_width=False, theme=None)

crypto_dashboard()
