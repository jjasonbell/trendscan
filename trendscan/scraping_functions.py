import serpapi 
import pickle

def get_google_results(search_term, api_key, pages=1):
    """Fetches both organic and sponsored search results using SerpApi's Google search engine."""
    results = []
    pages = int(pages)
    for i in range(pages):
        params = {
            "q": search_term,
            "engine": "google",
            "api_key": api_key,
            "start": i * 10,  # Pagination: 10 results per page
            "location": "Austin, Texas",  # Adjust this location if needed
            "hl": "en",
            "gl": "us"
        }
        
        # Call the serpapi search function directly
        search = serpapi.search(**params)
        search_results = search.get("organic_results", []) + search.get("ads", [])
        
        results.extend(search_results)
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