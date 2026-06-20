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

def fact_check(parameters: dict, player=None):
    """
    Fact-checks a specific claim or text using Gemini.
    """
    claim = parameters.get("claim", "").strip()

    if player:
        player.write_log("🔎 Fact-checking claim...")

    if not claim:
        return "Error: Please provide a 'claim' to fact-check."

    prompt = f"""You are an elite Fact-Checker and Investigative Researcher.
Your objective is to rigorously analyze the following claim and determine its accuracy.

Format your response exactly like this:
**Verdict:** [True, Mostly True, Half True, Mostly False, False, or Unverified]
**The Facts:** [A concise paragraph explaining the objective truth regarding the claim]
**Nuance/Context:** [Explain any missing context, common misconceptions, or nuances that complicate the claim]

Claim to fact-check:
\"\"\"
{claim}
\"\"\"
"""

    try:
        model = _get_gemini()
        response = model.generate_content(prompt)
        report = response.text.strip()
        
        return f"✅ Fact-Check Complete:\n\n{report}"
    except Exception as e:
        return f"Fact Checker failed: {str(e)}"
