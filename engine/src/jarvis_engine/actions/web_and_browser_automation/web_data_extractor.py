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

def web_data_extractor(parameters: dict, player=None):
    """
    Extracts data from a website using Gemini.
    """
    url = parameters.get("url", "").strip()
    query = parameters.get("query", "").strip()

    if not url or not query:
        return "Error: Provide both 'url' and 'query'."

    if player:
        player.write_log(f"🕷️ Extracting '{query}' from {url}")

    try:
        import requests
        from bs4 import BeautifulSoup
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
            
        text = soup.get_text(separator=' ', strip=True)
        text = text[:30000]
        
        model = _get_gemini()
        prompt = f"Extract the following information from the website text below.\n\nQuery: {query}\n\nWebsite Text:\n{text}"
        response = model.generate_content(prompt)
        
        return f"✅ Web Data Extraction Complete:\n\n{response.text.strip()}"
    except Exception as e:
        return f"Web data extraction failed: {str(e)}"
