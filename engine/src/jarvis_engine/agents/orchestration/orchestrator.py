from jarvis_engine.agents.orchestration.prompt_builder import build_system_prompt
from jarvis_engine.domains.tools.registry import registry
from jarvis_engine.domains.llm.router import router
from jarvis_engine.agents.execution.executor import _call_tool

class Orchestrator:
    def __init__(self, max_iterations: int = 5):
        self.max_iterations = max_iterations

    def run(self, user_message: str, session_memory=None, context: str = "", speak=None) -> str:
        """
        Runs the agent loop.
        """
        messages = session_memory.get_messages() if session_memory else []
        
        # Add the new user message
        messages.append({"role": "user", "content": user_message})
        if session_memory:
            session_memory.add_user_message(user_message)
            
        memory_snippets = session_memory.get_snippets() if session_memory else ""
        
        schemas = registry.get_all_tool_schemas()
        
        iterations = 0
        while iterations < self.max_iterations:
            # 1. Build prompt
            prompt = build_system_prompt(
                context_str=context,
                memory_snippets=memory_snippets,
            )
            
            # 2. Call LLM
            print(f"[Orchestrator] Thinking (Iteration {iterations+1}/{self.max_iterations})...")
            response = router.generate(
                system_prompt=prompt,
                messages=messages,
                tools=schemas
            )
            
            # Extract tool calls and text
            tool_calls = []
            text_response = ""
            
            # Gemini response object parsing
            if hasattr(response, 'candidates') and response.candidates:
                part = response.candidates[0].content.parts[0]
                if hasattr(part, 'function_call') and part.function_call:
                    for p in response.candidates[0].content.parts:
                        if hasattr(p, 'function_call') and p.function_call:
                            # Extract arguments from the protobuf Struct
                            args_dict = {}
                            if hasattr(p.function_call, 'args'):
                                for k, v in p.function_call.args.items():
                                    args_dict[k] = v
                            tool_calls.append({
                                "name": p.function_call.name,
                                "args": args_dict
                            })
                elif hasattr(part, 'text') and part.text:
                    text_response = part.text
            else:
                # If unexpected structure
                text_response = "I couldn't formulate a response."

            # 3. Process Tool Calls or text
            if tool_calls:
                # Add assistant message with tool calls to history
                assistant_msg = {"role": "assistant", "tool_calls": tool_calls}
                messages.append(assistant_msg)
                if session_memory:
                    session_memory.add_assistant_message(tool_calls=tool_calls)
                    
                for tc in tool_calls:
                    name = tc["name"]
                    args = tc["args"]
                    print(f"[Orchestrator] Executing tool: {name}")
                    
                    try:
                        result = _call_tool(name, args, speak=speak)
                    except Exception as e:
                        result = f"Error executing {name}: {str(e)}"
                        
                    print(f"[Orchestrator] Tool Result: {str(result)[:80]}")
                    
                    tool_msg = {"role": "tool", "tool_name": name, "content": str(result)}
                    messages.append(tool_msg)
                    if session_memory:
                        session_memory.add_tool_result(name, str(result))
                        
                iterations += 1
            elif text_response:
                # 4. Final Text Answer
                messages.append({"role": "assistant", "content": text_response})
                if session_memory:
                    session_memory.add_assistant_message(content=text_response)
                return text_response
            else:
                return "No response generated."
                
        # If we hit max iterations
        error_msg = f"Task aborted: exceeded maximum iterations ({self.max_iterations})."
        messages.append({"role": "assistant", "content": error_msg})
        if session_memory:
            session_memory.add_assistant_message(content=error_msg)
        return error_msg

orchestrator = Orchestrator()
