# web_search.py

import requests
from bs4 import BeautifulSoup

def wiki_search(query):
    """Search Wikipedia and return the summary if available."""
    try:
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        res = requests.get(api_url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            return data.get("extract")
    except Exception as e:
        print("❌ Wikipedia search failed:", e)
    return None


def scrape_brave(query):
    """Scrape Brave search results and return top 3 snippets."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/119.0.0.0 Safari/537.36"
        )
    }
    url = f"https://search.brave.com/search?q={query.replace(' ', '+')}"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        results = []
        for tag in soup.select("div.snippet"):
            txt = tag.get_text(strip=True)
            if txt and txt not in results:
                results.append(txt)
            if len(results) >= 3:
                break

        if results:
            return "\n".join(results)
        else:
            raise ValueError("No Brave search results found")

    except Exception as e:
        print("❌ Brave search failed:", e)
        return None


def unified_search(query):
    """Try Wikipedia first, then fallback to Brave search."""
    wiki_result = wiki_search(query)
    if wiki_result:
        return f"📚 From Wikipedia:\n{wiki_result}"

    brave_result = scrape_brave(query)
    if brave_result:
        return f"🌐 From Brave Search:\n{brave_result}"

    return "Sorry, I couldn't find any relevant information."


# Test
if __name__ == "__main__":
    query = "current status of AI regulation in Europe"
    print(unified_search(query))
