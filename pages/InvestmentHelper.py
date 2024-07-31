from io import BytesIO
import requests
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns
import yfinance as yf
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from PIL import Image
import os
from dotenv import load_dotenv
load_dotenv()

# Load ESG data
esg_data = pd.read_csv("combined_esg.csv")

# Portfolio Optimization Tool Header
st.header("Smart Investment Navigator")
st.write(
    "Welcome! We’re here to guide you in making informed investment choices based on your selected stocks and their financial potential."
)

# Sidebar for user inputs
st.sidebar.title("Build Your Investment Portfolio (Select at Least 3 Stocks)")
assets = st.sidebar.multiselect(
    "", list(esg_data.iloc[:, 0]), default=st.session_state['portfolio'] if st.session_state['portfolio'] else ["AAPL", "NVDA", "TGT"] 
)

st.sidebar.title("Investment Amount")
money = st.sidebar.number_input(
    "Enter the amount in $", min_value=1, max_value=10000000, value=500
)

size = len(assets)
weights = np.array([1 / size for _ in range(size)])

# Get the stock data
stock_start_date = "2019-01-01"
today = datetime.today().strftime("%Y-%m-%d")

df = pd.DataFrame()
for stock in assets:
    df[stock] = yf.download(stock, start=stock_start_date, end=today)["Adj Close"]

# Calculate returns and portfolio statistics
returns = df.pct_change()
cov_matrix_annual = returns.cov() * 252
port_variance = np.dot(weights.T, np.dot(cov_matrix_annual, weights))
port_volatility = np.sqrt(port_variance)
portfolio_simple_annual_return = np.sum(returns.mean() * weights) * 252

percent_var = str(round(port_variance, 2) * 100) + "%"
percent_vols = str(round(port_volatility, 2) * 100) + "%"
percent_ret = str(round(portfolio_simple_annual_return, 2) * 100) + "%"

# Portfolio Optimization
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
ef.portfolio_performance(verbose=True)

# ESG Score Calculation
esg_data.set_index(esg_data.iloc[:, 0], inplace=True)
e_score = esg_data.loc[
    assets, ["environment_score", "governance_score", "social_score"]
]
esg_sum = e_score.sum(axis=1)

# Discrete Allocation
latest_prices = get_latest_prices(df)
da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value=money)
allocation, leftover = da.lp_portfolio()

# Display name of selected stocks
with st.container():
    st.markdown(
        """
        <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h3>Your Selected Stocks</h3>
            <p>{}</p>
        </div>
    """.format(
            ", ".join(assets)
        ),
        unsafe_allow_html=True,
    )

# Display Portfolio Statistics
with st.container():
    st.markdown(
        """
        <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h4>Projected Returns of Your Portfolio</h4>
            <p>Estimated annual return: {}</p>
            <p>Annual volatility (risk): {}</p>
            <p>Annual variance: {}</p>
        </div>
    """.format(
            percent_ret, percent_vols, percent_var
        ),
        unsafe_allow_html=True,
    )

# Display Tables
with st.container():
    st.markdown(
        """
        <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <div style='display: flex; justify-content: space-between;'>
                <div style='width: 50%; padding-right: 10px;'>
                    <h4>Optimal Asset Allocation</h4>
                    <div style='overflow-x: auto;'>
                        {}
                    </div>
                </div>
                <div style='width: 50%; padding-left: 10px;'>
                    <h4>ESG Scores Summary</h4>
                    <div style='overflow-x: auto;'>
                        {}
                    </div>
                </div>
            </div>
        </div>
    """.format(
            pd.DataFrame(
                list(cleaned_weights.items()), columns=["Stock", "Weight"]
            ).to_html(index=False, classes="table table-bordered", border=0),
            pd.DataFrame(esg_sum)
            .reset_index()
            .rename(columns={0: "Stock", 1: "ESG Score Sum"})
            .to_html(index=False, classes="table table-bordered", border=0),
        ),
        unsafe_allow_html=True,
    )

# Plot Portfolio Price History
with st.container():
    st.markdown(
        """
        <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h3>Historical Price Trends</h3>
    """,
        unsafe_allow_html=True,
    )

    fig = plt.figure(figsize=(12.2, 4.5))
    for c in df.columns:
        plt.plot(df[c], label=c)
    plt.title("Historical Price Trends")
    plt.xlabel("Date", fontsize=18)
    plt.ylabel("Adjusted Price (USD)", fontsize=18)
    plt.legend(df.columns, loc="upper left")
    st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)

# Discrete Allocation results
with st.container():
    st.markdown(
        """
        <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h3>Recommended Stock Purchases:</h3>
            <div style='overflow-x: auto;'>
                {}
            </div>
        </div>
    """.format(
            pd.DataFrame(
                list(allocation.items()), columns=["Stock", "Quantity"]
            ).to_html(index=False, classes="table table-bordered", border=0)
        ),
        unsafe_allow_html=True,
    )

with st.container():
    st.markdown(
        """
        <div style='background-color: #ffffff; padding: 20px; border-radius: 10px;'>
            <h3>Remaining Funds:</h3>
            <p>$ {}</p>
        </div>
    """.format(
            round(leftover)
        ),
        unsafe_allow_html=True,
    )

with st.container():
    st.title("Post on FinConnect")

    # Function to make the API request
    def generate_image():
        apikey = os.getenv("OPENAI_API_KEY")
        print('api',apikey)
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')} ",
        }
        data = {
            "model": "dall-e-3",
            "prompt": f"Create a image with white background, On left half of image write all these in bullet points (colored) {st.session_state['portfolio']}. DO NOT include any other text, image,graphic or visualization in the image.",
            "n": 1,
            "size": "1024x1024",
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()

    # Generate image on button click
    if st.button("Generate Image"):
        response = generate_image()
        print(response)
        if "data" in response:
            image_url = response["data"][0]["url"]
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            st.image(image, caption="Generated Image", use_column_width=True)
        else:
            st.error("Failed to generate image. Please check the API response.")

    # Run the app
    if __name__ == "__main__":
        st.write("Click the button above to generate an image.")
