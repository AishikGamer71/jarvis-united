# ADR 0003: Multi-Agent System

## Status
Accepted

## Context
A single monolith agent handling coding, research, scheduling, and system operations became too complex, leading to prompt bloat and unpredictable behaviors.

## Decision
We will implement a Multi-Agent System (MAS). A `Supervisor` or `Orchestrator` will delegate tasks to specialized agents (e.g., `DevAgent`, `ResearchAgent`, `SystemAgent`). All agents will inherit from `BaseAgent` and implement a strict Perceive -> Plan -> Act -> Reflect cycle.

## Consequences
- Modularity: Each agent has a focused system prompt.
- Better error recovery through reflection.
- Increased token usage due to inter-agent communication and orchestration overhead.
