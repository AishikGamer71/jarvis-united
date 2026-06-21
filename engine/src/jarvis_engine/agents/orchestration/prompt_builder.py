import datetime
from pathlib import Path

def _get_base_dir() -> Path:
    import sys
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent.parent


def get_stable_prompt() -> str:
    """Returns the static JARVIS identity and persona rules."""
    prompt_path = _get_base_dir() / "core" / "prompt.txt"
    try:
        persona = prompt_path.read_text(encoding="utf-8")
    except Exception:
        persona = (
            "You are JARVIS, Tony Stark's AI assistant.\n"
            "Be concise, direct, and always use the provided tools to complete tasks.\n"
            "Never simulate or guess results — always call the appropriate tool."
        )
    return f"=== SYSTEM PERSONA ===\n{persona}\n"


def get_context_tier(context: str = "") -> str:
    """Returns the current loaded files or project context."""
    if not context:
        return ""
    return f"\n=== CURRENT CONTEXT ===\n{context}\n"


def get_volatile_tier(memory_snippets: str = "") -> str:
    """Returns dynamic, volatile context like timestamps and active memory."""
    now = datetime.datetime.now()
    time_str = now.strftime("%A, %B %d, %Y — %I:%M %p")
    time_ctx = (
        f"\n=== VOLATILE CONTEXT ===\n"
        f"[CURRENT DATE & TIME]\n"
        f"Right now it is: {time_str}\n"
        f"Use this to calculate exact times for reminders and references.\n"
    )
    if memory_snippets:
        time_ctx += f"\n[ACTIVE MEMORY]\n{memory_snippets}\n"
    return time_ctx


def build_system_prompt(
    context_str: str = "",
    memory_snippets: str = "",
    tool_schemas: list = None
) -> str:
    """
    Assembles the tiered system prompt.
    If 'tool_schemas' are provided, they can be formatted here,
    though modern APIs usually pass them as a separate JSON payload.
    We return the composed text prompt.
    """
    parts = [
        get_stable_prompt(),
        get_context_tier(context_str),
        get_volatile_tier(memory_snippets)
    ]
    
    # If the LLM requires tools inside the text prompt, we can inject them.
    # Otherwise, they are just passed to the provider config.
    if tool_schemas:
        tools_str = "\n".join(f"- {s['name']}: {s['description']}" for s in tool_schemas)
        parts.append(f"\n=== AVAILABLE TOOLS ===\n{tools_str}\n")
        parts.append(
            "\nYou have tools available to accomplish tasks. "
            "Please call the appropriate tool if you need information, want to take an action, or manage files."
        )

    return "".join(parts).strip()
