
import streamlit as st
from goldhand import *
from utils_stock_data import *

tw=get_tw()
with st.spinner("Generating plot..."):
    fig = get_market_plot()
    st.plotly_chart(fig, use_container_width=True, theme=None)




