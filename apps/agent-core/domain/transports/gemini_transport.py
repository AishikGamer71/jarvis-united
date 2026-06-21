import json
from typing import Any, Dict, List, Optional
from agent.transports.base import ProviderTransport
from agent.transports.types import NormalizedResponse, Usage, build_tool_call, map_finish_reason

class GeminiTransport(ProviderTransport):
    """Gemini Provider Transport implementing the Hermes Agent ProviderTransport ABC."""

    @property
    def api_mode(self) -> str:
        return "gemini_messages"

    def convert_messages(self, messages: List[Dict[str, Any]], **kwargs) -> Any:
        # Convert OpenAI format to Gemini format
        gemini_msgs = []
        system_instructions = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content", "")
            if role == "system":
                system_instructions.append(content)
            elif role == "user":
                gemini_msgs.append({"role": "user", "parts": [{"text": content}]})
            elif role == "assistant":
                parts = []
                if content:
                    parts.append({"text": content})
                if "tool_calls" in msg:
                    for tc in msg["tool_calls"]:
                        func = tc.get("function", {})
                        parts.append({
                            "functionCall": {
                                "name": func.get("name"),
                                "args": json.loads(func.get("arguments", "{}"))
                            }
                        })
                gemini_msgs.append({"role": "model", "parts": parts})
            elif role == "tool":
                gemini_msgs.append({
                    "role": "user",
                    "parts": [{
                        "functionResponse": {
                            "name": msg.get("name"),
                            "response": {"result": content}
                        }
                    }]
                })
        return system_instructions, gemini_msgs

    def convert_tools(self, tools: List[Dict[str, Any]]) -> Any:
        # Convert OpenAI tools to Gemini Tools
        gemini_tools = []
        for t in tools:
            func = t.get("function", {})
            gemini_tools.append({
                "name": func.get("name"),
                "description": func.get("description", ""),
                "parameters": func.get("parameters", {})
            })
        if not gemini_tools:
            return None
        return [{"functionDeclarations": gemini_tools}]

    def build_kwargs(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **params,
    ) -> Dict[str, Any]:
        system_instructions, gemini_msgs = self.convert_messages(messages)
        kwargs = {
            "model": model,
            "contents": gemini_msgs,
        }
        if system_instructions:
            kwargs["systemInstruction"] = {"parts": [{"text": "\n".join(system_instructions)}]}
        if tools:
            gemini_tools = self.convert_tools(tools)
            if gemini_tools:
                kwargs["tools"] = gemini_tools
        # add other parameters like temperature
        if "temperature" in params:
            kwargs.setdefault("generationConfig", {})["temperature"] = params["temperature"]
        return kwargs

    def normalize_response(self, response: Any, **kwargs) -> NormalizedResponse:
        # response is assumed to be a dictionary returned by the Gemini REST API or SDK
        # Example format: {"candidates": [{"content": {"parts": [{"text": "..."}, {"functionCall": {...}}]}, "finishReason": "STOP"}], "usageMetadata": {...}}
        if hasattr(response, "candidates"):
            # SDK response object wrapping
            candidate = response.candidates[0]
            parts = getattr(candidate.content, "parts", [])
            finish_reason = getattr(candidate, "finish_reason", "STOP")
            # Need to properly extract text and tool_calls
            content_text = ""
            tool_calls = []
            for part in parts:
                if hasattr(part, "text"):
                    content_text += part.text
                if hasattr(part, "function_call"):
                    fc = part.function_call
                    args_dict = dict(fc.args) if hasattr(fc, "args") else {}
                    tool_calls.append(build_tool_call(id=None, name=fc.name, arguments=args_dict))
            
            usage = None
            if hasattr(response, "usage_metadata"):
                um = response.usage_metadata
                usage = Usage(
                    prompt_tokens=getattr(um, "prompt_token_count", 0),
                    completion_tokens=getattr(um, "candidates_token_count", 0),
                    total_tokens=getattr(um, "total_token_count", 0)
                )
        else:
            # REST dictionary format
            candidate = response.get("candidates", [{}])[0]
            parts = candidate.get("content", {}).get("parts", [])
            finish_reason = candidate.get("finishReason", "STOP")
            
            content_text = ""
            tool_calls = []
            for part in parts:
                if "text" in part:
                    content_text += part["text"]
                if "functionCall" in part:
                    fc = part["functionCall"]
                    tool_calls.append(build_tool_call(id=None, name=fc.get("name"), arguments=fc.get("args", {})))
            
            usage = None
            um = response.get("usageMetadata")
            if um:
                usage = Usage(
                    prompt_tokens=um.get("promptTokenCount", 0),
                    completion_tokens=um.get("candidatesTokenCount", 0),
                    total_tokens=um.get("totalTokenCount", 0)
                )

        if isinstance(finish_reason, int) or str(finish_reason).upper() == "STOP":
            normalized_reason = "stop"
        elif str(finish_reason).upper() == "MAX_TOKENS":
            normalized_reason = "length"
        else:
            normalized_reason = "stop"
        if tool_calls:
            normalized_reason = "tool_calls"
            
        return NormalizedResponse(
            content=content_text if content_text else None,
            tool_calls=tool_calls if tool_calls else None,
            finish_reason=normalized_reason,
            usage=usage
        )
