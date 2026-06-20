import json
import sys
from pathlib import Path

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
    import google.generativeai as genai
    api_key = _get_api_key()
    if not api_key:
        raise ValueError("Gemini API key not found in config/api_keys.json")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def code_reviewer(parameters: dict, player=None):
    """
    Performs a comprehensive, structured code review on a file or raw code snippet using Gemini.
    """
    file_path = parameters.get("file_path", "").strip()
    code = parameters.get("code", "").strip()
    language = parameters.get("language", "python").strip()

    if player:
        player.write_log(f"🔎 Initiating Code Review for {file_path if file_path else 'raw snippet'}...")

    if file_path and not code:
        p = Path(file_path)
        if not p.exists():
            return f"Error: File not found at {file_path}"
        try:
            code = p.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading file: {e}"

    if not code:
        return "Error: No code or file path provided for review."

    prompt = f"""You are a Senior Staff Software Engineer and an expert Code Reviewer.
Perform a strict, comprehensive code review of the following {language} code.

Please structure your review using exactly these sections:
## 🐛 Bugs & Critical Issues
Identify any logic errors, potential crashes, or security vulnerabilities.

## ⚡ Performance & Optimization
Suggest ways to make the code faster or more memory-efficient.

## 🎨 Style & Readability
Identify naming convention violations, lack of comments, or messy structure.

## ✨ Overall Verdict
A 1-2 sentence summary of code quality.

Do NOT rewrite the entire code for them. Point out specific line numbers or snippets where improvements can be made.

Code to review:
```
{code[:15000]}
```"""

    try:
        model = _get_gemini()
        response = model.generate_content(prompt)
        review_report = response.text.strip()
        
        # Save report to storage if it was a file
        if file_path:
            storage_dir = get_base_dir() / "storage"
            storage_dir.mkdir(parents=True, exist_ok=True)
            report_path = storage_dir / f"CodeReview_{Path(file_path).stem}.md"
            report_path.write_text(review_report, encoding="utf-8")
            return f"✅ Code Review Complete. Report saved to {report_path}\n\n{review_report}"
            
        return f"✅ Code Review Complete:\n\n{review_report}"

    except Exception as e:
        return f"Code Review failed: {str(e)}"
