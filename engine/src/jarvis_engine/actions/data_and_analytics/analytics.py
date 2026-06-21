import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os
import json
import uuid
from pathlib import Path

def get_storage_dir():
    # Attempt to resolve storage dir relative to the project root
    cwd = Path(os.getcwd())
    storage_path = cwd / 'storage'
    if not storage_path.exists():
        storage_path.mkdir(parents=True, exist_ok=True)
    return storage_path

def data_analytics(parameters: dict, player=None):
    action = parameters.get("action", "")
    filepath = parameters.get("filepath", "")
    query = parameters.get("query", "")
    chart_type = parameters.get("chart_type", "bar")
    x_col = parameters.get("x_col", "")
    y_col = parameters.get("y_col", "")
    
    storage_dir = get_storage_dir()
    
    try:
        if action == "analyze":
            if not os.path.exists(filepath):
                return f"File not found: {filepath}"
                
            if filepath.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif filepath.endswith('.json'):
                df = pd.read_json(filepath)
            elif filepath.endswith('.xlsx'):
                df = pd.read_excel(filepath)
            else:
                return "Unsupported file format. Please use CSV, JSON, or Excel."
                
            stats = df.describe(include='all').to_json()
            head = df.head(5).to_json()
            columns = list(df.columns)
            
            summary = f"Columns: {columns}\n\nTop 5 rows:\n{head}\n\nStatistics:\n{stats}"
            return summary[:2000] # Return summarized info
            
        elif action == "chart":
            if not os.path.exists(filepath):
                return f"File not found: {filepath}"
                
            if filepath.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif filepath.endswith('.json'):
                df = pd.read_json(filepath)
            elif filepath.endswith('.xlsx'):
                df = pd.read_excel(filepath)
            else:
                return "Unsupported file format."
                
            if x_col not in df.columns or y_col not in df.columns:
                return f"Columns {x_col} or {y_col} not found in dataset."
                
            plt.figure(figsize=(10, 6))
            if chart_type == "bar":
                df.plot.bar(x=x_col, y=y_col)
            elif chart_type == "line":
                df.plot.line(x=x_col, y=y_col)
            elif chart_type == "scatter":
                df.plot.scatter(x=x_col, y=y_col)
            elif chart_type == "pie":
                df.set_index(x_col).plot.pie(y=y_col, autopct='%1.1f%%')
            else:
                df.plot(x=x_col, y=y_col)
                
            plt.title(f"{y_col} by {x_col}")
            plt.tight_layout()
            
            chart_filename = f"chart_{uuid.uuid4().hex[:8]}.png"
            chart_path = storage_dir / chart_filename
            plt.savefig(str(chart_path))
            plt.close()
            
            return f"Chart generated and saved to {chart_path}. You can view it in the gallery or storage folder."
            
        elif action == "sql":
            db_path = filepath if filepath else str(storage_dir / 'database.sqlite')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute(query)
                if query.strip().upper().startswith("SELECT"):
                    rows = cursor.fetchall()
                    cols = [description[0] for description in cursor.description]
                    return f"Query successful. Columns: {cols}\nRows: {rows[:10]}" # Return max 10 rows
                else:
                    conn.commit()
                    return f"Query executed successfully. {cursor.rowcount} rows affected."
            except Exception as e:
                return f"SQL Error: {str(e)}"
            finally:
                conn.close()
                
        else:
            return f"Unknown action: {action}"
            
    except Exception as e:
        return f"Data Analytics Error: {str(e)}"
