# Feature Specification: Rich Todo Suite

**Feature Branch**: `003-rich-todo-suite`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description: "Rich React/Next.js todo client with optimistic UX, undo queue, and polished styling"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create & View Todos (Priority: P1)
Users want to add todos with validation feedback and immediately see them in a responsive list without page reloads.

**Why this priority**: Creates the MVP value—without create/list, no workflow exists.

**Independent Test**: A new user can open the app, submit a title, and see the todo appear in the list and persist on refresh.

**Acceptance Scenarios**:
1. **Given** the todos page is empty, **When** the user submits a valid title, **Then** the todo appears at the top of the list with pending status.
2. **Given** the user submits an empty title, **When** validation runs, **Then** an inline error explains the requirement and no API call fires.

---

### User Story 2 - Manage Existing Todos (Priority: P2)
Users need to edit, toggle completion, delete todos, and filter lists by status to keep work organized.

**Why this priority**: Enables day-to-day maintenance and mirrors CLI parity requirements.

**Independent Test**: With seed todos present, a user can inline edit a title, toggle completion, delete a todo, and switch between All/Pending/Completed filters with immediate feedback.

**Acceptance Scenarios**:
1. **Given** a todo exists, **When** the user edits the title and blurs the field, **Then** the change is saved and reflected in the list.
2. **Given** a user is viewing completed todos, **When** they switch the filter to Pending, **Then** only incomplete todos display and the URL/search params update accordingly.

---

### User Story 3 - Undo & Resilient Optimistic UX (Priority: P3)
Users can undo destructive actions within 5 seconds and rely on optimistic UI that gracefully rolls back when the backend rejects a change.

**Why this priority**: Prevents data loss, increases trust, and fulfills the undo queue requirement.

**Independent Test**: Deleting a todo shows an Undo toast with countdown; clicking undo restores the todo without full refresh even under flaky network conditions.

**Acceptance Scenarios**:
1. **Given** a todo is deleted, **When** the user clicks Undo within 5 seconds, **Then** the todo reappears in the correct state and the server is called to restore it.
2. **Given** an optimistic update fails due to API error, **When** the error surfaces, **Then** the UI rolls back to the previous state and shows an ErrorBanner explaining next steps.

---

### Edge Cases
- What happens when titles exceed max length (64 chars) or include leading/trailing whitespace?
- How does system handle network failures or backend validation errors during optimistic mutations?
- How is undo handled when the queue expires or the server rejects the restore request?
- What happens if multiple actions queue simultaneously (delete + edit) before TTL expires?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create todos with client-side and server-side validation (title required, <=64 chars).
- **FR-002**: System MUST list todos with loading, empty, and error states synchronized with backend filters.
- **FR-003**: Users MUST be able to inline edit todo titles with optimistic save and rollback.
- **FR-004**: System MUST let users toggle completion state with filter-aware cache updates.
- **FR-005**: System MUST support deleting todos and queuing undo actions with 5-second expiry.
- **FR-006**: Users MUST be able to filter the list by All/Pending/Completed via toolbar + query params.
- **FR-007**: UI MUST surface global errors via ErrorBanner and context-specific toasts, including undo countdowns.

### Key Entities

- **Todo**: id (UUID), title, status (pending|completed), createdAt, updatedAt. Supports inline edits, toggles, deletes.
- **UndoAction**: id, todoSnapshot, actionType (delete|update), expiresAt, status (pending|executed). Stored client-side via Zustand + localStorage.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Creating a todo completes in <300ms p95 (excluding network) with optimistic update showing within 50ms.
- **SC-002**: Undo success rate ≥ 99% when triggered within 5 seconds, with clear error messaging otherwise.
- **SC-003**: 95% of manual QA runs pass FR-001..FR-007 scenarios without regressions.
- **SC-004**: Accessibility audit (axe) reports 0 critical violations on Todos page.
