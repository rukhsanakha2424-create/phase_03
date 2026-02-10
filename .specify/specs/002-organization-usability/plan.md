# Implementation Plan: 002-organization-usability

**Branch**: `002-organization-usability` | **Date**: 2026-01-02 | **Spec**: `specs/002-organization-usability/spec.md`

## Summary

Phase 2 extends the core todo app with data persistence (JSON file storage), priority levels (LOW/MEDIUM/HIGH), and advanced CLI capabilities for searching, filtering, and sorting tasks. This transforms the app from a session-based tool to a persistent, organized task management system.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `json` (Standard Library), existing Phase 1 modules
**Storage**: JSON file persistence (`data/todos.json`)
**Testing**: `pytest` (extend Phase 1 tests)
**Target Platform**: Cross-platform terminal
**Project Type**: Single project CLI (extending Phase 1)
**Performance Goals**: <50ms load/save for up to 1,000 tasks
**Constraints**: Backward compatible with Phase 1 data model; file-based persistence only
**Scale/Scope**: Support for 1,000+ tasks with search/filter performance

## Constitution Check

*GATE: Must pass before implementation*

- [x] Tech Stack: Python (consistent with Phase 1)
- [x] Development Style: Spec-Driven Development
- [x] No manual code edits (all via Claude Code)
- [x] Smallest viable diff: Phase 2 builds on Phase 1

## Project Structure

### Documentation (this feature)

```text
.specify/specs/002-organization-usability/
├── plan.md              # This file
├── research.md          # JSON persistence patterns
├── data-model.md        # Updated Task entity with priority
├── quickstart.md        # Updated setup for Phase 2
├── contracts/           # CLI command schemas
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
src/
├── core/
│   ├── models.py        # Updated: Task priority enum
│   ├── service.py       # Updated: Persistence layer
│   └── storage.py       # NEW: JSON file I/O
├── cli/
│   └── main.py          # Updated: Filter/sort/search commands
└── utils/
    └── id_gen.py        # Unchanged from Phase 1

data/                    # NEW: Persistence directory
└── todos.json           # Task storage file

tests/
├── unit/                # Extended tests
└── integration/         # Extended tests
```

**Structure Decision**: Single project structure maintained. New `storage.py` module for persistence logic. `data/` directory for JSON file.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| JSON over DB | Phase 4 scope | Simpler than SQLite, sufficient for CLI |
