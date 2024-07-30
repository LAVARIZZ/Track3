import streamlit as st
import requests

# API key and URL for NewsAPI
API_KEY = 'c843fc74ad7d44e28e00d37b802ce86f'
API_URL = 'https://newsapi.org/v2/everything'

def fetch_data(keyword):
    params = {
        'q': keyword,
        'sortBy': 'publishedAt',
        'apiKey': API_KEY
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

    keyword = st.text_input('Enter keyword for news search', 'financial')
    if keyword:
        data = fetch_data(keyword)

        if data and 'articles' in data and data['articles']:
            st.header('Latest Financial News')
            display_articles(data['articles'])
        else:
            st.write("No data available or failed to fetch data.")

if __name__ == "__main__":
    main()
