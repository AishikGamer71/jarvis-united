import os
import sys
import psutil

def task_manager(parameters: dict, player=None):
    """
    Lists or kills OS processes.
    """
    action = parameters.get("action", "list").strip()
    process_name = parameters.get("name", "").strip()

    if player:
        player.write_log(f"🖥️ OS Task Manager: {action}")

    if action == "list":
        procs = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                # Basic filter to avoid listing hundreds of minor processes
                if proc.info['cpu_percent'] > 1.0 or proc.info['memory_info'].rss > 50 * 1024 * 1024:
                    procs.append(f"PID: {proc.info['pid']} | {proc.info['name']} | CPU: {proc.info['cpu_percent']}%")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        procs = procs[:20]  # Return top 20
        return "Top Processes:\n" + "\n".join(procs)
    
    elif action == "kill":
        if not process_name:
            return "Error: Provide a process name to kill."
        killed = 0
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                try:
                    proc.kill()
                    killed += 1
                except psutil.AccessDenied:
                    return f"Error: Access denied to kill {proc.info['name']}."
        return f"✅ Killed {killed} process(es) matching '{process_name}'."
    else:
        return f"Unknown action: {action}"
