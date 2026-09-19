import urllib.request
import feedparser

def fetch_latest_papers(category="cat:cs.LG", search_text="", max_results=20):
    """
    Fetches the latest papers from ArXiv based on a category query and optional keyword search.
    """
    query = category
    if search_text:
        # ArXiv API uses 'all:' for global keyword searches. Spaces must become '+'
        formatted_search = search_text.replace(" ", "+")
        query += f'+AND+all:{formatted_search}'
        
    # sortBy=submittedDate ensures the baseline payload is always the most recent papers
    url = f'http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}'
    
    try:
        response = urllib.request.urlopen(url)
        feed = feedparser.parse(response)
        return feed.entries
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []