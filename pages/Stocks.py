import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def fetch_historical_data(crypto_id, days=30):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': days
    }
    response = requests.get(url, params=params)
    data = response.json()
    prices = data.get('prices', [])
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def fetch_market_data(crypto_ids):
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'ids': ','.join(crypto_ids)
    }
    response = requests.get(url, params=params)
    data = response.json()
    return pd.DataFrame(data)

st.title("Cryptocurrency Trends")

# Select cryptocurrency
cryptos = ['bitcoin', 'ethereum', 'litecoin', 'ripple', 'cardano', 'polkadot']
crypto = st.selectbox("Select Cryptocurrency", cryptos)

# Fetch historical data
df = fetch_historical_data(crypto)

# Plot price trends
st.subheader(f'{crypto.capitalize()} Price Trends (Last 30 Days)')
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(df.index, df['price'], label=f'{crypto.capitalize()} Price')
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD)')
ax.set_title(f'{crypto.capitalize()} Price Trend Over Time')
ax.legend()
st.pyplot(fig)

# Fetch market data
market_df = fetch_market_data(cryptos)

# Plot pie chart for market cap distribution with legend below
st.subheader('Market Capitalization Distribution')
fig, ax = plt.subplots(figsize=(10, 8))  # Adjust size if needed
sizes = market_df['market_cap']
labels = market_df['name']
colors = plt.get_cmap('tab20').colors  # Use a colormap with distinct colors

# Calculate percentage
percentages = [f'{label}: {size / sum(sizes) * 100:.1f}%' for label, size in zip(labels, sizes)]

# Plot pie chart
wedges, texts, autotexts = ax.pie(sizes, labels=None, colors=colors, autopct='', startangle=140)
ax.set_title('Market Cap Distribution of Cryptocurrencies')

# Add legend below pie chart with percentages
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in colors]
legend_labels = [f'{label}: {percentage}' for label, percentage in zip(labels, percentages)]
ax.legend(handles, legend_labels, title='Cryptocurrencies', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

st.pyplot(fig)

# Plot bar chart for price comparison
st.subheader('Current Price Comparison')
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x='name', y='current_price', data=market_df, ax=ax)
ax.set_xlabel('Cryptocurrency')
ax.set_ylabel('Current Price (USD)')
ax.set_title('Current Prices of Selected Cryptocurrencies')
st.pyplot(fig)

# Plot additional charts
# Line chart for price trends over the last year
st.subheader(f'{crypto.capitalize()} Price Trends (Last 365 Days)')
df_year = fetch_historical_data(crypto, days=365)
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(df_year.index, df_year['price'], label=f'{crypto.capitalize()} Price')
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD)')
ax.set_title(f'{crypto.capitalize()} Price Trend Over the Last Year')
ax.legend()
st.pyplot(fig)
