import sqlite3
import os
import json
from pathlib import Path

def get_storage_dir():
    cwd = Path(os.getcwd())
    storage_path = cwd / 'storage'
    if not storage_path.exists():
        storage_path.mkdir(parents=True, exist_ok=True)
    return storage_path

def init_db():
    db_path = get_storage_dir() / 'todo.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            priority TEXT DEFAULT 'normal',
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    return db_path

def todo_manager(parameters: dict, player=None):
    action = parameters.get("action", "list")
    task_text = parameters.get("task", "")
    priority = parameters.get("priority", "normal")
    task_id = parameters.get("task_id", None)
    
    db_path = init_db()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        if action == "add":
            if not task_text:
                return "Error: Task text is required."
            cursor.execute("INSERT INTO tasks (task, priority) VALUES (?, ?)", (task_text, priority))
            conn.commit()
            return f"Task added: '{task_text}' (Priority: {priority}, ID: {cursor.lastrowid})"
            
        elif action == "remove":
            if task_id is None:
                return "Error: task_id is required for removal."
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            if cursor.rowcount > 0:
                conn.commit()
                return f"Task {task_id} removed."
            return f"Task {task_id} not found."
            
        elif action == "check":
            if task_id is None:
                return "Error: task_id is required to check off."
            cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
            if cursor.rowcount > 0:
                conn.commit()
                return f"Task {task_id} marked as completed."
            return f"Task {task_id} not found."
            
        elif action == "list":
            cursor.execute("SELECT id, task, priority, status FROM tasks ORDER BY status DESC, id ASC")
            rows = cursor.fetchall()
            if not rows:
                return "Your to-do list is empty."
                
            output = ["--- To-Do List ---"]
            for row in rows:
                tid, txt, prio, status = row
                checkbox = "[X]" if status == "completed" else "[ ]"
                output.append(f"{tid}. {checkbox} {txt} (Priority: {prio})")
            return "\n".join(output)
            
        elif action == "clear_completed":
            cursor.execute("DELETE FROM tasks WHERE status = 'completed'")
            count = cursor.rowcount
            conn.commit()
            return f"Cleared {count} completed tasks."
            
        else:
            return f"Unknown action: {action}"
            
    except Exception as e:
        return f"Todo Manager Error: {str(e)}"
    finally:
        conn.close()
