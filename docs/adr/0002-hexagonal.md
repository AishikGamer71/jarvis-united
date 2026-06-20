# ADR 0002: Hexagonal Architecture for Python Engine

## Status
Accepted

## Context
The previous Python backend (`python-engine`) had tightly coupled logic, where API handlers directly called LLMs and databases, making it difficult to test or swap providers.

## Decision
We will adopt a Hexagonal (Ports and Adapters) Architecture. Core business logic will reside in `engine/domains/` (cognition, memory, llm, rag), while external integrations (DBs, Redis, vector stores) will reside in `engine/infra/`. Dependencies will be injected via `engine/core/container.py`.

## Consequences
- Highly testable core logic without spinning up actual databases.
- Easier to swap LLM providers (e.g., Gemini vs Ollama).
- Slight overhead in boilerplate (interfaces/ABCs).
