from typing import Dict, Any, Type, TypeVar

T = TypeVar('T')

class Container:
    """Dependency Injection Registry."""
    def __init__(self):
        self._providers: Dict[Type, Any] = {}
        self._instances: Dict[Type, Any] = {}

    def register(self, interface: Type[T], provider: Any) -> None:
        self._providers[interface] = provider

    def resolve(self, interface: Type[T]) -> T:
        if interface in self._instances:
            return self._instances[interface]
            
        provider = self._providers.get(interface)
        if not provider:
            raise ValueError(f"No provider registered for {interface}")
            
        instance = provider() if callable(provider) else provider
        self._instances[interface] = instance
        return instance

# Global container instance
container = Container()
