import os
import sys
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Add vendor to path to import hermes_agent
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "vendor", "hermes-agent"))

from agent.transports.base import ProviderTransport
from run_agent import AIAgent
from hermes_state import HermesState
from domain.transports.gemini_transport import GeminiTransport

app = FastAPI(title="JARVIS Agent Core", description="Hermes Agent wrapped as FastAPI")

# Note: Ideally we load settings and initialize AIAgent, 
# for now we provide a minimal /v1/chat/completions interface

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: Optional[bool] = False

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    # Dummy mock for now, to ensure the UI adapter has a valid endpoint
    # In a real implementation we would route the request through `AIAgent` loop.
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": request.model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hello! I am JARVIS, powered by Hermes Agent.",
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 9,
            "completion_tokens": 12,
            "total_tokens": 21
        }
    }

@app.get("/v1/memory")
async def get_memory():
    return {"status": "memory stub"}

@app.get("/v1/skills")
async def get_skills():
    return {"status": "skills stub"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8420)
