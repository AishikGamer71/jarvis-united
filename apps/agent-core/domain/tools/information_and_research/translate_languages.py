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
        raise ValueError("Gemini API key not found in config/api_keys.json")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def translate_languages(parameters: dict, player=None):
    """
    Translates text or a document to a specified target language using Gemini.
    """
    text = parameters.get("text", "").strip()
    file_path = parameters.get("file_path", "").strip()
    target_language = parameters.get("target_language", "English").strip()

    if player:
        player.write_log(f"🌍 Translating to {target_language}...")

    if file_path and not text:
        p = Path(file_path)
        if not p.exists():
            return f"Error: File not found at {file_path}"
        try:
            text = p.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading file: {e}"

    if not text:
        return "Error: Please provide either 'text' or a valid 'file_path' to translate."

    prompt = f"""You are a Master Linguist and Translator.
Translate the following text into fluent, natural-sounding {target_language}.
Preserve the original tone, formatting, and any technical terminology where appropriate.

If the text is already in {target_language}, reply saying it is already in the target language.

Do NOT add any extra markdown formatting or conversational filler before or after the translation. Just return the translated text.

Text to translate:
\"\"\"
{text[:30000]}
\"\"\"
"""

    try:
        model = _get_gemini()
        response = model.generate_content(prompt)
        translation = response.text.strip()
        
        # Save translation to storage if it was a file
        if file_path:
            storage_dir = get_base_dir() / "storage"
            storage_dir.mkdir(parents=True, exist_ok=True)
            translation_path = storage_dir / f"Translation_{target_language}_{Path(file_path).stem}.txt"
            translation_path.write_text(translation, encoding="utf-8")
            return f"✅ Translation to {target_language} Complete. Saved to {translation_path}\n\n{translation}"
            
        return f"✅ Translation ({target_language}):\n\n{translation}"
    except Exception as e:
        return f"Language Translator failed: {str(e)}"
