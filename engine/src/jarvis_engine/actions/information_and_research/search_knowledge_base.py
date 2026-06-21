import requests

def search_knowledge_base(parameters: dict, player=None):
    """
    Searches Wikipedia (as a global knowledge base) for a specific topic.
    """
    query = (parameters or {}).get("query", "").strip()
    if not query:
        return "Error: Please specify a search query."
        
    if player:
        player.write_log(f"🧠 Searching Global Knowledge Base for: '{query}'...")
        
    try:
        # Wikipedia summary API
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(query)}"
        response = requests.get(url, headers={"User-Agent": "JARVIS-Unified/1.0"})
        
        if response.status_code == 200:
            data = response.json()
            title = data.get("title", query)
            extract = data.get("extract", "No summary found.")
            url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
            
            return f"**Knowledge Base Results for '{title}':**\n\n{extract}\n\n*Source: {url}*"
        elif response.status_code == 404:
            # Fallback to search API
            search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={requests.utils.quote(query)}&limit=3&namespace=0&format=json"
            search_response = requests.get(search_url)
            if search_response.status_code == 200:
                results = search_response.json()
                if len(results) > 1 and len(results[1]) > 0:
                    titles = results[1]
                    links = results[3]
                    out = f"No direct page found for '{query}'. Did you mean one of these?\n"
                    for t, l in zip(titles, links):
                        out += f"- {t}: {l}\n"
                    return out
            return f"Could not find any knowledge base entries for '{query}'."
        else:
            return f"Error connecting to Knowledge Base: HTTP {response.status_code}"
            
    except Exception as e:
        return f"Knowledge Base search failed: {str(e)}"
