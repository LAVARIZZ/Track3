import streamlit as st
import requests

# API key and URL for Financial Modeling Prep
# API_KEY = 'IIox350AjA5uTmnil9oxoZkWkmLy8Urc'
# API_URL = 'https://financialmodelingprep.com/api/v3/search-ticker?query=AA&limit=10&exchange=NASDAQ'


API_KEY = 'c843fc74ad7d44e28e00d37b802ce86f'
API_URL = 'https://newsapi.org/v2/everything?q=tesla&from=2024-06-30&sortBy=publishedAt'

def fetch_data(query):
    params = {
        'query': query,
        'apikey': API_KEY
    }
    response = requests.get(API_URL, params=params)
    return response.json()

def display_articles(articles):
    for article in articles:
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-bottom: 16px; background-color: #ffffff;">
                <h3 style="margin-top: 0;">{article['title']}</h3>
                <p><strong>Author:</strong> {article['author']}</p>
                <p>{article['description']}</p>
                {f'<img src="{article["urlToImage"]}" style="width: 100%; border-radius: 4px;"/>' if article['urlToImage'] else ''}
                <p><a href="{article['url']}" target="_blank">Read more</a></p>
                <p><strong>Published At:</strong> {article['publishedAt']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

def main():
    st.title('Financial News Carousel')

    query = 'financial'  # Modify this query based on your needs
    data = fetch_data(query)

    if data and 'articles' in data and data['articles']:
        st.header('Latest Financial News')
        display_articles(data['articles'])
    else:
        st.write("No data available or failed to fetch data.")

if __name__ == "__main__":
    main()