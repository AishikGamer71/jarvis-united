import asyncio
from typing import Callable, Dict, List, Any

class EventBus:
    """Async Event Bus for inter-component communication."""
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(handler)

    async def publish(self, event_type: str, payload: Any = None) -> None:
        handlers = self._subscribers.get(event_type, [])
        tasks = [handler(payload) for handler in handlers]
        if tasks:
            await asyncio.gather(*tasks)

# Global event bus instance
bus = EventBus()
