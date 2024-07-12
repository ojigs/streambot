"""
This script extracts URLs from specified websites and saves them to text files.
It fetches the content of each website, parses the HTML to find all anchor tags,
and writes the URLs to a file named after the website.
"""

import time
from urllib.parse import urljoin
from urllib.error import URLError, HTTPError
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException


def extract_urls(base_url, timeout=10):
    """Extract URLs from a given base URL."""
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'https://' + base_url
    # Selenium setup
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(base_url)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        links = driver.find_elements(By.TAG_NAME, "a")
        urls = [urljoin(base_url, link.get_attribute("href")) for link in links if link.get_attribute("href")]
    except (URLError, HTTPError, WebDriverException) as e:
        st.error(f"Failed to retrieve {base_url}: {e}")
        print(f"Failed to retrieve {base_url}: {e}")
        urls = []
    finally:
        driver.quit()

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
            background-color: #1c61d9;
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
            with st.spinner("Extracting URLs... Please wait, this may take a while"):
                urls = extract_urls(url)
            if urls:
                st.write("### Extracted URLs:")
                for extracted_urls in urls:
                    st.write(f" - {extracted_urls}")
            else:
                st.write("### No URLs found for this website")
        else:
            st.error("Please enter a valid URL")

    st.markdown("<footer>© 2024 <a href='https://ojigs.netlify.app' target='_blank'>Emmanuel Ojighoro</a></footer>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
