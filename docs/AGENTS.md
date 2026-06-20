# JARVIS Multi-Agent System

## Agent Hierarchy

1. **Orchestrator**: The main entry point. Decides which specialist to invoke based on user intent.
2. **Supervisor**: Monitors execution, handles error loops, and ensures tasks align with the initial goal.

## Specialists

- **DevAgent**: Writes, refactors, and debugs code.
- **ResearchAgent**: Scrapes the web, reads docs, and synthesizes answers.
- **SystemAgent**: Interacts with the local OS (files, apps, settings).
- **CreativeAgent**: Handles content generation, writing, and brainstorming.
- **DataAgent**: Analyzes data, executes SQL, and generates charts.
