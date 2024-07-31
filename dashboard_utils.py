import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import json
import datetime
import altair as alt

# Function to fetch stock data
def fetch_stock_data(stock_symbol, period):
    stock = yf.Ticker(stock_symbol)
    hist = stock.history(period=period)
    return hist['Close']

# Fetch stock data and combine into a DataFrame
def get_trends(stocks, time_period):
    stock_data = {stock: fetch_stock_data(stock, time_period) for stock in stocks}
    df = pd.DataFrame(stock_data)
    return df

def plot_trends(stocks, time_period='1mo'):
    fig = go.Figure()
    data = get_trends(stocks, time_period)
    for stock in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data[stock], mode='lines', name=stock))
    fig.update_layout(
        title='Stock Price Trends',
        xaxis_title='Date',
        yaxis_title='Closing Price',
        template='plotly_dark',
        legend_title_text='Stocks'
    )
    return fig

def calculate_gains_losses(stocks, time_period):
    data = get_trends(stocks, time_period)
    gains_losses = {}
    for stock in stocks:
        gains_losses[stock] = (data[stock].iloc[-1] - data[stock].iloc[0]) / data[stock].iloc[0] * 100
    return gains_losses

def create_donut_chart(stocks, time_period):
    gains_losses = calculate_gains_losses(stocks, time_period)
    total_gain_loss = sum(gains_losses.values())
    
    # Prepare data for the donut chart
    source = pd.DataFrame({
        "Topic": ["Total Gain/Loss", ""],
        "% value": [total_gain_loss, 100 - total_gain_loss]
    })
    source_bg = pd.DataFrame({
        "Topic": ["Total Gain/Loss", ""],
        "% value": [100, 0]
    })
    
    # Determine chart color based on gain/loss
    if total_gain_loss >= 0:
        chart_color = ['#27AE60', '#12783D']  # Green for gain
    else:
        chart_color = ['#E74C3C', '#781F16']  # Red for loss
    
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color=alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=["Total Gain/Loss", ""],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
    
    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=20, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{total_gain_loss:.2f} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color=alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=["Total Gain/Loss", ""],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
    
    return plot_bg + plot + text

