"""
This script extracts URLs from specified websites and saves them to text files.
It fetches the content of each website, parses the HTML to find all anchor tags,
and writes the URLs to a file named after the website.
"""

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import streamlit as st


def extract_urls(base_url, timeout=10):
    """Extract URLs from a given base URL."""
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'https://' + base_url

    try:
        response = requests.get(base_url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve {base_url}: {e}")
        return []
    soup = BeautifulSoup(response.content, "html.parser")
    urls = []

    for link in soup.find_all("a", href=True):
        url = urljoin(base_url, link["href"])
        urls.append(url)
    return urls


def save_urls_to_file(urls, filename):
    """Save extracted URLs to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        for url in urls:
            file.write(url + "\n")


def main():
    """Main function to extract and render URLs from specified websites."""
    st.markdown(
        """
        <style>
        body {
            background-color: #0d1b2a;
            color: #ffffff;
        }
        .main {
            background-color: #0d1b2a;
        }
        .stTextInput > div > div > input {
            background-color: #1b263b;
            color: #ffffff
        }
        .stButton > button {
            background-color: #1b263b;
            color: #ffffff
        }
        footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            background-color: #1b263b;
            color: #ffffff;
            padding: 10px 10px;
        }
        .css-1aumxhk {
            padding-bottom: 50px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("streemBot")
    st.header("Extract URLS from websites")

    url = st.text_input("Enter the website URL", "")
    if st.button("Extract URLs"):
        if url:
            urls = extract_urls(url)
            if urls:
                st.write("### Extracted URLs:")
                for extracted_urls in urls:
                    st.write(f" - {extracted_urls}")
            else:
                st.write("### No URLs found for this website")
        else:
            st.error("Olease inout a valid URL")
    st.markdown("<footer>© 2024 <a href='https://ojigs.netlify.app' target='_blank'>Emmanuel Ojighoro</a></footer>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
