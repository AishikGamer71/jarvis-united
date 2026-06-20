import json
import sys
from pathlib import Path
import google.generativeai as genai

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent.parent

def _get_api_key() -> str:
    api_config_path = get_base_dir() / "config" / "api_keys.json"
    try:
        with open(api_config_path, "r", encoding="utf-8") as f:
            return json.load(f)["gemini_api_key"]
    except Exception:
        return ""

def _get_gemini():
    api_key = _get_api_key()
    if not api_key:
        raise ValueError("Gemini API key not found")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def summarize_articles(parameters: dict, player=None):
    """
    Fetches a web page and uses Gemini to summarize the article.
    """
    url = parameters.get("url", "").strip()

    if not url:
        return "Error: Please provide a 'url' to summarize."

    if player:
        player.write_log(f"📰 Summarizing article from: {url}")

    try:
        import requests
        from bs4 import BeautifulSoup
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Remove script/style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
            
        text = soup.get_text(separator=' ', strip=True)
        # Limit to roughly 30000 characters
        text = text[:30000]
        
        model = _get_gemini()
        prompt = f"Please provide a comprehensive summary of this article, highlighting the main points, key arguments, and conclusions.\n\nArticle Text:\n{text}"
        response = model.generate_content(prompt)
        
        return f"✅ Article Summary:\n\n{response.text.strip()}"
    except ImportError:
        return "Error: requests or beautifulsoup4 is not installed."
    except Exception as e:
        return f"Article summarization failed: {str(e)}"
