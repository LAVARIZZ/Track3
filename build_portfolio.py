import streamlit as st
import numpy as np
from stock_rec import *


# Function to get risk tolerance from slider value
def get_risk_tolerance(value):
    if value < 33:
        return 'low'
    elif value < 66:
        return 'medium'
    else:
        return 'high'


# Streamlit app
def main():
    st.title("Start building your portfolio")
    slider_value = st.slider(
        "Select your risk tolerance",
        min_value=0,
        max_value=100,
        value=50,
        step=1
    )
    risk_tolerance = get_risk_tolerance(slider_value)
    st.markdown(f'''
    <style>
        .stSlider > div {{
            background: linear-gradient(to right, green, yellow, red);
            border-radius: 10px;
            padding: 0px 10px;
        }}
        .stSlider > div > div > div > div {{
            color: transparent;
        }}
        .stSlider > div > div > div > div > div {{
            color: white;
        }}
    </style>
    ''', unsafe_allow_html=True)

    # Portfolio list to keep track of added stocks
    if 'portfolio' not in st.session_state:
        st.session_state['portfolio'] = []

    if st.button("Get Recommendations"):
        st.write(f"Fetching recommendations for {risk_tolerance} risk tolerance...")
        recommendations = recommend_stocks_to_buy(tickers, risk_tolerance)

        # Create table headers
        cols = st.columns(6)
        headers = ["Stock", "Composite Score", "Returns", "Risk", "Market Cap", ""]
        for col, header in zip(cols, headers):
            col.write(f"**{header}**")

        # Create table rows with stock data and add to portfolio buttons
        for idx, row in recommendations.iterrows():
            cols = st.columns(6)
            cols[0].write(f"**{row['Ticker']}**")
            cols[1].write(f"{row['Composite Score']:.2f}")
            cols[2].write(f"{row['Returns']:.2f}%")
            cols[3].write(f"{row['Risk']:.2f}%")
            cols[4].write(f"{row['Market Cap']:,}")
            if cols[5].button("Add to Portfolio", key=f"add_{row['Ticker']}",
                              help=f"Add {row['Ticker']} to your portfolio"):
                if row['Ticker'] not in st.session_state['portfolio']:
                    st.session_state['portfolio'].append(row['Ticker'])
                    st.success(f"Added {row['Ticker']} to portfolio")

        # Display the portfolio
    st.write("### Your Portfolio")
    if st.session_state['portfolio']:
        portfolio_df = pd.DataFrame(st.session_state['portfolio'], columns=['Ticker'])
        st.write(portfolio_df)
    else:
        st.write("Your portfolio is empty.")


if __name__ == "__main__":
    main()
