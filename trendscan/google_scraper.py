import os, sys
import pickle
import requests 
from bs4 import BeautifulSoup
from trendscan.scraping_functions import google_scrape
from trendscan import SERP_API_KEY


api_key = SERP_API_KEY

if len(sys.argv) > 1:
    search_text = sys.argv[1]
    pages = sys.argv[2]
else:
    search_text = input("Search query? ")
    pages = input("How many pages? ")

with open('output/search_text.p', 'wb') as f:
    pickle.dump(search_text, f)

results = google_scrape(search_text, api_key, pages)

full_results = []
for result in results:
    link = result.get("link")  # Assumes each result dictionary has a 'link' key
    page_text = None  # Default to None if unable to fetch
    if link:
        try:
            response = requests.get(link, timeout=10)
            response.raise_for_status()  # Check for HTTP errors
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text(separator=" ", strip=True)  # Extract visible text
            print(f"Fetched text from {link}")
        except requests.RequestException as e:
            print(f"Failed to fetch {link}: {e}")
    else:
        print("No link found in result.")

    full_results.append({
        "title": result.get("title"),
        "link": link,
        "snippet": result.get("snippet"),
        "page_text": page_text  # Include the fetched text
    })

with open('output/search_results.p', 'wb') as f:
    pickle.dump(full_results, f)

print("\nSearch results with page text saved to search_results.p")
