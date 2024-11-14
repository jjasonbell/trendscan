import sys
import pickle
import requests
import csv
import json
from bs4 import BeautifulSoup
from pathlib import Path
from trendscan.scraping_functions import google_scrape
from trendscan import SERP_API_KEY

api_key = SERP_API_KEY

# Define the input and output files relative to the script's location
base_dir = Path(__file__).resolve().parent
input_file = base_dir / '../output/exploding_topics.csv'
output_file = base_dir / '../output/exploding_topics_search_results.json'

# Read search queries from the CSV file
search_queries = []
with open(input_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        search_queries.append(row['title'])

all_results = []

for search_text in search_queries:
    print(f"Processing search query: {search_text}")
    results = google_scrape(search_text, api_key, pages=1)  # Assuming 1 page for each query

    full_results = []
    for result in results:
        link = result.get("link") 
        page_text = None  
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

    all_results.append({
        "search_query": search_text,
        "results": full_results
    })

with open(output_file, 'w') as f:
    json.dump(all_results, f, indent=4)

print(f"\nSearch results saved to {output_file}")