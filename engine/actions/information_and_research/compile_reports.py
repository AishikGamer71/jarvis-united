import json
import sys
import uuid
import time
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

def compile_reports(parameters: dict, player=None):
    """
    Compiles data and information into a highly structured, professional report.
    """
    topic = parameters.get("topic", "").strip()
    data = parameters.get("data", "").strip()

    if player:
        player.write_log(f"📊 Compiling report on '{topic}'...")

    if not topic:
        return "Error: Please provide a 'topic' for the report."

    prompt = f"""You are an elite Business Analyst and Research Assistant.
Your objective is to compile a highly professional, well-structured report on the following topic.
If data or context is provided, integrate it deeply into the report.

Topic: {topic}
Provided Data/Context: {data if data else 'None provided, rely on your internal knowledge.'}

Structure the report using markdown formatting with the following sections:
# Executive Summary
[High-level overview of the topic and key takeaways]

## Introduction & Background
[Context and background information]

## Key Findings & Analysis
[Detailed analysis, bullet points, data breakdown]

## Conclusion & Recommendations
[Final thoughts and actionable recommendations]
"""

    try:
        model = _get_gemini()
        response = model.generate_content(prompt)
        report = response.text.strip()
        
        # Save report to storage
        storage_dir = get_base_dir() / "storage"
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        report_filename = f"Report_{topic.replace(' ', '_').replace('/', '_')}_{uuid.uuid4().hex[:4]}.md"
        report_path = storage_dir / report_filename
        
        report_path.write_text(report, encoding="utf-8")
        
        return f"✅ Report Compilation Complete for '{topic}'.\nSaved to: {report_path}\n\nHere is the Executive Summary:\n{report.split('##')[0].strip()}"
    except Exception as e:
        return f"Report Compiler failed: {str(e)}"
