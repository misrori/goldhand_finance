
import streamlit as st
from goldhand import *
from utils_stock_data import *
tw = get_tw()


biggest_category = ['layer-1', 'smart-contract-platforms', 'memecoins', 'made-in-america', 'cryptocurrencies']
def get_first_category(category_list):
    if not category_list:
        return "cryptocurrencies"
    for category in biggest_category:
        if category in category_list:
            return category
    return "cryptocurrencies"


@st.fragment
def base_crypto_plot_chart():
    with st.expander('### Crypto chart', expanded=False):
        selected_description = st.selectbox("", tw.crypto["display_name"])
        user_ticker = tw.crypto.loc[tw.crypto['display_name']==selected_description, "base_currency"].values[0]

        with st.container(border=True):
            t = GoldHand(user_ticker)
            st.plotly_chart(t.plotly_last_year(tw.get_plotly_title(user_ticker)), use_container_width=False, theme=None)


@st.fragment
def crypto_heat_map():


    crypto_df = tw.crypto[['base_currency', 'display_name', 'market_cap', 'crypto_common_categories', '24h_close_change|5']]
    crypto_df.rename(columns={'base_currency': 'Currency', 'display_name': 'Name', 'market_cap': 'Market Cap', '24h_close_change|5': 'Change', 'crypto_common_categories':'category'}, inplace=True)
    crypto_df['all_category'] = crypto_df['category'].apply(lambda x: ' # '.join(x) if x else 'Nincs' )

    crypto_df['category'] = crypto_df['category'].apply(get_first_category)
    crypto_df['Change'] = crypto_df['Change'].astype(float)
    crypto_df['Change'] = crypto_df['Change'].apply(custom_colorscale, maxcolorchange = 15)

    crypto_df['Market Cap'] = crypto_df['Market Cap'].astype(float)
    crypto_df['market_cap_text'] = crypto_df['Market Cap'].apply(format_large_number)
    crypto_df['Change_text'] = crypto_df['Change'].apply(lambda x: f"{x:.2f}%")  # Két tizedesjegy
    crypto_df['Crypto_Label'] = crypto_df['Name']



    
    with st.spinner("Generating plot..."):
        fig = px.treemap(
            crypto_df,
            path=['category', 'Currency'],  # Hierarchia, ID helyett Display Name használata
            values='Market Cap',  # Méret a piaci kapitalizáció
            color='Change',  # Szín a változás alapján
            color_continuous_scale='RdYlGn',  # Piros-zöld skála
            title='Crypto Market Heatmap',
            labels={
            "market_cap_text": "Market Cap",
            'Change_text' : "Change"
            },
            hover_data={
                'Crypto_Label': True,
                'all_category': True,
                'Change_text': True,
                'market_cap_text': True,
            }
        )
        fig.data[0].update(hovertemplate='Name=%{customdata[0]}<br>Category=%{customdata[1]}<br>Change=%{customdata[2]}<br>Market Cap=%{customdata[3]}')
        fig.update_layout(height=2000, coloraxis_showscale=True)
        st.plotly_chart(fig, use_container_width=True, theme=None)

base_crypto_plot_chart()
crypto_heat_map()