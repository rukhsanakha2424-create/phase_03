# Data Model: Todo In-Memory CLI

**Feature**: 001-todo-in-memory | **Date**: 2026-01-02

## Task Entity

```python
@dataclass
class Task:
    id: int                          # Unique identifier (1-indexed, sequential)
    description: str                 # Task description (1-1000 chars)
    completed: bool = False          # Completion status
    created_at: datetime = field(default_factory=datetime.utcnow)
```

## Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| description | Must be non-empty | "Task description cannot be empty" |
| description | Max 1000 characters | "Description exceeds maximum length" |
| id | Must exist for operations | "Task with ID {id} not found" |

## State Transitions

```
         ┌─────────────┐
         │   PENDING   │ (default)
         └──────┬──────┘
                │ complete()
         ┌──────▼──────┐
         │   COMPLETE  │
         └─────────────┘
```

## Storage Structure

```python
# In-memory task store (TodoManager)
# Using list as specified by user requirements
_tasks: list[Task] = []
_next_id: int = 1

# NOTE: Data resets on application restart (FR-008, FR-009)
# No persistence between executions
```

## Methods

| Method | Input | Output | Side Effects | Error Conditions |
|--------|-------|--------|--------------|------------------|
| add(description) | str | Task | Appends to _tasks list | Empty description raises ValueError |
| list() | None | str | No side effects | Returns empty message if no tasks |
| update(id, description) | int, str | Task | Modifies task in-place | Invalid ID raises ValueError |
| delete(id) | int | Task | Removes from _tasks list | Invalid ID raises ValueError |
| complete(id) | int | Task | Toggles completed flag | Invalid ID raises ValueError |

## Error Handling

All operations that require an existing task ID (update, delete, complete) must:
1. Validate that the task ID exists in _tasks
2. Raise `ValueError` with clear message: "Task with ID {id} not found" if not found
3. Return the modified/deleted task on success

## Output Format

Task list display format:
```
✓ [1] Complete task description
  [2] Incomplete task description
```

- Completed tasks: "✓" prefix
- Incomplete tasks: " " (space) prefix
- Format: `[status] [id] description`
