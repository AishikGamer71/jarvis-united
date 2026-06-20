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

def summarize_documents(parameters: dict, player=None):
    """
    Summarizes a document or raw text using Gemini.
    """
    text = parameters.get("text", "").strip()
    file_path = parameters.get("file_path", "").strip()
    length = parameters.get("length", "medium").lower()

    if player:
        player.write_log("📄 Summarizing document...")

    if file_path and not text:
        p = Path(file_path)
        if not p.exists():
            return f"Error: File not found at {file_path}"
        try:
            text = p.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading file: {e}"

    if not text:
        return "Error: Please provide either 'text' or a valid 'file_path' to summarize."

    length_instruction = {
        "short": "Provide a very brief 1-2 paragraph summary.",
        "medium": "Provide a comprehensive summary covering the main points and key takeaways in bullet points.",
        "long": "Provide a highly detailed, extensive summary including all major sections, arguments, and conclusions."
    }.get(length, "Provide a comprehensive summary.")

    prompt = f"""You are an expert Document Summarizer.
{length_instruction}

Document Content:
\"\"\"
{text[:20000]}
\"\"\"
"""

    try:
        model = _get_gemini()
        response = model.generate_content(prompt)
        summary = response.text.strip()
        
        # Save summary to storage if it was a file
        if file_path:
            storage_dir = get_base_dir() / "storage"
            storage_dir.mkdir(parents=True, exist_ok=True)
            summary_path = storage_dir / f"Summary_{Path(file_path).stem}.md"
            summary_path.write_text(summary, encoding="utf-8")
            return f"✅ Summary Complete. Saved to {summary_path}\n\n{summary}"
            
        return f"✅ Summary Complete:\n\n{summary}"
    except Exception as e:
        return f"Document Summarizer failed: {str(e)}"
