import pandas as pd
import matplotlib.pyplot as plt
import os
import uuid
import json
from pathlib import Path

def get_storage_dir():
    cwd = Path(os.getcwd())
    storage_path = cwd / 'storage'
    storage_path.mkdir(parents=True, exist_ok=True)
    return storage_path

def chart_generator(parameters: dict, player=None):
    """
    Generates high-quality charts from either file paths (CSV/JSON/Excel) or raw JSON data.
    """
    filepath = parameters.get("filepath", "")
    raw_data = parameters.get("raw_data", "")
    chart_type = parameters.get("chart_type", "bar").lower()
    x_col = parameters.get("x_col", "")
    y_col = parameters.get("y_col", "")
    title = parameters.get("title", f"{y_col} by {x_col}")
    
    if player:
        player.write_log(f"📊 Generating {chart_type} chart...")

    storage_dir = get_storage_dir()
    
    try:
        # Load Data
        df = None
        if raw_data:
            try:
                data = json.loads(raw_data)
                df = pd.DataFrame(data)
            except Exception as e:
                return f"Error parsing raw_data JSON: {str(e)}"
        elif filepath:
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
        else:
            return "Error: You must provide either 'filepath' or 'raw_data'."

        if df is None or df.empty:
            return "Error: DataFrame is empty or could not be loaded."

        # Verify columns exist if explicitly provided
        if x_col and x_col not in df.columns:
            return f"Error: X column '{x_col}' not found in dataset. Available: {list(df.columns)}"
        
        # If y_col is a comma-separated list, plot multiple lines/bars
        y_cols = [y.strip() for y in y_col.split(",")] if y_col else []
        for y in y_cols:
            if y not in df.columns:
                return f"Error: Y column '{y}' not found in dataset. Available: {list(df.columns)}"
        
        # If no columns provided, just try to plot the whole dataframe
        if not x_col and not y_cols:
            x_col = df.columns[0]
            y_cols = [c for c in df.columns[1:] if pd.api.types.is_numeric_dtype(df[c])]

        # Use ggplot style for premium aesthetics
        plt.style.use('ggplot')
        plt.figure(figsize=(10, 6))
        
        # Draw Chart
        y_arg = y_cols[0] if len(y_cols) == 1 else y_cols
        
        if chart_type == "bar":
            df.plot.bar(x=x_col, y=y_arg, ax=plt.gca(), color='cornflowerblue')
        elif chart_type == "line":
            df.plot.line(x=x_col, y=y_arg, ax=plt.gca(), linewidth=2, marker='o')
        elif chart_type == "scatter":
            if len(y_cols) == 1:
                df.plot.scatter(x=x_col, y=y_arg, ax=plt.gca(), color='darkorange', s=50)
            else:
                return "Scatter plots only support a single Y column."
        elif chart_type == "pie":
            if len(y_cols) == 1:
                df.set_index(x_col).plot.pie(y=y_arg, ax=plt.gca(), autopct='%1.1f%%', cmap='viridis')
                plt.ylabel("") # Clean up pie charts
            else:
                return "Pie charts only support a single Y column."
        elif chart_type == "hist" or chart_type == "histogram":
            df[y_arg].plot.hist(ax=plt.gca(), bins=20, alpha=0.7, color='mediumseagreen')
        else:
            return f"Unsupported chart_type: {chart_type}"

        # Formatting
        plt.title(title, fontsize=16, fontweight='bold', pad=15)
        plt.xlabel(x_col if x_col else "", fontsize=12)
        if chart_type != "pie":
            plt.ylabel(", ".join(y_cols) if y_cols else "", fontsize=12)
        
        plt.tight_layout()
        
        # Save to Storage
        chart_filename = f"chart_{chart_type}_{uuid.uuid4().hex[:6]}.png"
        chart_path = storage_dir / chart_filename
        plt.savefig(str(chart_path), dpi=300)
        plt.close()
        
        return f"✅ Beautiful {chart_type.capitalize()} chart generated successfully!\nSaved to: {chart_path}"
        
    except Exception as e:
        return f"Chart Generator Error: {str(e)}"
