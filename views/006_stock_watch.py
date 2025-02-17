import streamlit as st
import pandas as pd
from goldhand import *
from utils_data import get_tw

tw=get_tw()

@st.cache_data()
def get_money_data():
    df = pd.read_csv('https://raw.githubusercontent.com/misrori/money_flow/refs/heads/main/last_stocks_update.csv')
    df =pd.merge(df, tw.stock[['name', 'description']], left_on='ticker', right_on='name', how='left')
    df['display_name'] = df['description'] + ' (' + df['name'] + ')'
    return df

stock_moves = get_money_data()

if 'selected_strategy_index' not in st.session_state:
    st.session_state.selected_strategy_index = 0

if 'selected_filtered_index' not in st.session_state:
    st.session_state.selected_filtered_index = 0



def update_index(temp_df):
    try:
        st.session_state.selected_filtered_index = int(temp_df[temp_df['display_name'] == st.session_state.selected_filtered_id].index[0])
    except:
        pass

def zero_index():
    try:
        st.session_state.selected_filtered_index = 0
    except:
        pass

@st.fragment
def show_stock_filter():

    # Create tabs and handle tab switching
    tab1, tab2, = st.tabs([ "🔑 Filter", "📊 Analyze"])

    # Detect tab switch
    with tab1:  
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
                    step=(max_value - min_value) / 100,  # Optional: fine-tuning
                    on_change=zero_index
                )
                filters[col] = value_range
            else:
                unique_values = stock_moves[col].unique().tolist()
                selected_values = st.multiselect(f"Select values - {column_descriptions[col]}", unique_values, on_change=zero_index)
                filters[col] = selected_values

        # Apply filters to the DataFrame
        filtered_df = stock_moves.copy()
        for col, condition in filters.items():
            if stock_moves[col].dtype in ['float64', 'int64']:
                filtered_df = filtered_df[(filtered_df[col] >= condition[0]) & (filtered_df[col] <= condition[1])]
            elif condition:  # If there are selected values
                filtered_df = filtered_df[filtered_df[col].isin(condition)]
                
        # check if the filtered data is empty
        

        # merge with the stock name by ticker
        #filtered_df =pd.merge(filtered_df, tw.stock[['name', 'description']], left_on='ticker', right_on='name', how='left')
        
        # rename the column description to stock name
        # filtered_df.rename(columns={'description': 'stock_name'}, inplace=True)
        

        if len(filtered_df) > 0:
            display_columns = [
                'display_name', 'ticker',  'rsi_status', 'ghl_status', 'diff_sma50', 
                'diff_sma100', 'diff_sma200', 'number_of_employees', 'price_per_earning','sector', 'industry', 'volume'
            ]
            filtered_df = filtered_df[display_columns]
            # Display the filtered DataFrame
            event = st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True,
                #on_select="rerun",
                #selection_mode="multi-row",
            )
            st.session_state.filtered_df = filtered_df
        else:
            st.session_state.filtered_df = pd.DataFrame()
            
    with tab2:
        
        if len(st.session_state.filtered_df) > 0:
            
            temp_df = st.session_state.filtered_df.copy()
            temp_df.reset_index(drop=True, inplace=True)
            
            selected_description = st.selectbox(
                "Select a company:", 
                temp_df["display_name"], 
                key="selected_filtered_id",
                index=st.session_state.selected_filtered_index, 
                on_change= lambda: update_index(temp_df)

            )
            
            company_name = temp_df.loc[temp_df["display_name"] == selected_description, "ticker"].values[0]
            col1, col2, col3 = st.columns([1.4, 1, 4],vertical_alignment='center')

            with col1:
                #st.markdown("##### Select a Company")
                label_of_next_button = f'Next: {temp_df["display_name"][(st.session_state.selected_filtered_index + 1) % len(temp_df)]}'

                if st.button(label_of_next_button):
                    st.session_state.selected_filtered_index = (st.session_state.selected_filtered_index + 1) % len(temp_df)
                    st.rerun(scope="fragment")

                
            with col2:
                with st.container(border=True):
                    # Input for selecting the number of days
                    ndays = st.number_input("Number of days:", min_value=1, max_value=5000, value=800, step=10)

            # Layout: Strategies displayed in a single row
            with col3:
                with st.container(border=True):
                    # Radio buttons for selecting a trading strategy
                    strategy_selected = st.radio(
                        "Select a strategy:",
                        [
                            "Base Plot",
                            "Goldhand Line Plot",
                            "RSI Strategy",
                            "Goldhand Line Strategy",
                        ],
                        index=st.session_state.selected_strategy_index,
                        horizontal=True,  # Displayed in a horizontal row
                    )
                # RSI Strategy parameters
            if strategy_selected == "RSI Strategy":
                st.session_state.selected_strategy_index =2
                st.divider()
                st.markdown("### RSI Parameters")
                col4, col5 = st.columns(2)
                with col4:
                    buy_threshold = st.slider("Buy Threshold:", min_value=10, max_value=50, value=30, step=1)
                with col5:
                    sell_threshold = st.slider("Sell Threshold:", min_value=60, max_value=100, value=70, step=1)
            else:
                # Default values for thresholds if not using RSI strategy
                buy_threshold = 30
                sell_threshold = 70

            # Display strategy results
            if company_name:
                if strategy_selected == "Base Plot":
                    st.session_state.selected_strategy_index = 0
                    # Display a basic plot for the selected company
                    t = GoldHand(company_name)
                    fig = t.plotly_last_year(plot_title=tw.get_plotly_title(company_name), ndays=ndays)

                elif strategy_selected == "Goldhand Line Plot":
                    st.session_state.selected_strategy_index = 1
                    # Display a Goldhand line plot for the selected company
                    t = GoldHand(company_name)
                    fig = t.plot_goldhand_line(plot_title=tw.get_plotly_title(company_name), ndays=ndays)

                elif strategy_selected == "RSI Strategy":
                    st.session_state.selected_strategy_index = 2
                    # Display results for RSI strategy
                    fig = show_indicator_rsi_strategy(
                        ticker=company_name,
                        buy_threshold=buy_threshold,
                        sell_threshold=sell_threshold,
                        plot_title=tw.get_plotly_title(company_name),
                        plot_height=1000,
                        ndays=ndays
                    )

                elif strategy_selected == "Goldhand Line Strategy":
                    # Display results for Goldhand Line strategy
                    fig = show_indicator_goldhand_line_strategy(
                        ticker=company_name,
                        plot_title=tw.get_plotly_title(company_name),
                        plot_height=1000,
                        ndays=ndays
                    )

                else:
                    st.error("Unknown strategy selected!")
                    
                
                # Display the results
                with st.container(border=True):
                    st.plotly_chart(fig, use_container_width=True, theme=None)

show_stock_filter()