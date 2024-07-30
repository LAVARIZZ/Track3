import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns, objective_functions
import yfinance as yf

# Load ESG data
esg_data = pd.read_csv('combined_esg.csv')

# Portfolio Optimization Tool Header
st.header('Portfolio Optimization Tool')
st.subheader("This tool is designed to help you determine the optimum distribution of your portfolio based on how much money you have to invest, the risk, and the potential return. It is designed to optimize on the max Sharpe Ratio.")
st.write("Note, the app may encourage you to not select a stock at all depending on the risk of the investment and its expected return.")

with st.expander("What's a Sharpe Ratio?"):
    st.write(""" The Sharpe ratio was developed by Nobel laureate William F. Sharpe and is used to help investors understand the return of an investment compared to its risk. The ratio is the average return earned in excess of the risk-free rate per unit of volatility or total risk. Volatility is a measure of the price fluctuations of an asset or portfolio.

Subtracting the risk-free rate from the mean return allows an investor to better isolate the profits associated with risk-taking activities. The risk-free rate of return is the return on an investment with zero risk, meaning it's the return investors could expect for taking no risk. The yield for a U.S. Treasury bond, for example, could be used as the risk-free rate.

Generally, the greater the value of the Sharpe ratio, the more attractive the risk-adjusted return.""")

# Sidebar for user inputs
st.sidebar.title("Select your portfolio (Minimum of 3 Stocks)")
assets = st.sidebar.multiselect('', list(esg_data.iloc[:, 0]), default=["AAPL", "NVDA", "TGT"])

st.sidebar.title("How much money would you like to invest?")
money = st.sidebar.number_input('Input amount in $', min_value=1, max_value=10000000, value=500)

size = len(assets)
weights = np.array([1 / size for _ in range(size)])

# Get the stock data
stock_start_date = '2019-01-01'
today = datetime.today().strftime('%Y-%m-%d')

df = pd.DataFrame()
for stock in assets:
    df[stock] = yf.download(stock, start=stock_start_date, end=today)['Adj Close']

# Plot Portfolio Price History
fig = plt.figure(figsize=(12.2, 4.5))
for c in df.columns:
    plt.plot(df[c], label=c)
plt.title('Portfolio Price History')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Adj. Price USD ($)', fontsize=18)
plt.legend(df.columns, loc='upper left')
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(""" The chart above shows your portfolio's past returns but does not guarantee future returns.""")

# Calculate returns and portfolio statistics
returns = df.pct_change()
cov_matrix_annual = returns.cov() * 252
port_variance = np.dot(weights.T, np.dot(cov_matrix_annual, weights))
port_volatility = np.sqrt(port_variance)
portfolio_simple_annual_return = np.sum(returns.mean() * weights) * 252

percent_var = str(round(port_variance, 2) * 100) + '%'
percent_vols = str(round(port_volatility, 2) * 100) + '%'
percent_ret = str(round(portfolio_simple_annual_return, 2) * 100) + '%'

# Portfolio Optimization
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

ef = EfficientFrontier(mu, S)
weights = ef.nonconvex_objective(
    objective_functions.sharpe_ratio,
    objective_args=(ef.expected_returns, ef.cov_matrix),
    weights_sum_to_one=True,
)
cleaned_weights = ef.clean_weights()
ef.portfolio_performance(verbose=True)

# ESG Score Calculation
esg_data.set_index(esg_data.iloc[:, 0], inplace=True)
e_score = esg_data.loc[assets, ['environment_score', 'governance_score', 'social_score']]
esg_sum = e_score.sum(axis=1)

# Display results
col1, col2 = st.columns(2)

# Display Portfolio Statistics
with col1:
    st.subheader("Your Portfolio's Expected Returns")
    st.subheader("Expected annual return:")
    st.write(percent_ret)
    st.subheader('Annual volatility/standard deviation/risk:')
    st.write(percent_vols)
    st.subheader('Annual variance:')
    st.write(percent_var)

# Display Optimal Weights and ESG Scores
with col2:
    st.subheader("Your Portfolio's Optimal Weights")
    st.write(pd.Series(cleaned_weights, name='Optimal Weights'))

    # Display ESG Score Sum
    st.subheader("ESG Score Sum")
    esg_sum_display = pd.Series(esg_sum, name='ESG Score Sum')
    st.write(esg_sum_display)

    with st.expander("See explanation"):
        st.write(""" Note the weights may have some rounding error, meaning they may not add up exactly to 1 but should be close.""")

# Discrete Allocation
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

latest_prices = get_latest_prices(df)
da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value=money)
allocation, leftover = da.lp_portfolio()

st.subheader("How much of each stock to buy:")
st.write(pd.Series(allocation, name='Optimal Buy'))

st.subheader("Funds Remaining:")
st.write("$" + str(round(leftover)) + " dollars left over")
