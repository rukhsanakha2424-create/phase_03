# Data Model: Phase II Full-Stack Todo

**Feature**: 002-fullstack-todo | **Date**: 2026-01-05

## Entities

### Todo
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | integer (PK) | Auto-increment, immutable | Mirrors Phase I deterministic IDs (server-generated) |
| title | string | Required, 1-140 chars | Validation rejects whitespace-only values |
| notes | string? | Optional, 0-500 chars | Stored as TEXT |
| priority | enum('low','medium','high') | Default 'medium' | Optional extension to CLI parity |
| completed | boolean | Default false | Toggled via completion endpoint |
| created_at | datetime (UTC) | Auto-set on insert | Stored with timezone |
| updated_at | datetime (UTC) | Auto-set on insert/update | Reflects last mutation |
| completed_at | datetime? | Nullable | Only set when completed=true |

### UndoToken (transient, not persisted)
- Generated on delete responses: `{ token: string, expires_at: iso8601 }`
- Client stores token locally; backend verifies signature + expiry when undo invoked.

## Relationships
- Single table `todos`; no foreign keys in Phase II.
- Undo tokens map to deleted todo IDs for up to 5 seconds; after window expires, record removal is permanent.

## Validation Rules
| Rule | Enforcement |
|------|-------------|
| Title required, <=140 chars | Pydantic schema + frontend Zod validation |
| Notes <=500 chars | Pydantic + frontend validation |
| Priority limited to enum | SQLModel Enum + frontend select |
| completed_at requires completed=true | SQLModel validator + service guard |
| Deletion requires undo token for restoration | Service ensures token matches last delete |

## State Transitions
```
      ┌─────────┐   complete()    ┌─────────────┐
      │ Pending │ ──────────────▶ │ Completed   │
      └─────────┘ ◀────────────── └─────────────┘
            ▲      reopen()
            │
            │ delete()
            │  (undo window)
            ▼
        [Deleted*]
```
`[Deleted*]` represents physical removal plus client-side undo token. Undo re-inserts row using prior payload before token expiry.

## Derived Views
- API list endpoint sorts by `created_at DESC` and filters by `completed` status.
- UI maintains optimistic client state but server remains source of truth.

## Repository Responsibilities
- `TodoRepository` wraps SQLModel session for CRUD and toggle operations.
- All mutations occur within transactions to maintain deterministic timestamps.
- Observability hooks log request_id + todo_id per mutation.
