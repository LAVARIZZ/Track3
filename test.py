import yfinance as yf
from datetime import datetime, timedelta

def get_stock_metrics(stock):
    """
    Fetch stock metrics including yesterday's and today's data.
    
    Parameters:
    - stock (str): Stock ticker symbol.
    
    Returns:
    - dict: A dictionary containing yesterday's high, low, open, close, adjusted close, 
            today's open, and the increase/decrease since yesterday.
    """
    # Define the time range
    end_time = datetime.now().strftime('%Y-%m-%d')
    start_time_yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_time_today = end_time
    
    # Download historical data
    data_yesterday = yf.download(stock, start=start_time_yesterday, end=end_time, interval='1d')
    data_today = yf.download(stock, start=start_time_today, end=end_time, interval='1m')
    
    if data_yesterday.empty or data_today.empty:
        return {"Error": "No data available for the requested dates"}
    
    # Get yesterday's data
    yesterday_data = data_yesterday.iloc[-1]
    
    # Get today's data (most recent minute)
    today_data = data_today.iloc[-1]
    
    # Calculate metrics
    stock_metrics = {
        'Yesterday Open': yesterday_data['Open'],
        'Yesterday High': yesterday_data['High'],
        'Yesterday Low': yesterday_data['Low'],
        'Yesterday Close': yesterday_data['Close'],
        'Yesterday Adj Close': yesterday_data['Adj Close'],
        'Today Open': today_data['Open'],
        'Increase/Decrease Since Yesterday': today_data['Open'] - yesterday_data['Close']
    }
    
    return stock_metrics

# Example usage
stock_symbol = 'AAPL'  # Replace with your stock ticker
metrics = get_stock_metrics(stock_symbol)
print(metrics)