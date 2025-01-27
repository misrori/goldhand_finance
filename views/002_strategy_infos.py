import streamlit as st


# Tabs for strategy explanations
tab1, tab2, tab3, tab4 = st.tabs(["📈 RSI Strategy", "🔑 Goldhand Line", "📊 Momentum Strategy", "💰 Mean Reversion"])

with tab1:
    st.markdown("""
    ### RSI Strategy
    The **Relative Strength Index (RSI)** strategy identifies overbought and oversold conditions in the market:
    - **Buy** when RSI < 30 (oversold).
    - **Sell** when RSI > 70 (overbought).
    This helps you spot potential trend reversals and optimize entry/exit points in trades.
    """)

with tab2:
    st.markdown("""
    ### Goldhand Line Strategy
    The **Goldhand Line Strategy** leverages advanced predictive models to identify potential support and resistance levels.
    - **Buy signals** are generated near predicted support levels.
    - **Sell signals** occur at predicted resistance levels.
    This strategy is highly effective for trending markets.
    """)

with tab3:
    st.markdown("""
    ### Momentum Strategy
    The **Momentum Strategy** focuses on stocks that are trending strongly in one direction.
    - **Buy** when prices show strong upward momentum.
    - **Sell** when momentum slows or reverses.
    This strategy is ideal for capturing profits during sustained trends.
    """)

with tab4:
    st.markdown("""
    ### Mean Reversion Strategy
    The **Mean Reversion Strategy** assumes that prices eventually revert to their historical averages.
    - **Buy** when prices are significantly below the average.
    - **Sell** when prices exceed the average.
    This approach is effective in range-bound markets with less volatility.
    """)


