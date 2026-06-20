import json
import sys
import uuid
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
    return genai.GenerativeModel("gemini-2.5-pro")

def generate_research_briefs(parameters: dict, player=None):
    """
    Uses Gemini to synthesize a 1-page research brief on a given topic.
    """
    topic = parameters.get("topic", "").strip()
    context = parameters.get("context", "").strip()

    if not topic:
        return "Error: Please provide a 'topic' for the research brief."

    if player:
        player.write_log(f"📚 Generating research brief on: {topic}")

    prompt = f"""You are an elite researcher. Create a concise, 1-page research brief on the following topic.
Include an executive summary, key historical context, current state of the art, and future outlook.

Topic: {topic}
Additional Context: {context if context else 'None provided.'}
"""
    
    try:
        model = _get_gemini()
        response = model.generate_content(prompt)
        report = response.text.strip()
        
        storage_dir = get_base_dir() / "storage"
        storage_dir.mkdir(parents=True, exist_ok=True)
        report_filename = f"Research_Brief_{topic.replace(' ', '_').replace('/', '_')}_{uuid.uuid4().hex[:4]}.md"
        report_path = storage_dir / report_filename
        report_path.write_text(report, encoding="utf-8")
        
        return f"✅ Research Brief Generated.\nSaved to: {report_path}\n\nSummary:\n{report.split('##')[0][:500]}..."
    except Exception as e:
        return f"Research brief generation failed: {str(e)}"
