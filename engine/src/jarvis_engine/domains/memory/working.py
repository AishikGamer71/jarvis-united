class WorkingMemory:
    def __init__(self):
        # We just store a rolling list of messages for the session
        # e.g. [{"role": "user", "content": "..."}, {"role": "assistant", "tool_calls": [...]}, ...]
        self.messages = []
        
        # We can also store volatile snippets (e.g., active files, short-term facts)
        self.snippets = []

    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str = None, tool_calls: list = None):
        msg = {"role": "assistant"}
        if content:
            msg["content"] = content
        if tool_calls:
            msg["tool_calls"] = tool_calls
        self.messages.append(msg)

    def add_tool_result(self, tool_name: str, content: str):
        self.messages.append({"role": "tool", "tool_name": tool_name, "content": content})

    def get_messages(self) -> list:
        # Return a copy to prevent accidental mutation by the router
        import copy
        return copy.deepcopy(self.messages)

    def get_snippets(self) -> str:
        return "\n".join(self.snippets)
        
    def add_snippet(self, snippet: str):
        if snippet not in self.snippets:
            self.snippets.append(snippet)
