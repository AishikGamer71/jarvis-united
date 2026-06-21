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

def archive_compressor(parameters: dict, player=None):
    """Automatically generated capability: archive_compressor"""
    prompt = parameters.get("prompt", "Execute archive_compressor")
    
    if player:
        player.write_log(f"⚡ Executing archive_compressor...")
        
    try:
        model = _get_gemini()
        response = model.generate_content(f"Task: archive_compressor\nContext: {prompt}\nParameters: {parameters}")
        return f"✅ archive_compressor Completed:\n\n{response.text.strip()}"
    except Exception as e:
        return f"archive_compressor failed: {str(e)}"
