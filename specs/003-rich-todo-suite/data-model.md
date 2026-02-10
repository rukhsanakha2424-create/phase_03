# Data Model: Rich Todo Suite

## Todo (API Contract)
| Field | Type | Notes |
|-------|------|-------|
| `id` | string (UUID) | Comes from backend; treated as opaque.
| `title` | string | Required, trimmed, 1–64 chars (FR-001).
| `notes` | string | Optional notes textarea (user story scope).
| `priority` | enum("low","medium","high") | Defaults to medium when omitted (backend parity).
| `status` | enum("pending","completed") | Derived from backend toggle route.
| `createdAt` | ISO 8601 string | Displayed in list details.
| `updatedAt` | ISO 8601 string | Used for optimistic patches.

Validation: trim whitespace, collapse multiple spaces, reject >64 chars, block blank titles.

## TodoViewModel (UI Layer)
Adds presentation helpers:
| Field | Type | Notes |
|-------|------|-------|
| `displayTitle` | string | Trimmed + sanitized title.
| `isOptimistic` | boolean | True while mutation pending.
| `undoableUntil` | number (epoch ms) | Derived when delete mutation enqueues undo.
| `displayStatus` | string | Human label ("Pending", "Completed").
| `filterMatch` | boolean | Whether current filter shows this todo.

## UndoAction (Client-side only)
| Field | Type | Notes |
|-------|------|-------|
| `id` | string | Unique per action, e.g., `delete:<todoId>:<timestamp>`.
| `todoSnapshot` | Todo | Snapshot prior to mutation for rollback.
| `actionType` | enum("delete","update","toggle") | Determines handler.
| `expiresAt` | number (epoch ms) | TTL = delete response expiry (`now + 5000ms`).
| `status` | enum("pending","executed","expired") | Controls toast messaging.

### State Transitions
1. **Delete** → `UndoAction` enqueued with `pending`, toast shows countdown.
2. **Undo click** → call `/todos/{id}/undo`; on success, remove action + reinsert todo; on failure, mark `expired` and show error.
3. **TTL elapsed** → background sweep marks `expired`, hides toast, prevents further undo.

### Filter Parameters
- `status`: `all | pending | completed` (mirrors backend `status` query param alias).
- `priority`: `all | low | medium | high` (sent as `priority` query param when supported).
- `search`: optional substring filter applied client-side for now.

### Derived Helpers
- `toTodoInput(formData)`: trims and validates user input before POST/PUT.
- `toListQuery(filters)`: builds query string for GET with `status` + optional `priority`.
- `applyOptimisticPatch(todo, patch)`: clones Todo and merges new values while flagging `isOptimistic`.
