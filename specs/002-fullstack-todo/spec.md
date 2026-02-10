# Feature Specification: Phase II Full-Stack Todo Web Application

**Feature Branch**: `002-fullstack-todo`
**Created**: 2026-01-05
**Status**: Draft
**Input**: User description: "Project: Phase II – Full-Stack Todo Web Application ... Generate the complete formal specification."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Capture Todos Anywhere (Priority: P1)
As a busy user, I need to add todos from the responsive web UI so every task is saved to the shared Neon database and echoed back instantly.

**Why this priority**: Todo capture is the gateway for all other workflows and must feel reliable on every device.

**Independent Test**: From a fresh account, submit new tasks via desktop and mobile breakpoints; confirm each appears in the UI list and via GET `/todos`.

**Acceptance Scenarios**:
1. **Given** the todo list is empty, **When** a user submits "Schedule demo" via the add form, **Then** the task appears at the top of the list with a generated ID and default "incomplete" status.
2. **Given** network latency under 500 ms, **When** a user adds a todo, **Then** the UI shows optimistic feedback and reconciles with server response without duplicates.
3. **Given** the database rejects a payload (e.g., missing title), **When** the user submits it, **Then** inline validation prevents creation and surfaces a typed error message.

---

### User Story 2 - Inline Update & Completion (Priority: P1)
As a user reviewing tasks, I want to edit titles inline and toggle completion without leaving the list so I can maintain flow while triaging work.

**Why this priority**: Rapid editing keeps the app competitive with native notes apps and mirrors Phase I CLI update/complete parity.

**Independent Test**: Load a list with mixed statuses, edit titles via inline controls, toggle completion, and confirm changes persist across refresh/API calls.

**Acceptance Scenarios**:
1. **Given** a todo "Call Jon" exists, **When** the user edits the text inline to "Call Joan" and blurs the field, **Then** the updated value persists after page refresh and API retrieval.
2. **Given** a todo is incomplete, **When** the checkbox is toggled, **Then** the status updates to complete, renders with completed styling, and the API returns `completed=true`.
3. **Given** the user loses connectivity mid-edit, **When** the update fails, **Then** the UI reverts to the previous value and displays a non-blocking error banner.

---

### User Story 3 - Guided Review & Filtering (Priority: P2)
As a user with many todos, I want to view all tasks in chronological order and optionally filter by completion so I can plan my day efficiently.

**Why this priority**: Viewing and filtering ensure parity with Phase I list behavior and supports high task counts.

**Independent Test**: Seed >20 todos, verify default sorted order, apply completion filters, ensure pagination (if needed) stays in sync with API responses.

**Acceptance Scenarios**:
1. **Given** multiple todos exist, **When** the user opens the list, **Then** tasks display newest-first with created timestamps and completion indicators.
2. **Given** both complete and incomplete todos exist, **When** the user filters to "Incomplete", **Then** only tasks with `completed=false` render and API queries respect the filter.
3. **Given** no todos match a filter, **When** the user applies it, **Then** the UI shows an empty-state message with guidance to clear filters.

---

### User Story 4 - Delete & Undo Opportunity (Priority: P2)
As a user cleaning up, I need to delete tasks and receive a brief undo option so accidental removals can be reversed before being lost.

**Why this priority**: Deletion completes CRUD parity and aligns with production-ready UX expectations.

**Independent Test**: Delete tasks from different devices, observe undo toast duration, confirm permanent removal after timeout, and verify Neon state matches UI.

**Acceptance Scenarios**:
1. **Given** a todo is visible, **When** the user hits delete, **Then** the item disappears immediately and an undo toast appears for at least 5 seconds.
2. **Given** the user clicks undo within the toast window, **When** the action executes, **Then** the todo reappears with identical data and no duplicate record.
3. **Given** the undo window expires, **When** the user refreshes, **Then** the deleted todo remains absent from both UI and API responses.

---

