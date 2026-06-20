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

def extract_structured_data(parameters: dict, player=None):
    """
    Extracts structured JSON data from unstructured text using Gemini.
    """
    text = parameters.get("text", "").strip()
    schema = parameters.get("schema", "").strip()

    if not text:
        return "Error: Please provide 'text' to extract from."
    if not schema:
        return "Error: Please provide a 'schema' describing what to extract."

    if player:
        player.write_log(f"🧠 Extracting structured data from text...")

    prompt = f"Extract structured data from the text below according to this schema/description:\n{schema}\n\nText:\n{text}\n\nReturn ONLY valid JSON."
    
    try:
        model = _get_gemini()
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        
        if raw_text.startswith("```json"): raw_text = raw_text[7:]
        if raw_text.startswith("```"): raw_text = raw_text[3:]
        if raw_text.endswith("```"): raw_text = raw_text[:-3]
        
        # Try to parse to ensure it's valid
        parsed = json.loads(raw_text.strip())
        return json.dumps(parsed, indent=2)
    except Exception as e:
        return f"Structured data extraction failed: {str(e)}"
