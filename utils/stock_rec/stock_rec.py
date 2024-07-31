import yfinance as yf
import numpy as np
import pandas as pd

class StockRecommendation:
    def __init__(self):
        self.tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'JNJ', 'V', 'PG']
        self.stock_data = {}

    def fetch_stock_data(self):
        for ticker in self.tickers:
            self.stock_data[ticker] = yf.Ticker(ticker).history(period="5y")
        return self.stock_data

    def calculate_metrics(self, stock_data):
        metrics = []
        for ticker, data in stock_data.items():
            if data.empty:
                continue

            returns = data['Close'].pct_change().mean() * 252  # Annualized return
            risk = data['Close'].pct_change().std() * np.sqrt(252)  # Annualized risk

            info = yf.Ticker(ticker).info
            market_cap = info.get('marketCap', 0)
            dividend_yield = info.get('dividendYield', 0)
            pe_ratio = info.get('trailingPE', 0)
            trailing_eps = info.get('trailingEps', 0)
            forward_eps = info.get('forwardEps', 0)
            eps_growth = (forward_eps - trailing_eps) / trailing_eps if trailing_eps else 0

            metrics.append({
                'Ticker': ticker,
                'Returns': returns * 100,
                'Risk': risk * 100,
                'Market Cap': market_cap,
                'Dividend Yield': dividend_yield,
                'P/E Ratio': pe_ratio,
                'EPS Growth': eps_growth
            })
        return pd.DataFrame(metrics)

    def score_and_rank_stocks(self, metrics_df, risk_tolerance):
        # Normalize metrics
        metrics_df['Returns Score'] = metrics_df['Returns'].rank(ascending=False)
        metrics_df['Risk Score'] = metrics_df['Risk'].rank(ascending=True)
        metrics_df['Market Cap Score'] = metrics_df['Market Cap'].rank(ascending=False)
        metrics_df['Dividend Yield Score'] = metrics_df['Dividend Yield'].rank(ascending=False)
        metrics_df['P/E Ratio Score'] = metrics_df['P/E Ratio'].rank(ascending=True)
        metrics_df['EPS Growth Score'] = metrics_df['EPS Growth'].rank(ascending=False)

        # Composite score weights based on risk tolerance
        if risk_tolerance == 'low':
            risk_weight = 0.3
            return_weight = 0.2
        elif risk_tolerance == 'medium':
            risk_weight = 0.2
            return_weight = 0.3
        elif risk_tolerance == 'high':
            risk_weight = 0.1
            return_weight = 0.4
        else:
            risk_weight = 0.2
            return_weight = 0.3  # Default to medium risk

        metrics_df['Composite Score'] = (
                metrics_df['Returns Score'] * return_weight +
                metrics_df['Risk Score'] * risk_weight +
                metrics_df['Market Cap Score'] * 0.2 +
                metrics_df['Dividend Yield Score'] * 0.1 +
                metrics_df['P/E Ratio Score'] * 0.1 +
                metrics_df['EPS Growth Score'] * 0.1
        )

        metrics_df = metrics_df.sort_values(by='Composite Score', ascending=False)
        return metrics_df

    def recommend_stocks_to_buy(self, risk_tolerance,top_n = 10):
        stock_data = self.fetch_stock_data()
        metrics_df = self.calculate_metrics(stock_data)
        ranked_stocks = self.score_and_rank_stocks(metrics_df, risk_tolerance)
        return ranked_stocks.head(top_n)[['Ticker', 'Composite Score', 'Returns', 'Risk', 'Market Cap']]

# Example usage
# risk_tolerance = 'medium'
# stock_rec = StockRecommendation()
# recommendations = stock_rec.recommend_stocks_to_buy(risk_tolerance)
# print(recommendations)
