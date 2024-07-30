import requests

def fetch_technical_indicators(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

api_key = 'YOUR_API_KEY'
symbol = 'AAPL'
technical_indicators = fetch_technical_indicators(symbol, api_key)

print(technical_indicators)