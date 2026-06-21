import sys
from pathlib import Path
import json

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent.parent

def reminder_manager(parameters: dict, player=None):
    """
    Manages reminders in a local file.
    """
    action = parameters.get("action", "add").strip()
    reminder_text = parameters.get("reminder", "").strip()

    storage_dir = get_base_dir() / "storage"
    storage_dir.mkdir(parents=True, exist_ok=True)
    file_path = storage_dir / "reminders.json"

    if player:
        player.write_log(f"📝 Reminder Manager: {action}")

    reminders = []
    if file_path.exists():
        try:
            reminders = json.loads(file_path.read_text())
        except Exception:
            pass

    if action == "add":
        if not reminder_text:
            return "Error: Provide a reminder text."
        reminders.append(reminder_text)
        file_path.write_text(json.dumps(reminders, indent=2))
        return f"✅ Added reminder: {reminder_text}"
    elif action == "list":
        if not reminders:
            return "No reminders."
        return "Reminders:\n" + "\n".join([f"{i+1}. {r}" for i, r in enumerate(reminders)])
    elif action == "clear":
        file_path.write_text("[]")
        return "✅ Cleared all reminders."
    else:
        return f"Unknown action: {action}"
