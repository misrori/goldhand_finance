
import streamlit as st
from goldhand import *
from utils_stock_data import *


@st.fragment
def stock_heat_map():
    
    tw = get_tw()

    with st.container(border=True):
        st.markdown("## Market Performance Heatmap")
        col1, col2 = st.columns([2, 1])
        with col1:
            heat_map_time = st.radio(
                "### Select timeframe:",
                [
                    "One day",
                    "One week",
                    "One month",
                    "Three months",
                    "Six months",
                    "One year",
                ],
                index=0,
                horizontal=True,  # Displayed in a horizontal row
            )
        
            
            time_frame_dict = {
                "One day": "change",
                "One week": "Perf.W",
                "One month": "Perf.1M",
                "Three months": "Perf.3M",
                "Six months": "Perf.6M",
                "One year": "Perf.Y",
            }
            
            selelcted_change_col = time_frame_dict[heat_map_time] 
        with col2:
            if st.button("Refresh"):
                st.cache_data.clear()  # Clear cache
                st.session_state["clear_cache_executed"] = True  # Mark as executed
                st.cache_resource.clear()
                st.rerun()


    with st.spinner("Generating plot..."):
        fig = get_market_plot(tw, selelcted_change_col)
        st.plotly_chart(fig, use_container_width=True, theme=None)


stock_heat_map()