# Research Findings: Todo In-Memory Python Console App

**Branch**: `001-todo-in-memory` | **Date**: 2026-01-03
**Purpose**: Resolve technical unknowns and establish best practices for Phase I implementation

## Research Summary

This document consolidates research findings for building a Python CLI todo application. All decisions align with Phase I constraints: in-memory storage, argparse subcommands, pytest testing, and clean architecture.

---

## Decision 1: Argparse Subcommand Architecture

**Decision**: Use argparse subparsers with a main subparser for command routing.

**Rationale**:
- Subparsers provide built-in help, error handling, and command routing
- Each subcommand can have its own arguments (e.g., `add` takes description, `delete` takes ID)
- Standard library - no external dependencies
- Matches constitution requirement for deterministic CLI behavior

**Implementation Pattern**:
```python
parser = argparse.ArgumentParser(description="Todo CLI Application")
subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

add_parser = subparsers.add_parser("add", help="Add a new task")
add_parser.add_argument("description", help="Task description")

list_parser = subparsers.add_parser("list", help="List all tasks")

delete_parser = subparsers.add_parser("delete", help="Delete a task")
delete_parser.add_argument("id", type=int, help="Task ID")

# Additional subparsers: update, complete
```

**Alternatives Considered**:
- `click` or `typer` libraries: Rejected because they add dependencies; argparse is sufficient
- Manual command parsing: Rejected due to poor error handling and help generation
- Interactive REPL: Rejected per constitution (§3.1) - stateless per invocation required

---

## Decision 2: In-Memory Storage Model

**Decision**: Use a Python list of dataclass instances for task storage.

**Rationale**:
- Simple, readable, and type-safe with dataclasses
- List preserves insertion order (sequential IDs align naturally)
- No serialization overhead required for in-memory use
- Easy to clear/reset on application restart (FR-008, FR-009)

**Implementation Pattern**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    description: str
    complete: bool = False

class TodoManager:
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1
```

**Alternatives Considered**:
- Dictionary mapping IDs to tasks: Rejected because list is simpler and sequential IDs don't need lookup optimization
- Global module-level list: Rejected because class-based approach enables better testing and isolation
- SQLite in-memory database: Rejected as overkill; violates constitution principle of simplicity

---

## Decision 3: Task ID Generation Strategy

**Decision**: Sequential integers starting from 1, assigned incrementally.

**Rationale**:
- Spec requirement (Assumptions section)
- Simple and predictable for users
- Aligns with list-based storage
- No gaps in IDs during session (IDs are never reused)

**Implementation**:
```python
def add_task(self, description: str) -> Task:
    task = Task(id=self._next_id, description=description)
    self._tasks.append(task)
    self._next_id += 1
    return task
```

**Alternatives Considered**:
- UUIDs: Rejected as over-engineering for Phase I
- Hash of description: Rejected due to collision risk
- Timestamps: Rejected as user-unfriendly and non-sequential

---

## Decision 4: Input Validation Strategy

**Decision**: Validate inputs at CLI layer using argparse, with additional validation in core layer for business rules.

**Rationale**:
- Argparse handles type conversion and basic validation (e.g., integer IDs)
- Business logic validation (ID existence) lives in core layer for testability
- Clear error messages satisfy constitution requirement (Principle 2)

**Implementation Pattern**:
```python
# CLI layer (argparse)
delete_parser.add_argument("id", type=int, help="Task ID")

# Core layer (business validation)
def delete_task(self, task_id: int) -> Task:
    task = self._find_task(task_id)
    if task is None:
        raise ValueError(f"Task with ID {task_id} not found")
    self._tasks.remove(task)
    return task
```

**Edge Cases**:
- Empty descriptions: Validate via argparse (nargs='+' ensures at least one word)
- Very long descriptions: Warn but accept (spec allows up to 1000 chars)
- Invalid IDs: Raise ValueError with user-friendly message (FR-007)

---

## Decision 5: Testing Strategy

**Decision**: Two-tier testing approach with pytest: unit tests for core logic, integration tests for CLI commands.

**Rationale**:
- Separation of concerns: unit tests test business logic in isolation; integration tests verify CLI flow
- Pytest is the de facto standard for Python testing
- Both test types are required by constitution (§3.1)

**Unit Test Pattern** (tests/unit/test_todo_manager.py):
```python
def test_add_task():
    manager = TodoManager()
    task = manager.add_task("Buy groceries")
    assert task.id == 1
    assert task.description == "Buy groceries"
    assert task.complete is False
```

**Integration Test Pattern** (tests/integration/test_cli.py):
```python
from click.testing import CliRunner
from src.cli.main import main

def test_add_command():
    result = runner.invoke(main, ["add", "Buy groceries"])
    assert result.exit_code == 0
    assert "Task added" in result.output
```

**Alternatives Considered**:
- `unittest` framework: Rejected as pytest is more modern and expressive
- Only integration tests: Rejected because unit tests are needed for core logic coverage
- Mock filesystem: Not needed for in-memory storage

---

## Decision 6: Output Format

**Decision**: Plain text output with clear formatting using f-strings.

**Rationale**:
- Spec requirement: "plain text suitable for terminal display"
- Simple and readable
- No external dependencies (e.g., rich or tabulate)

**Implementation Pattern**:
```python
def list_tasks(self) -> str:
    if not self._tasks:
        return "No tasks found."
    output = []
    for task in self._tasks:
        status = "✓" if task.complete else " "
        output.append(f"{status} [{task.id}] {task.description}")
    return "\n".join(output)
```

**Alternatives Considered**:
- JSON output: Rejected as not user-friendly for CLI
- Table formatting libraries: Rejected as overkill for simple task list
- Color-coded output: Rejected as unnecessary complexity for Phase I

---

## Technical Dependencies

### Required (Python Standard Library)
- `argparse`: Command-line argument parsing
- `dataclasses`: Type-safe data structures
- `typing`: Type hints (List, Optional, etc.)

### Testing
- `pytest`: Test framework
- `pytest-cov` (optional): Code coverage

### No External Dependencies Required
- All core functionality uses Python standard library
- Maintains simplicity and reduces attack surface

---

## Constitution Alignment Verification

Post-research constitution check confirms all Phase I constraints are respected:

- ✅ **Stateless Per Invocation**: Each command runs independently, no session state
- ✅ **No Persistence**: In-memory list resets on process exit
- ✅ **Clean Architecture**: CLI/Core/Utils boundaries maintained
- ✅ **Deterministic CLI**: Argparse with validation and clear errors
- ✅ **Simplicity**: Minimal implementation, no premature optimization
- ✅ **Spec-Driven**: All decisions derived from spec requirements

---

## Open Questions Resolved

None. All technical unknowns from the plan have been resolved through this research.

## Next Steps

Proceed to Phase 1: Design & Contracts
- Generate data-model.md from Task entity definition
- Create CLI command contracts
- Write quickstart.md
- Update agent context
