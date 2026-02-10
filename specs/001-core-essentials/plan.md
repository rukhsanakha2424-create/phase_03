# Implementation Plan: 001-core-essentials

**Branch**: `001-core-essentials` | **Date**: 2026-01-01 | **Spec**: [specs/001-core-essentials/spec.md](specs/001-core-essentials/spec.md)

## Summary

Build the core foundation for the Evolution of Todo app. This phase implements a Python-based CLI that allows users to manage tasks (CRUD operations) using in-memory storage. The focus is on clean architecture, deterministic unique IDs, and clear command-line feedback.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `argparse` (Standard Library) for CLI, `pytest` for testing.
**Storage**: In-memory (Dictionary/List-based storage service).
**Testing**: `pytest` (unit and integration tests).
**Target Platform**: Cross-platform (Linux/macOS/Windows) via terminal.
**Project Type**: Single project CLI application.
**Performance Goals**: Sub-10ms response time for all local operations.
**Constraints**: No persistent storage in this phase; data lost on exit.
**Scale/Scope**: Support for 1,000+ active tasks in memory.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Tech Stack: Python CLI only (Phase 1-3).
- [x] Development Style: Spec-Driven Development (SDD).
- [x] No manual code edits (all via Claude Code).
- [x] Smallest viable diff: One feature = one spec file.

## Project Structure

### Documentation (this feature)

```text
specs/001-core-essentials/
├── plan.md              # This file
├── research.md          # Technology choices and rationale
├── data-model.md        # Entity definitions and validation rules
├── quickstart.md        # Setup and usage for this phase
├── contracts/           # API/Command schemas
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
src/
├── core/
│   ├── models.py        # Task entity
│   └── service.py       # Task management logic (In-memory)
├── cli/
│   └── main.py          # Argparse entry point
└── utils/
    └── id_gen.py        # Deterministic ID generation

tests/
├── unit/                # Testing core logic
└── integration/         # Testing CLI commands
```

**Structure Decision**: Single project structure follows the constitution's "no overengineering" principle. Logic is separated into `core` and `cli` to facilitate future persistence (Phase 4).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
