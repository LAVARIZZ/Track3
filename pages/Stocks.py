import streamlit as st

# Example data
stocks = [
    {"name": "Apple Inc.", "recommended_investment": 10},
    {"name": "Tesla Inc.", "recommended_investment": 15},
    {"name": "Amazon.com Inc.", "recommended_investment": 12},
]

def display_stocks(stocks):
    st.title('Recommended Stocks for Investment')

    # Display the headers for the columns
    st.write(
        f"""
        <div style="display: grid; grid-template-columns: 3fr 2fr 2fr; gap: 20px; font-weight: bold; margin-bottom: 20px; background-color: #f0f0f0; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <div style="font-size: 22px;">Stock Name</div>
            <div style="font-size: 22px;">Number of Stocks You Invest</div>
            <div style="font-size: 22px;">Number of Stocks Recommended</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display the stock information in rows with input fields
    for idx, stock in enumerate(stocks, start=1):
        # Input field for number of stocks user is investing in
        num_investing = st.number_input(f"Number of {stock['name']} stocks you are investing in", min_value=0, step=1, key=f"invest_{idx}")

        st.write(
            f"""
            <div style="display: grid; grid-template-columns: 3fr 2fr 2fr; gap: 20px; margin-bottom: 20px; padding: 15px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                <div style="font-size: 18px; font-weight: bold;">{stock['name']}</div>
                <div style="font-size: 18px; text-align: center;">{num_investing}</div>
                <div style="font-size: 18px; text-align: center;">{stock['recommended_investment']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def main():
    display_stocks(stocks)

if __name__ == "__main__":
    main()
