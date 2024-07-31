import streamlit as st
import pandas as pd
from utils.stock_rec.stock_rec import StockRecommendation
from streamlit_extras.switch_page_button import switch_page
from dotenv import load_dotenv
load_dotenv()
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

    # Initialize session state for portfolio and checkboxes
    if 'portfolio' not in st.session_state:
        st.session_state['portfolio'] = []

    if 'checkboxes' not in st.session_state:
        st.session_state['checkboxes'] = {}

    if 'recommendations' not in st.session_state:
        st.session_state['recommendations'] = pd.DataFrame()

    # Get the number of recommendations to display from the user
    top_n = st.number_input("Enter the number of recommendations to display", min_value=1, value=10, step=1)
    
    # Store the value in st.session_state
    st.session_state['top_n'] = top_n

    if st.button("Get Recommendations"):
        st.write(f"Fetching recommendations for {risk_tolerance} risk tolerance...")
        sr = StockRecommendation()
        recommendations = sr.recommend_stocks_to_buy(risk_tolerance,st.session_state['top_n'])
        st.session_state['recommendations'] = recommendations
    if not st.session_state['recommendations'].empty:
        recommendations = st.session_state['recommendations']
        
        # Create table headers
        cols = st.columns(6)
        headers = ["Stock", "Composite Score", "Returns", "Risk", "Market Cap", ""]
        for col, header in zip(cols, headers):
            col.write(f"**{header}**")

        # Create table rows with stock data and add to portfolio checkboxes
        for idx, row in recommendations.iterrows():
            cols = st.columns(6)
            cols[0].write(f"**{row['Ticker']}**")
            cols[1].write(f"{row['Composite Score']:.2f}")
            cols[2].write(f"{row['Returns']:.2f}%")
            cols[3].write(f"{row['Risk']:.2f}%")
            cols[4].write(f"{row['Market Cap']:,}")
            checkbox_key = f"add_{row['Ticker']}"
            if checkbox_key not in st.session_state['checkboxes']:
                st.session_state['checkboxes'][checkbox_key] = False
            add_to_portfolio = cols[5].checkbox(
                "Add to Portfolio", 
                key=checkbox_key, 
                value=st.session_state['checkboxes'][checkbox_key]
            )
            st.session_state['checkboxes'][checkbox_key] = add_to_portfolio

        # Update the portfolio based on checkboxes
        for key, value in st.session_state['checkboxes'].items():
            ticker = key.replace("add_", "")
            if value and ticker not in st.session_state['portfolio']:
                st.session_state['portfolio'].append(ticker)
            elif not value and ticker in st.session_state['portfolio']:
                st.session_state['portfolio'].remove(ticker)

    print(st.session_state['portfolio'])
    # Display the portfolio
    st.write("### Your Portfolio")
    if st.session_state['portfolio']:
        portfolio_df = pd.DataFrame(st.session_state['portfolio'], columns=['Ticker'])
        st.write(portfolio_df)
    else:
        st.write("Your portfolio is empty.")
        # Add a button to redirect to the portfolio page
    want_to_contribute = st.button("Optimise My Portfolio")
    if want_to_contribute:
        switch_page("my_portfolios")


if __name__ == "__main__":
    main()
