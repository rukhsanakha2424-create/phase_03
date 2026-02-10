# Tasks: Phase 2: Organization & Usability

**Input**: Design documents from `.specify/specs/002-organization-usabilities/`
**Prerequisites**: plan.md (required), spec.md (required)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)

## Phase 1: Setup (Data Persistence)

**Purpose**: Enable file-based storage

- [ ] T001 Create `data/` directory and `data/todos.json`
- [ ] T002 Implement `src/core/storage.py` with JSON load/save
- [ ] T003 Update `src/core/service.py` to integrate storage

---

## Phase 2: Priority Support

**Purpose**: Add LOW/MEDIUM/HIGH priority levels

- [ ] T004 Update `src/core/models.py` with `TaskPriority` enum
- [ ] T005 Add `priority` field to `Task` dataclass
- [ ] T006 Update `add` command to accept `--priority` flag
- [ ] T007 Update `update` command to modify priority

---

## Phase 3: Search

**Purpose**: Find tasks by keyword

- [ ] T008 [P] Implement `search` CLI command in `src/cli/main.py`
- [ ] T009 [P] Add unit tests for search functionality

---

## Phase 4: Filter

**Purpose**: Filter by status or priority

- [ ] T010 [P] Add `--status` filter to `list` command
- [ ] T011 [P] Add `--priority` filter to `list` command
- [ ] T012 [P] Add unit tests for filter functionality

---

## Phase 5: Sort

**Purpose**: Order tasks by various criteria

- [ ] T013 [P] Add `--sort` option to `list` command (priority, date, status)
- [ ] T014 [P] Add unit tests for sort functionality

---

## Phase 6: Polish & Validation

- [ ] T015 Verify JSON persistence works across sessions
- [ ] T016 Run all tests
- [ ] T017 Update quickstart.md

---

## Dependencies

- Phase 1 (Setup) blocks all other tasks
- T004-T007 (Priority) can proceed in parallel with T008-T014 (Search/Filter/Sort)
