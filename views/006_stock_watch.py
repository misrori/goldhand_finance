import streamlit as st
import pandas as pd
from goldhand import *

@st.cache_data()
def get_tw():
    tw = Tw()
    tw.stock['display_name'] = tw.stock['description'] + ' (' + tw.stock['name'] + ')'
    return tw
tw = get_tw()


@st.cache_data()
def get_money_data():
    df = pd.read_csv('https://raw.githubusercontent.com/misrori/money_flow/refs/heads/main/last_stocks_update.csv')
    df =pd.merge(df, tw.stock[['name', 'description']], left_on='ticker', right_on='name', how='left')
    return df

stock_moves = get_money_data()

@st.fragment
def show_stock_watch():
    # Define a dictionary for user-friendly descriptions
    column_descriptions = {
        'sector': 'Sector of the company',
        'industry': 'Industry of the company',
        'diff_sma50': 'Difference from 50-day Simple Moving Average',
        'diff_sma100': 'Difference from 100-day Simple Moving Average',
        'diff_sma200': 'Difference from 200-day Simple Moving Average',
        'diff_upper_bb': 'Difference from Upper Bollinger Band',
        'diff_lower_bb': 'Difference from Lower Bollinger Band',
        'ghl_status': 'Goldhand status',
        'ghl_color': 'Goldhand color',
        'ghl_days_since_last_change': 'Days since last Goldhand change',
        'ghl_change_percent_from_last_change': 'Percentage change since last Goldhand change',
        'rsi':'Relative Strength Index',
        'rsi_status': 'RSI strategy status',
        'rsi_days_since_last_change': 'Days since last RSI strategy change',
        'rsi_change_percent_from_last_change': 'Percentage change since last RSI strategy change',
        'fell_from_last_max': 'Fall from last maximum',
        'price_per_earning': 'Price per earnings ratio',
        'number_of_employees': 'Number of employees',
        'volume': 'Trading volume'
    }
    
    # Order of columns to display
    filter_column_order = list(column_descriptions.keys())
    
    # Create a reverse mapping for easier processing
    reverse_mapping = {v: k for k, v in column_descriptions.items()}
    
    # Multi-select widget for column selection using descriptions
    selected_descriptions = st.multiselect("Select columns:", list(column_descriptions.values()))
    
    # Map selected descriptions back to original column names
    selected_columns = [reverse_mapping[desc] for desc in selected_descriptions]

    # Display dynamic filters based on selected columns
    filters = {}
    for col in selected_columns:
        if stock_moves[col].dtype in ['float64', 'int64']:
            min_value, max_value = float(stock_moves[col].min()), float(stock_moves[col].max())
            value_range = st.slider(
                f"Select value range - {column_descriptions[col]}",
                min_value=min_value,
                max_value=max_value,
                value=(min_value, max_value),
                step=(max_value - min_value) / 100  # Optional: fine-tuning
            )
            filters[col] = value_range
        else:
            unique_values = stock_moves[col].unique().tolist()
            selected_values = st.multiselect(f"Select values - {column_descriptions[col]}", unique_values)
            filters[col] = selected_values

    # Apply filters to the DataFrame
    filtered_df = stock_moves.copy()
    for col, condition in filters.items():
        if stock_moves[col].dtype in ['float64', 'int64']:
            filtered_df = filtered_df[(filtered_df[col] >= condition[0]) & (filtered_df[col] <= condition[1])]
        elif condition:  # If there are selected values
            filtered_df = filtered_df[filtered_df[col].isin(condition)]

    # merge with the stock name by ticker
    #filtered_df =pd.merge(filtered_df, tw.stock[['name', 'description']], left_on='ticker', right_on='name', how='left')
    
    # rename the column description to stock name
    filtered_df.rename(columns={'description': 'stock_name'}, inplace=True)
    
    # Reorder and select only the desired columns
    display_columns = [
        'stock_name', 'ticker',  'rsi_status', 'ghl_status', 'diff_sma50', 
        'diff_sma100', 'diff_sma200', 'number_of_employees', 'price_per_earning','sector', 'industry', 'volume'
    ]
    filtered_df = filtered_df[display_columns]
    
    

    event = st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
    )
    
    row_id = event.selection.rows
    if row_id:
        selected_stock_ticker = filtered_df.iloc[row_id]['ticker'].iloc[0]      
        with st.container(border=True):
            t = GoldHand(selected_stock_ticker)
            st.plotly_chart(t.plotly_last_year(tw.get_plotly_title(selected_stock_ticker)), use_container_width=False, theme=None)


    
show_stock_watch()
