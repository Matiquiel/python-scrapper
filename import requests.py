import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse

# Function to fetch URLs from a sitemap and filter based on a specific path prefix
def fetch_urls_from_sitemap(sitemap_url, path_prefix):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    urls = [url.text.strip() for url in soup.find_all('loc') if url.text.strip().startswith(path_prefix)]
    return urls

# Function to scrape a webpage and extract text content
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text_content = soup.get_text()
    return text_content

# Function to clean the text content
def clean_text(text):
    cleaned_text = text.strip()
    return cleaned_text

# Function to save text content to a file
def save_to_file(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def scrape_section(sitemap, path_prefix):
    print(f"Checking Prefix {path_prefix}")
    # Example sitemap URL
    # Fetch URLs from sitemap and filter based on path prefix
    urls = fetch_urls_from_sitemap(sitemap, path_prefix)

    if(os.path.exists("./output")):
        os.mkdir('./output')

    # Scrape and save content for each URL
    for url in urls:
        print(f"Reading url {url}")
        # Extract filename from URL
        parsed_url = urlparse(url)

        filename = './output' + os.path.basename(parsed_url.path) + '.txt'
        
        # Scrape page content
        page_content = scrape_page(url)
        
        # Clean and save content to file
        cleaned_page_content = clean_text(page_content)
        if os.path.exists(filename)== False:
            save_to_file(cleaned_page_content, filename)
            print(f"Content saved to {filename}")

def main():
    sitemap_url = 'https://mysite.com/sitemap.xml'
    scrape_section(sitemap_url,"https://mysite.com/interestingsubsection")

if __name__ == "__main__":
    main()