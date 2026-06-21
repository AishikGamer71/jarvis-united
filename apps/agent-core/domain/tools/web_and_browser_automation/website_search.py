import sys
from pathlib import Path
import webbrowser
import urllib.parse

def website_search(parameters: dict, player=None):
    """
    Performs a site-specific Google search.
    """
    domain = parameters.get("domain", "").strip()
    query = parameters.get("query", "").strip()

    if not domain or not query:
        return "Error: Provide both 'domain' and 'query'."

    if player:
        player.write_log(f"🔍 Searching {domain} for '{query}'")

    try:
        search_term = f"site:{domain} {query}"
        url = f"https://www.google.com/search?q={urllib.parse.quote(search_term)}"
        webbrowser.open(url)
        return f"✅ Opened Google Search for '{query}' on {domain}."
    except Exception as e:
        return f"Website search failed: {str(e)}"