### Edge Cases
- What happens when two clients edit the same todo simultaneously? (Last write wins with conflict messaging.)
- How does the system respond when Neon is temporarily unavailable? (Show clear error, retry policy per spec.)
- How does the UI behave when the todo list exceeds a device viewport? (Ensure scrollability while keeping input visible.)
- What if a user submits titles exceeding the maximum length? (Reject via validation, show remaining characters.)
- How are timezones handled for `created_at` display? (Always convert to user locale while storing UTC.)

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: The system MUST allow users to create todos with a required title, optional priority (default medium), and optional notes via the web UI; submissions must persist to the Neon database within one second.
- **FR-002**: The system MUST expose RESTful endpoints for create, read, update, delete, and toggle completion so external clients and the UI share identical behavior.
- **FR-003**: The system MUST support inline editing of todo titles and notes, saving changes automatically on blur or Enter, with optimistic UI feedback and rollback on failure.
- **FR-004**: The system MUST allow toggling completion status through both UI checkboxes and API PATCH operations while emitting deterministic timestamps for status transitions.
- **FR-005**: The system MUST provide list retrieval with sorting (newest first) and filters for completion state so phase parity with CLI `list` is preserved.
- **FR-006**: The system MUST enable deletion with a reversible grace period surfaced in the UI; expired deletions become permanent and consistent in persistence.
- **FR-007**: The system MUST enforce validation (non-empty titles under 140 characters, boolean completed flag, ISO 8601 timestamps) and return typed error payloads with HTTP status codes (400 validation, 404 missing todo, 409 conflict, 500 internal).
- **FR-008**: The system MUST auto-provision and migrate Neon tables on startup, guaranteeing schema matches SQLModel definitions before serving traffic.
- **FR-009**: The system MUST log structured events for every mutation (add/update/complete/delete) including request ID, user agent, and outcome for observability.
- **FR-010**: The system MUST secure environment-driven configuration (database URL, logging level, allowed origins) and refuse to start when critical variables are missing.

### Key Entities
- **Todo**: Canonical task object with attributes `{ id: integer primary key, title: string (1-140 chars), notes?: string (0-500 chars), completed: boolean default false, created_at: datetime (UTC), updated_at: datetime, completed_at?: datetime }`. The domain layer enforces invariants (e.g., `completed_at` present only when `completed=true`).
- **User Interaction Session**: Represents a UI session encapsulating viewport size, optimistic state queue, current filters, and undo stack. Not persisted, but used to guarantee deterministic UI feedback and align with API contracts.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: 95% of todo creations complete (UI acknowledgement + Neon persistence) within 1 second under nominal load.
- **SC-002**: Users can complete the add → inline edit → toggle completion → delete (with undo) workflow in under 90 seconds on both desktop (>1024px) and mobile (<640px) breakpoints.
- **SC-003**: API endpoints return typed error payloads for 100% of invalid requests observed in integration tests; no generic 500 leaks of internal stack traces.
- **SC-004**: System restarts initialize schema and serve traffic in under 10 seconds with environment validation failures surfaced before binding network ports.
- **SC-005**: Observability logs include correlation IDs for 100% of write operations, enabling end-to-end tracing during audits.

## Assumptions
- Single-tenant deployment; authentication/authorization handled by future phases (all requests treated as belonging to one workspace).
- Neon provides a dedicated database branch with sufficient throughput for MVP traffic (≤100 concurrent users) and allows auto-creation on startup.
- Client-server communication uses JSON over HTTPS with UTF-8 encoding and timezone-aware timestamps.
- Undo duration is fixed at 5 seconds and is not configurable in Phase II.
- Feature relies on browser LocalStorage only for ephemeral undo queues; all authoritative data resides in Neon.

## Out of Scope
- Multi-user accounts, sharing, or team workspaces.
- Task categorization, tagging, reminders, or recurring schedules.
- Offline mode or background synchronization.
- Bulk import/export, file attachments, or rich text editing.
- AI assistance, natural language parsing, or voice interfaces (reserved for Phase III).
