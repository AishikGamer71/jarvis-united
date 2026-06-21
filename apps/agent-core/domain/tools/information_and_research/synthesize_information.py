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

def synthesize_information(parameters: dict, player=None):
    """
    Synthesizes multiple text sources or documents into one cohesive summary.
    """
    sources = parameters.get("sources", [])
    topic = parameters.get("topic", "General Synthesis").strip()

    if not sources or not isinstance(sources, list):
        return "Error: Please provide a list of 'sources' (text strings or file paths)."

    if player:
        player.write_log(f"🧬 Synthesizing {len(sources)} sources for topic: {topic}")

    combined_text = ""
    for idx, source in enumerate(sources):
        if len(source) < 260 and Path(source).is_file():
            try:
                content = Path(source).read_text(encoding="utf-8", errors="ignore")
                combined_text += f"\n--- Source {idx+1} ({Path(source).name}) ---\n{content[:10000]}\n"
            except Exception:
                combined_text += f"\n--- Source {idx+1} (Raw Text) ---\n{source[:10000]}\n"
        else:
            combined_text += f"\n--- Source {idx+1} (Raw Text) ---\n{source[:10000]}\n"

    prompt = f"""You are an expert analyst. Synthesize the following information sources into a single, cohesive, well-structured document focusing on: {topic}.
Identify common themes, conflicting information, and draw overarching conclusions.

{combined_text}
"""
    
    try:
        model = _get_gemini()
        response = model.generate_content(prompt)
        report = response.text.strip()
        
        storage_dir = get_base_dir() / "storage"
        storage_dir.mkdir(parents=True, exist_ok=True)
        report_filename = f"Synthesis_{topic.replace(' ', '_').replace('/', '_')}_{uuid.uuid4().hex[:4]}.md"
        report_path = storage_dir / report_filename
        report_path.write_text(report, encoding="utf-8")
        
        return f"✅ Synthesis Complete.\nSaved to: {report_path}\n\nSnapshot:\n{report[:500]}..."
    except Exception as e:
        return f"Information synthesis failed: {str(e)}"
