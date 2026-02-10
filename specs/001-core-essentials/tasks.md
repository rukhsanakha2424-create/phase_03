# Tasks: Phase 1: Core Essentials

**Input**: Design documents from `/specs/001-core-essentials/`
**Prerequisites**: plan.md (required), spec.md (required)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure (src/core, src/cli, src/utils, tests/unit, tests/integration)
- [ ] T002 Initialize Python project (pyproject.toml or requirements.txt with pytest)
- [ ] T003 [P] Configure README.md and .gitignore

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [ ] T004 Implement deterministic ID generation in `src/utils/id_gen.py`
- [ ] T005 Implement Task status Enum in `src/core/models.py`
- [ ] T006 Implement base Task model in `src/core/models.py`
- [ ] T007 Setup `src/core/service.py` with in-memory storage dictionary
- [ ] T008 Configure basic CLI argument parsing using argparse in `src/cli/main.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add a New Task (Priority: P1) 🎯 MVP

**Goal**: Allow users to add a task with a description

- [ ] T009 [US1] Integration test for "add task" in `tests/integration/test_add.py`
- [ ] T010 [US1] Implement `add_task` in `src/core/service.py`
- [ ] T011 [US1] Implement `add` command in `src/cli/main.py`
- [ ] T012 [US1] Add non-empty description validation in `src/core/service.py`

**Checkpoint**: US1 fully functional

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: Display all tasks

- [ ] T013 [US2] Integration test for "list tasks" in `tests/integration/test_list.py`
- [ ] T014 [US2] Implement `get_all_tasks` in `src/core/service.py`
- [ ] T015 [US2] Implement `list` command in `src/cli/main.py`
- [ ] T016 [US2] Implement "empty list" message feedback in CLI

**Checkpoint**: US2 fully functional

---

## Phase 5: User Story 3 & 4 - Update & Complete (Priority: P1/P2)

**Goal**: Modify task description or status

- [ ] T017 [US3/4] Integration test for "update/complete" in `tests/integration/test_update.py`
- [ ] T018 [US3/4] Implement `update_task` (id, description=None, status=None) in `src/core/service.py`
- [ ] T019 [US3/4] Implement `update` and `complete` CLI commands

**Checkpoint**: US3 & 4 fully functional

---

## Phase 6: User Story 5 - Delete a Task (Priority: P1)

**Goal**: Remove a task from the list

- [ ] T020 [US5] Integration test for "delete task" in `tests/integration/test_delete.py`
- [ ] T021 [US5] Implement `delete_task` in `src/core/service.py`
- [ ] T022 [US5] Implement `delete` command in `src/cli/main.py`

---

## Phase 7: Polish & Validation

- [ ] T023 Run all tests (pytest tests/)
- [ ] T024 Validate feedback for non-existent IDs (Error paths)
- [ ] T025 Run quickstart.md validation

---

## Dependencies & Execution Order

- **Phase 1 & 2** are mandatory and block all user stories.
- **US1 (Add)** is required before US2-US5 can be meaningful in integration.
- **US3, US4, US5** can follow in any order after US1/US2.
