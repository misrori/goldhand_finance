
import streamlit as st
from goldhand import *
import os
import streamlit as st

# Cache mappák elérési útja
streamlit_cache_dir = os.path.expanduser("__pycache__")



st.markdown("""
## 🌟 About This Project
Dive into the world of **stock market analysis**! This platform is designed to empower you with insightful tools to make informed decisions. Whether you're a seasoned investor or just starting out, our application offers something for everyone. 🚀

### 💡 Key Features:
- **Interactive Dashboards** 🖥️: Explore stocks, sectors, and industries with real-time insights.
- **Custom Strategies** 📊: Analyze your chosen stocks with cutting-edge strategies powered by the Goldhand Python package.
- **Trend Analysis** 🔍: Uncover performance trends in exciting fields like **Quantum Computing** and **Cybersecurity**.
- **News Aggregation** 📰: Stay updated with the latest news affecting the companies you're interested in.

### 🔧 Tools You'll Love:
- **Powerful Filters** 🔥: Filter stocks by market cap, sector, industry, or performance metrics like drawdowns from their peaks.
- **Advanced Visualizations** 📈: View elegant, interactive charts to guide your decisions.

### 🚀 Ready to Explore?
Navigate using the sidebar to discover our unique features and uncover new investment opportunities! 🌟

---
Designed and developed with ❤️ by Orsós Mihály and powered by the **Goldhand Python Package**.
""")




# Initialize session state variable to track execution
if "clear_cache_executed" not in st.session_state:
    st.session_state["clear_cache_executed"] = False

# Check and execute the code only once
if not st.session_state["clear_cache_executed"]:
    st.cache_data.clear()  # Clear cache
    st.cache_resource.clear()
    st.session_state["clear_cache_executed"] = True  # Mark as executed
    st.rerun()  

# manual rerun
if st.button("Clear cache and rerun"):
    st.cache_data.clear()  # Clear cache
    st.session_state["clear_cache_executed"] = True  # Mark as executed
    st.cache_resource.clear()
    st.rerun()


