import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
from dashboard_utils import *
import altair as alt

# Load user data from JSON file
with open('user_stocks.json') as f:
    data = json.load(f)

# Fetch stocks for user1
user = next((user for user in data['users'] if user['username'] == 'user1'), None)
if user is None:
    st.error("User not found")
    st.stop()

stocks = list(user['stocks'].keys())

esg_data = pd.read_csv('combined_esg.csv')
esg_data.set_index(esg_data['ticker'], inplace=True)

# Get ESG scores for the portfolio
portfolio_esg = esg_data.loc[stocks, ['environment_score', 'governance_score', 'social_score']]
avg_esg_score = int(portfolio_esg.mean(axis=0).values[0])

# Function to create ESG donut charts
def create_esg_donut_chart(score, label, color):
    source = pd.DataFrame({
        "Topic": ['', label],
        "% value": [100 - score, score]
    })
    
    chart_color = ['#27AE60', '#12783D'] if color == 'green' else ['#E74C3C', '#781F16']
    
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color=alt.Color("Topic:N", scale=alt.Scale(domain=[label, ''], range=chart_color), legend=None)
    ).properties(width=130, height=130)
    
    text = plot.mark_text(align='center', color=chart_color[1], font="Lato", fontSize=18, fontWeight=700).encode(text=alt.value(f'{score:.2f} %'))
    plot_bg = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color=alt.Color("Topic:N", scale=alt.Scale(domain=[label, ''], range=chart_color), legend=None)
    ).properties(width=130, height=130)
    return plot_bg + plot + text


# Streamlit app layout
st.set_page_config(
    page_title="Stock Portfolio Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.title('📈 Stock Portfolio Dashboard')
    
    time_period_list = ['1d', '5d', '1mo', '3mo', '1y']
    selected_time_period = st.selectbox('Select a time period', time_period_list)

    color_theme_list = ['Blues', 'Cividis', 'Greens', 'Inferno', 'Magma', 'Plasma', 'Reds', 'Rainbow', 'Turbo', 'Viridis']

r1_cols = st.columns((2, 2, 2, 2), gap='medium')  
with r1_cols[0]:
    st.markdown('#### Portfolio ESG Score')
    st.markdown(f"""
        <div style="text-align: center; font-size: 60px; font-weight: bold; padding: 20px; background-color: #f0f0f0; border-radius: 10px;">
            {avg_esg_score}
        </div>
        """, unsafe_allow_html=True)    
        
with r1_cols[1]:
    st.markdown('#### Environment Score')
    e_score = int(portfolio_esg['environment_score'].values[0])
    e_donut = create_esg_donut_chart(e_score, 'Environment', 'green')
    st.altair_chart(e_donut, use_container_width=True)
    
    
with r1_cols[2]:
    st.markdown('#### Social Score')
    s_score = int(portfolio_esg['social_score'].values[0])
    s_donut = create_esg_donut_chart(s_score, 'Social', 'orange')    
    st.altair_chart(s_donut, use_container_width=True)
    
    
with r1_cols[3]:
    st.markdown('#### Governance Score')    
    g_score = int(portfolio_esg['governance_score'].values[0])
    g_donut = create_esg_donut_chart(g_score, 'Governance', 'blue')
    st.altair_chart(g_donut, use_container_width=True)
    
    
    

col1, col2 = st.columns((2.5, 6), gap='medium')  

with col1:
    st.markdown('#### Gains/Losses')
    donut_chart = create_donut_chart(stocks, selected_time_period)
    st.altair_chart(donut_chart, use_container_width=True)
    st.markdown('#### Top Stocks')

    gains_losses = calculate_gains_losses(stocks, selected_time_period)
    top_stocks_df = pd.DataFrame.from_dict(gains_losses, orient='index', columns=['Profit'])
    top_stocks_df = top_stocks_df.sort_values(by='Profit', ascending=False)
    top_stocks_df[' % '] = top_stocks_df['Profit'].apply(lambda x: f'🡅 {round(x)}%' if x >= 0 else f'🡇 {round(x)}%')


    st.dataframe(top_stocks_df,
                width=None,
                column_config={
                    "Profit": st.column_config.ProgressColumn(
                        "Profit",
                        format="%d",  
                        min_value=-100,
                        max_value=100
                    )}
                )

with col2:
    st.markdown('#### Stock Trends')
    fig = plot_trends(stocks, selected_time_period)
    st.plotly_chart(fig, use_container_width=True)
    
    
st.markdown('#### Stock Portfolio Details')

# Calculate returns based on the selected time period

def fetch_portfolio_details(stocks, time_period='1d'):
    data = []
    
    for stock in stocks:
        ticker = yf.Ticker(stock)
        hist = ticker.history(period=time_period)
        
        if hist.empty:
            continue
        
        # Get the last available record
        initial_record = hist.iloc[0]  # Opening record
        latest_record = hist.iloc[-1]  # Latest record
        
        initial_close = initial_record['Close']
        final_close = latest_record['Close']
        high = latest_record['High']
        low = latest_record['Low']
        open_price = latest_record['Open']
        close_price = latest_record['Close']
        
        if(time_period=='1d'):
        # Calculate percentage change from open to close
            percentage_change = ((close_price - open_price) / open_price) * 100
        else:
            percentage_change = ((final_close - initial_close) / initial_close) * 100

        
        data.append({
            'Stock': stock,
            'High': high,
            'Low': low,
            'Open': open_price,
            'Close': close_price,
            'Returns': f'{round(percentage_change, 2)}%'
        })
    
    df = pd.DataFrame(data)
    return df


portfolio_details = fetch_portfolio_details(stocks, selected_time_period)
# Function to apply color and arrow based on returns
def color_return(value):
    if value.startswith('-'):
        return 'color: red; font-weight: bold;', '🡇'
    else:
        return 'color: green; font-weight: bold;', '🡅'

# Apply color formatting and arrow
portfolio_details['Returns'] = portfolio_details['Returns'].apply(
    lambda x: f'<span style="{color_return(x)[0]}">{color_return(x)[1]} {x}</span>'
)

html = portfolio_details.to_html(escape=False, index=False, classes='styled-table')

# Add custom CSS
css = """
<style>
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #ddd;
        font-size: 16px;
    }
    .styled-table th, .styled-table td {
        padding: 12px 15px;
        text-align: center;
    }
    .styled-table thead tr {
        background-color: #f4f4f4;
        border-bottom: 1px solid #ddd;
    }
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f9f9f9;
    }
    .styled-table tbody tr:nth-of-type(odd) {
        background-color: #fff;
    }
    .styled-table tbody tr:hover {
        background-color: #f1f1f1;
    }
</style>
"""

# Display the styled HTML table
st.markdown(css, unsafe_allow_html=True)
st.markdown(html, unsafe_allow_html=True)