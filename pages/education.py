import streamlit as st

# Title of the Financial Literacy Page
st.title('Explore the Education Platform')

# Section 1: Introduction to Financial Education
st.subheader("""
   The education platform provides learning modules on portfolio construction and ETFs to help investors learn the basics and potentially make better investment decisions.
""")

# Section 2: Display Videos with Titles
with st.container():
    st.subheader('Course Videos')
    
    videos = [
        ("What is ETF?", "https://www.youtube.com/embed/OwpFBi-jZVg?si=nwFyRb1EW88wWxH4"),
        ("Fixed Income", "https://www.youtube.com/embed/uE3xUEaG5X8?si=z_OzhokXCYyQqGPK"),
        ("Alternative Investing", "https://www.youtube.com/embed/F4O6S2yGijU?si=nCr7Wmo7VKpET1RK"),
        ("International Investing", "https://www.youtube.com/embed/3w6QSA_qYY8?si=BGQrpsJLAyB7dNCI"),
        ("Financial Planning", "https://www.youtube.com/embed/6-tqUtwqxlI?si=7-Z4230KyTDMjNrR"),
        ("Budget Basics", "https://www.youtube.com/embed/sVKQn2I4HDM?si=QC-bcMp9I7Ld5ral")
    ]

    # Create columns based on the number of videos
    cols = st.columns(3)  # Adjust the number of columns as needed

    for i, (title, video) in enumerate(videos):
        col_index = i % len(cols)
        with cols[col_index]:
            st.markdown(f"**{title}**")
            st.video(video, format='video/mp4')

# Section 3: Start Course Button
with st.container():
    st.subheader('Start Your Portfolio Building Course')
    st.write("""
    Congratulations on starting your financial literacy journey! Let's dive into the topics that will empower you to make informed financial decisions.
    """)

    # Start Course Button
    if st.button('Start Course'):
        st.write("You are now ready to start building your financial portfolio. Explore each topic in detail to enhance your understanding and make better financial decisions.")
        # Here you can add functionality to navigate to another page or section
        # For example, you can display course content or redirect to another page

# Additional Resources
with st.container():
    st.subheader('Additional Resources')
    st.write("""
    - [Investopedia](https://www.investopedia.com/)
    - [NerdWallet](https://www.nerdwallet.com/)
    - [The Balance](https://www.thebalance.com/)
    - [Blackrock Academies](https://www.blackrock.com/americas-offshore/en/education)
    """)

# FAQ Section with Expanders
with st.container():
    st.subheader('Frequently Asked Questions (FAQ)')

    # FAQ 1
    with st.expander("What is the Coffee Can Portfolio Strategy?"):
        st.write("""
        The Coffee Can Portfolio Strategy is an investment approach where you buy a set of high-quality stocks and then "forget" about them, allowing them to grow over a long period. The strategy is named after the idea of buying stocks and storing them in a coffee can, never to be touched again until you decide to sell. This approach minimizes the impact of market volatility and short-term trends, focusing instead on long-term growth.
        """)

    # FAQ 2
    with st.expander("What is the Dollar-Cost Averaging Strategy?"):
        st.write("""
        Dollar-cost averaging (DCA) involves investing a fixed amount of money at regular intervals, regardless of the asset's price. This strategy reduces the impact of volatility by spreading out the investment over time. By purchasing more shares when prices are low and fewer shares when prices are high, DCA can lower the average cost per share and mitigate the risks of market timing.
        """)

    # FAQ 3
    with st.expander("What is the Buy and Hold Strategy?"):
        st.write("""
        The Buy and Hold strategy involves purchasing stocks or other investments and holding them for an extended period, regardless of market fluctuations. The goal is to benefit from the long-term growth of the investment. This strategy requires patience and a belief in the underlying strength of the investments, as it avoids the costs and potential pitfalls associated with frequent trading.
        """)

# Footer
st.write("© 2024 Financial Literacy Course. All rights reserved.")
