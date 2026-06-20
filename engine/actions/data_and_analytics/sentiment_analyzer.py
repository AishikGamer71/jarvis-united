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

def sentiment_analyzer(parameters: dict, player=None):
    """
    Analyzes the sentiment of provided text or a file's contents.
    Returns Sentiment (Positive/Negative/Neutral), Emotion tags, and a summary.
    """
    text = parameters.get("text", "").strip()
    file_path = parameters.get("file_path", "").strip()

    if player:
        player.write_log("🧠 Analyzing sentiment...")

    if file_path and not text:
        p = Path(file_path)
        if not p.exists():
            return f"Error: File not found at {file_path}"
        try:
            text = p.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading file: {e}"

    if not text:
        return "Error: Please provide either 'text' or a valid 'file_path' to analyze."

    prompt = f"""You are an expert NLP Sentiment Analyzer.
Analyze the following text and provide a structured sentiment report.

Format your response exactly like this:
**Sentiment:** [Positive, Negative, or Neutral]
**Score:** [1 to 100, where 1 is extremely negative and 100 is extremely positive]
**Primary Emotions:** [Comma separated list of 2-3 core emotions detected]
**Reasoning:** [A brief 1-2 sentence explanation of why the text exhibits this sentiment]

Text to analyze:
\"\"\"
{text[:10000]}
\"\"\"
"""

    try:
        model = _get_gemini()
        response = model.generate_content(prompt)
        return f"✅ Sentiment Analysis Complete:\n\n{response.text.strip()}"
    except Exception as e:
        return f"Sentiment Analyzer failed: {str(e)}"
