# ADR 0001: Monorepo Architecture

## Status
Accepted

## Context
JARVIS consisted of multiple detached codebases (frontend, backend, shared utilities). This caused version mismatches, duplicated IPC types, and difficult CI/CD pipelines.

## Decision
We will adopt a monorepo architecture using `pnpm` workspaces and `turbo` for build caching. The structure will separate applications (`apps/`) from shared libraries (`packages/`).

## Consequences
- Single source of truth for IPC types (now in `packages/ipc-contracts`).
- Easier to run integration tests across the entire stack.
- Requires learning new tooling (`turborepo`, `pnpm` workspaces).
