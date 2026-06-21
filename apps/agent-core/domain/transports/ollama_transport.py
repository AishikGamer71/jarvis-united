import json
from typing import Any, Dict, List, Optional
from agent.transports.base import ProviderTransport
from agent.transports.types import NormalizedResponse, Usage, build_tool_call, map_finish_reason

class OllamaTransport(ProviderTransport):
    """Ollama/llama.cpp Provider Transport implementing the ProviderTransport ABC."""

    @property
    def api_mode(self) -> str:
        return "ollama_chat"

    def convert_messages(self, messages: List[Dict[str, Any]], **kwargs) -> Any:
        # Ollama supports OpenAI style messages natively
        return messages

    def convert_tools(self, tools: List[Dict[str, Any]]) -> Any:
        # Ollama supports OpenAI style tools
        return tools

    def build_kwargs(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **params,
    ) -> Dict[str, Any]:
        kwargs = {
            "model": model,
            "messages": self.convert_messages(messages),
        }
        if tools:
            kwargs["tools"] = self.convert_tools(tools)
        if "temperature" in params:
            kwargs["temperature"] = params["temperature"]
        return kwargs

    def normalize_response(self, response: Any, **kwargs) -> NormalizedResponse:
        # response is assumed to be OpenAI-like JSON or object
        if hasattr(response, "choices"):
            choice = response.choices[0]
            message = choice.message
            content = getattr(message, "content", None)
            tool_calls_raw = getattr(message, "tool_calls", None)
            finish_reason = getattr(choice, "finish_reason", "stop")
            
            tool_calls = []
            if tool_calls_raw:
                for tc in tool_calls_raw:
                    func = tc.function
                    args_dict = json.loads(func.arguments) if isinstance(func.arguments, str) else func.arguments
                    tool_calls.append(build_tool_call(id=tc.id, name=func.name, arguments=args_dict))
                    
            usage = None
            if hasattr(response, "usage"):
                usage_obj = response.usage
                usage = Usage(
                    prompt_tokens=getattr(usage_obj, "prompt_tokens", 0),
                    completion_tokens=getattr(usage_obj, "completion_tokens", 0),
                    total_tokens=getattr(usage_obj, "total_tokens", 0)
                )
        else:
            choice = response.get("choices", [{}])[0]
            message = choice.get("message", {})
            content = message.get("content")
            tool_calls_raw = message.get("tool_calls")
            finish_reason = choice.get("finish_reason", "stop")
            
            tool_calls = []
            if tool_calls_raw:
                for tc in tool_calls_raw:
                    func = tc.get("function", {})
                    args = func.get("arguments", "{}")
                    args_dict = json.loads(args) if isinstance(args, str) else args
                    tool_calls.append(build_tool_call(id=tc.get("id"), name=func.get("name"), arguments=args_dict))
                    
            usage = None
            usage_dict = response.get("usage")
            if usage_dict:
                usage = Usage(
                    prompt_tokens=usage_dict.get("prompt_tokens", 0),
                    completion_tokens=usage_dict.get("completion_tokens", 0),
                    total_tokens=usage_dict.get("total_tokens", 0)
                )

        if tool_calls:
            normalized_reason = "tool_calls"
        else:
            normalized_reason = map_finish_reason(finish_reason, {"stop": "stop", "length": "length"})

        return NormalizedResponse(
            content=content,
            tool_calls=tool_calls if tool_calls else None,
            finish_reason=normalized_reason,
            usage=usage
        )
