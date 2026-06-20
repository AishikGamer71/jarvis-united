import sys
from pathlib import Path
import sqlite3
import datetime

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent.parent

def productivity_tracker(parameters: dict, player=None):
    """
    Tracks productivity tasks.
    """
    action = parameters.get("action", "log").strip()
    task = parameters.get("task", "").strip()
    duration = parameters.get("duration", 0)

    storage_dir = get_base_dir() / "storage"
    storage_dir.mkdir(parents=True, exist_ok=True)
    db_path = storage_dir / "productivity.sqlite"

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS productivity
                 (id INTEGER PRIMARY KEY, task TEXT, duration INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    if player:
        player.write_log(f"📈 Productivity Tracker: {action}")

    try:
        if action == "log":
            c.execute("INSERT INTO productivity (task, duration) VALUES (?, ?)", (task, int(duration)))
            conn.commit()
            return f"✅ Logged {duration} minutes for task: {task}"
        elif action == "summary":
            c.execute("SELECT task, SUM(duration) FROM productivity GROUP BY task")
            rows = c.fetchall()
            summary = "\n".join([f"- {r[0]}: {r[1]} mins" for r in rows])
            return f"📊 Productivity Summary:\n{summary}" if summary else "No tasks logged yet."
        else:
            return f"Unknown action: {action}"
    finally:
        conn.close()
