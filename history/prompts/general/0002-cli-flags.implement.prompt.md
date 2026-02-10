---
id: "0002"
title: "Implement CLI flags for priority and filters"
stage: "implement"
date: "2026-01-02"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-core-essentials"
user: "anas0"
command: "Implement CLI flags for priority and filters"
labels: ["cli","flags","priority","filter"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "src/cli/main.py"
  - "src/core/storage.py"
  - "tests/unit/test_service.py"
tests:
  - "tests/unit/test_service.py::test_add_task"
  - "tests/unit/test_service.py::test_add_empty_task"
  - "tests/unit/test_service.py::test_get_all_tasks"
  - "tests/unit/test_service.py::test_update_task_status"
  - "tests/unit/test_service.py::test_delete_task"
  - "tests/unit/test_service.py::test_delete_non_existent_task"
---

## Prompt

Implement CLI flags for priority and filters

## Response snapshot

Implemented CLI flags for the todo CLI:

1. **add command**: Added `--priority` flag with choices [LOW, MEDIUM, HIGH], defaulting to MEDIUM
2. **list command**: Added `--status` filter (pending/completed), `--priority` filter (LOW/MEDIUM/HIGH), and `--sort` option (id/priority/status)
3. **Fixed storage.py**: Priority was being loaded as a string instead of TaskPriority enum, causing AttributeError
4. **Fixed tests**: Updated tests to use temporary storage files to avoid state pollution

All 6 tests pass after fixes.

## Outcome

- ✅ Impact: CLI now supports priority flags on add, filtering and sorting on list
- 🧪 Tests: 6 passed
- 📁 Files: 3 modified
- 🔁 Next prompts: Continue with Phase 3 user stories
- 🧠 Reflection: Storage layer needed enum conversion fix when loading from JSON

## Evaluation notes (flywheel)

- Failure modes observed: Priority enum not properly converted when loading from JSON storage
- Graders run and results (PASS/FAIL): All 6 tests PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add integration tests for the new CLI flags
