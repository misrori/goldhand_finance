import streamlit as st
from goldhand import *

st.set_page_config( layout="wide", page_title="Goldhand Finance",page_icon="📊",)


# --- INTRO ---
about_page = st.Page(
    "views/introduction.py",
    title="About this app",
    icon=":material/account_circle:",
    default=True,
)

st_infos_page = st.Page(
    "views/strategy_infos.py",
    title="Strategies info",
    icon=":material/trending_up:",
)

# --- STOCK ---
stock_view_page = st.Page(
    "views/stock_view_page.py",
    title="Stock View",
    icon=":material/bar_chart:",
)

stock_trading_strategy_page = st.Page(
    "views/stock_trading_strategy.py",
    title="Stock Trading Strategy",
    icon=":material/bar_chart:",
)

stock_compare_page = st.Page(
    "views/stock_compare.py",
    title="Stock compare",
    icon=":material/bar_chart:",
)

# --- CRYPTO ---

crypto_view_page = st.Page(
    "views/crypto_view_page.py",
    title="Crypto View",
    icon=":material/bar_chart:",
)

crypto_trading_strategy_page = st.Page(
    "views/crypto_trading_strategy.py",
    title="Crypto Trading Strategy",
    icon=":material/bar_chart:",
)

crypto_compare_page = st.Page(
    "views/crypto_compare.py",
    title="Crypto compare",
    icon=":material/bar_chart:",
)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [about_page, st_infos_page],
        "Stocks": [stock_view_page, stock_trading_strategy_page, stock_compare_page],
        "Crypto": [crypto_view_page, crypto_trading_strategy_page, crypto_compare_page],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo(
    'https://i.ibb.co/Pgw52bM/Screenshot-from-2024-12-26-09-41-17-removebg-preview.png',
    link="https://streamlit.io/gallery",
    size="large")

st.sidebar.markdown("Made with ❤️ by [Goldhandfinance](https://youtube.com/@goldhandfinance)")


# --- RUN NAVIGATION ---
pg.run()

