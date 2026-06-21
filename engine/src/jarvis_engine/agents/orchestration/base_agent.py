from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """Abstract Base Class for all JARVIS agents."""
    
    @abstractmethod
    async def perceive(self, context: Dict[str, Any]) -> Any:
        pass
        
    @abstractmethod
    async def plan(self, observation: Any) -> Any:
        pass
        
    @abstractmethod
    async def act(self, plan: Any) -> Any:
        pass
        
    @abstractmethod
    async def reflect(self, result: Any) -> Any:
        pass
