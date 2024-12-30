import streamlit as st
import requests
from bs4 import BeautifulSoup

# Hardcoded NewsAPI key
NEWS_API_KEY = "27f827bbf2a94b3d8a2051e1d0bc061d"  # Replace with your NewsAPI key

# Function to fetch the latest technology news from NewsAPI.org
def fetch_tech_news():
    try:
        # URL for NewsAPI.org API
        url = f"https://newsapi.org/v2/top-headlines?apiKey={NEWS_API_KEY}&category=technology&language=en"

        # Fetch the news
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for failed requests
        data = response.json()

        # Extract news items
        news_items = []
        for item in data.get("articles", []):
            news_items.append({
                "title": item.get("title"),
                "link": item.get("url"),
                "published_date": item.get("publishedAt"),
                "description": item.get("description", "No description available."),
                "image_url": item.get("urlToImage")
            })

        # Limit to 100 news items if there are more
        return news_items[:100]
    except Exception as e:
        return str(e)

# Function to extract full description from the article's URL
def extract_full_description(url):
    try:
        # Request the article's page content
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try to find the main content of the article (this can vary based on the site)
        # Example: Find the first <p> element or a specific class for content
        paragraphs = soup.find_all('p')

        # Join all paragraphs into a single string
        full_description = ' '.join([para.get_text() for para in paragraphs])

        return full_description if full_description else "No full description available."
    except Exception as e:
        return "Error extracting description from the article."

# Main function to display the Streamlit app
def main():
    st.title("Tech News Viewer")
    st.header("Latest Technology News")

    if "news" not in st.session_state:
        with st.spinner("Fetching news..."):
            st.session_state.news = fetch_tech_news()

    news = st.session_state.news

    if isinstance(news, str):
        st.error(f"Failed to fetch news: {news}")
    else:
        if "current_index" not in st.session_state:
            st.session_state.current_index = 0

        total_news = len(news)

        # Function to display the news item in a simple format (no card)
        def show_news_item(index):
            item = news[index]

            # Display the news item in a simple format with text and image
            if item["image_url"]:
                st.image(item["image_url"], use_container_width=True)
            st.subheader(item["title"])
            st.markdown(f"**Description:** {item['description']}")

            # Extract the full description from the article link
            full_description = extract_full_description(item['link'])

            # Beautified Full Description
            st.markdown("### Full Description")
            st.markdown(f"<div style='line-height: 1.8;'>{full_description}</div>", unsafe_allow_html=True)

            st.markdown(f"**Published on:** {item['published_date']}")
            st.markdown(f"[Read more]({item['link']})")

        # Display the Previous and Next buttons side by side, aligned above the news item
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if st.button("⬅️ Previous") and st.session_state.current_index > 0:
                st.session_state.current_index -= 1

        with col3:
            if st.button("➡️ Next") and st.session_state.current_index < total_news - 1:
                st.session_state.current_index += 1

        # Show the current news item
        show_news_item(st.session_state.current_index)

if __name__ == "__main__":
    main()
