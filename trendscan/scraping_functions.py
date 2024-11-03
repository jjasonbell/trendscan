from serpapi import GoogleSearch
import pickle

def get_google_results(search_term, api_key, pages=1):
    """Fetches both organic and sponsored search results using SerpApi's Google search engine."""
    results = []
    pages = int(pages)
    for i in range(pages):
        params = {
            "engine": "google",
            "q": search_term,
            "api_key": api_key,
            "start": i * 10  # Pagination: 10 results per page
        }
        search = GoogleSearch(params)
        search_results = search.get_dict()
        organic_results = search_results.get("organic_results", [])
        ads = search_results.get("ads", [])
        
        results.extend(organic_results + ads)
        print(f'Page {i + 1} of Google results gathered (organic and sponsored).')
        
    return results

def extract_text(result):
    """Extracts relevant text content from a single SerpApi result."""
    title = result.get("title", "")
    snippet = result.get("snippet", "")
    link = result.get("link", "")
    return {"title": title, "snippet": snippet, "link": link}


def google_scrape(search_text, api_key, pages=1):
    """Retrieves Google search results for a given search term, cleans the text, and saves it to a file."""
    raw_results = get_google_results(search_text, api_key, pages)
    cleaned_results = [extract_text(result) for result in raw_results]
    with open("search_results.p", "wb") as f:
        pickle.dump(cleaned_results, f)
    return cleaned_results