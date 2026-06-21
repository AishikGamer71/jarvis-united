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

def marketing_copy_generator(parameters: dict, player=None):
    """Automatically generated capability: marketing_copy_generator"""
    prompt = parameters.get("prompt", "Execute marketing_copy_generator")
    
    if player:
        player.write_log(f"⚡ Executing marketing_copy_generator...")
        
    try:
        model = _get_gemini()
        response = model.generate_content(f"Task: marketing_copy_generator\nContext: {prompt}\nParameters: {parameters}")
        return f"✅ marketing_copy_generator Completed:\n\n{response.text.strip()}"
    except Exception as e:
        return f"marketing_copy_generator failed: {str(e)}"
