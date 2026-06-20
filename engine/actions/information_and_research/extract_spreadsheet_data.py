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

def extract_spreadsheet_data(parameters: dict, player=None):
    """
    Reads a CSV/Excel file and uses Gemini to extract specific data based on the user's prompt.
    """
    file_path = parameters.get("file_path", "").strip()
    query = parameters.get("query", "").strip()

    if not file_path:
        return "Error: Please provide a 'file_path'."
    if not query:
        return "Error: Please provide a 'query' to extract."

    if player:
        player.write_log(f"📊 Extracting data from spreadsheet: {Path(file_path).name}")

    try:
        import pandas as pd
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            df = pd.read_excel(file_path)
        else:
            return "Error: Unsupported file format. Please provide a .csv or .xlsx file."
        
        # Convert to a text representation (limit to 500 rows to avoid token limit)
        data_str = df.head(500).to_string()
        
        model = _get_gemini()
        prompt = f"Analyze this spreadsheet data (up to 500 rows provided) and answer the query.\n\nQuery: {query}\n\nData:\n{data_str}"
        response = model.generate_content(prompt)
        
        return f"✅ Spreadsheet Extraction Complete:\n\n{response.text.strip()}"
    except ImportError:
        return "Error: pandas is not installed. Please pip install pandas."
    except Exception as e:
        return f"Spreadsheet extraction failed: {str(e)}"
