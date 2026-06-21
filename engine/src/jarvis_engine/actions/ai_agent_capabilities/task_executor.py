import json
import sys
import uuid
import time
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
        raise ValueError("Gemini API key not found in config/api_keys.json")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def task_executor(parameters: dict, player=None):
    """
    Orchestrates complex goals by breaking them down into actionable sub-tasks and saving an execution plan.
    """
    goal = parameters.get("goal", "").strip()
    if not goal:
        return "Error: Please specify a goal for the task executor."

    if player:
        player.write_log(f"🤖 Orchestrating tasks for: '{goal}'...")

    prompt = f"""You are an advanced AI Orchestrator Agent. 
Your objective is to break down the following high-level user goal into a strict, logical sequence of step-by-step subtasks that an AI agent or automated system must follow to achieve the goal.

Goal: {goal}

Format your response strictly as a JSON list of task strings. Do not include markdown formatting or backticks around the JSON.
Example format:
[
  "Research the necessary APIs and dependencies",
  "Initialize the project directory structure",
  "Write the core logic module",
  "Write unit tests",
  "Deploy the application"
]
"""

    try:
        model = _get_gemini()
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        
        # Clean up possible markdown
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        tasks = json.loads(raw_text.strip())
        
        # Save orchestration plan to storage
        storage_dir = get_base_dir() / "storage"
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        plan_id = f"plan_{uuid.uuid4().hex[:6]}"
        plan_file = storage_dir / f"{plan_id}.json"
        
        plan_data = {
            "goal": goal,
            "status": "pending",
            "created_at": time.time(),
            "tasks": [{"id": i+1, "task": t, "status": "pending"} for i, t in enumerate(tasks)]
        }
        
        with open(plan_file, "w", encoding="utf-8") as f:
            json.dump(plan_data, f, indent=4)
            
        output = f"✅ Orchestration Plan Generated for: '{goal}'\n\n"
        for i, t in enumerate(tasks, 1):
            output += f"{i}. {t}\n"
            
        output += f"\nPlan saved to: {plan_file}"
        return output

    except Exception as e:
        return f"Task Orchestrator failed: {str(e)}"
