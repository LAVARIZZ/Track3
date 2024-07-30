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

        st.write("### Recommended Stocks")
        for idx, row in recommendations.iterrows():
            col1, col2 = st.columns([4, 1])
            col1.write(
                f"**{row['Ticker']}**: Composite Score: {row['Composite Score']:.2f}, Returns: {row['Returns']:.2f}%, Risk: {row['Risk']:.2f}%")
            if col2.button("Add to Portfolio", key=f"add_{row['Ticker']}"):
                if row['Ticker'] not in st.session_state['portfolio']:
                    st.session_state['portfolio'].append(row['Ticker'])
                    st.success(f"Added {row['Ticker']} to portfolio")

    # Display the portfolio
    st.write("### Your Portfolio")
    if st.session_state['portfolio']:
        for ticker in st.session_state['portfolio']:
            st.write(f"- {ticker}")
    else:
        st.write("Your portfolio is empty.")


if __name__ == "__main__":
    main()
