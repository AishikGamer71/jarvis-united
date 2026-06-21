import json

def terminal_execute(parameters=None, response=None, player=None, session_memory=None):
    """
    Executes a command directly in the user's Live Terminal (PTY).
    """
    command = (parameters or {}).get("command", "").strip()

    if not command:
        return "Please specify a command to execute, sir."

    print(f"[terminal_execute] 🚀 Sending to UI Terminal: {command}")
    
    if player:
        player.write_log(f"[Terminal] {command}")
        # Send a special WebSocket broadcast to the React frontend
        player.broadcast(json.dumps({
            "type": "terminal_execute",
            "value": command + "\r"
        }))

    return f"I have executed '{command}' in the terminal, sir."
