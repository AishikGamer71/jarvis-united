# JARVIS Unified Monorepo

Welcome to the JARVIS Unified Monorepo. This repository houses both the frontend desktop application and the backend AI control engine in a scalable, Turborepo-managed workspace.

## Monorepo Layout

The repository is organized as follows:

- **`apps/desktop/`**: The frontend Electron/Vite React application.
- **`engine/src/jarvis_engine/`**: The core Python AI and control engine.
- **`packages/ipc-contracts/`**: Shared TypeScript types establishing the inter-process communication (IPC) bridge.
- **`infra/`**: Infrastructure configurations, such as Docker Compose setups.
- **`docs/`**: Project documentation and architecture decision records (ADRs).

## Architecture: The IPC Bridge

The desktop app and the Python engine operate in tandem. They communicate seamlessly via an Inter-Process Communication (IPC) bridge:
- The React application (`apps/desktop`) uses explicitly defined contracts in `packages/ipc-contracts`.
- The frontend invokes tasks and sends queries via the bridging layer.
- The backend (`engine/`) processes AI commands, system automation, and web scraping, returning results over the shared communication interface.

## Quick Start

### Prerequisites
- Node.js & `pnpm`
- Python 3.10+
- `make` (optional but recommended on Unix systems)

### Installation
From the root directory, run:
```bash
make install
```
*(This runs `pnpm install` at the root and `pip install -e .` inside the `engine` directory.)*

### Running the App
To start the development servers for the frontend:
```bash
make dev
```
*(This invokes `pnpm turbo run dev` across the workspace.)*

To start the Python engine:
```bash
cd engine
python -m jarvis_engine.main
```

## Known Gaps
- **Scaffolded Modules**: `engine/src/jarvis_engine/agents/orchestration/`, `domains/`, and `infra/` have been architecturally scaffolded per ADR 0002/0003, but they are not yet fully wired into the live `main.py` execution path. Future work will route execution through this hexagonal architecture.
