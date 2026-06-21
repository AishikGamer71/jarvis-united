import json
from pathlib import Path
import google.generativeai as genai
from google.generativeai.types import content_types

def _get_api_key() -> str:
    import sys
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).parent
    else:
        # e:\Projects\ui test\jarvis-unified - Copy\engine\src\jarvis_engine\domains\llm\router.py
        # -> llm -> domains -> jarvis_engine
        base = Path(__file__).resolve().parent.parent.parent
    config_path = base / "config" / "api_keys.json"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f).get("gemini_api_key", "")
    except Exception:
        return ""

class LLMRouter:
    def __init__(self):
        self.api_key = _get_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
            
    def generate(self, system_prompt: str, messages: list, tools: list = None) -> object:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_prompt,
            tools=[{"function_declarations": tools}] if tools else None
        )
        
        history = []
        for msg in messages:
            if msg["role"] == "user":
                history.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                if "tool_calls" in msg:
                    parts = []
                    for tc in msg["tool_calls"]:
                        parts.append({
                            "function_call": {
                                "name": tc["name"],
                                "args": tc["args"]
                            }
                        })
                    history.append({"role": "model", "parts": parts})
                else:
                    history.append({"role": "model", "parts": [msg["content"]]})
            elif msg["role"] == "tool":
                history.append({
                    "role": "function",
                    "parts": [{
                        "function_response": {
                            "name": msg["tool_name"],
                            "response": {"result": msg["content"]}
                        }
                    }]
                })
                
        if history and history[-1]["role"] == "user":
            prompt = history.pop()
            chat = model.start_chat(history=history)
            return chat.send_message(prompt["parts"][0])
        else:
            chat = model.start_chat(history=history)
            return chat.send_message("Continue.")

router = LLMRouter()
