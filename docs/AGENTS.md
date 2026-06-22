# JARVIS Agent Architecture

## Agent Loop
The core of JARVIS is a multi-step agent loop orchestrated in `agents/orchestration/orchestrator.py`. 
When a user prompt enters `main.py`, it is passed to the Orchestrator, which loops over the following steps (capped at 5 iterations):
1. **Prompt Build**: Generates the context using `prompt_builder.py`.
2. **LLM Query**: Consults the LLM via `domains/llm/router.py`.
3. **Dispatch**: If the LLM generates a tool call, `agents/execution/executor.py` dispatches it to the relevant action tool.
4. **Observation**: Results are returned back to the LLM to decide on the next step or conclude.

## Memory Layer
The conversation history and volatile state are maintained via `domains/memory/working.py`. This ensures context is retained across iterative tool calls within a single user request.

## Execution
`agents/execution/executor.py` handles the physical dispatching of tools and routes them to the actual implementations under `actions/`.
