import sys
from pathlib import Path

def alarm_manager(parameters: dict, player=None):
    """
    Manages local alarms.
    """
    action = parameters.get("action", "set").strip()
    time = parameters.get("time", "").strip()
    message = parameters.get("message", "Alarm!").strip()

    if player:
        player.write_log(f"⏰ Alarm Manager: {action} {time}")

    # Very simplified implementation
    if action == "set":
        return f"✅ Alarm set for {time} with message: {message}"
    elif action == "list":
        return "No active alarms."
    else:
        return f"Unknown alarm action: {action}"
