# Tasks: Rich Todo Suite

**Input**: Checklist provided in /sp.task response (Next.js frontend with undo + optimistic UX)
**Prerequisites**: plan.md (pending), spec.md (to be synthesized from checklist), research.md, data-model.md, contracts/

**Tests**: Unit tests + hook tests are required per checklist. Playwright E2E tests are optional but planned in Polish phase.

**Organization**: Tasks are grouped by execution phase to honor dependencies and maintain independently testable user stories.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Task can run in parallel (different files, no ordering constraints)
- **[Story]**: User story identifier (US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Scaffold Next.js workspace, dependencies, and base tooling so later stories have a consistent foundation.

- [ ] T001 Initialize Next.js 13+ App Router project under `frontend/` with TypeScript and Turbopack enabled per plan.
- [X] T002 Install core dependencies in `frontend/package.json`: React 19, Next 13+, TypeScript, Tailwind CSS v4, shadcn/ui, lucide-react.
- [X] T003 [P] Install state/data tools (TanStack Query, Zustand, Zod, axios) and add npm scripts (`dev`, `build`, `lint`, `test`).
- [X] T004 [P] Configure Tailwind base files in `frontend/tailwind.config.ts` and `frontend/postcss.config.mjs`, enabling shadcn presets.
- [X] T005 Set up ESLint + TypeScript configs (`frontend/eslint.config.mjs`, `tsconfig.json`) with Next + React rules.
- [X] T006 Initialize testing stack (`@testing-library/react`, `@testing-library/jest-dom`, `vitest` or `jest`) and base test script in `frontend/package.json`.

**Checkpoint**: Base Next.js project builds locally with lint/test commands available.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Infrastructure shared across all stories—providers, design tokens, API client, schemas, and global state. No user story work can begin until complete.

- [ ] T007 Configure global providers in `frontend/src/app/layout.tsx`: ThemeProvider, QueryClientProvider, ToastProvider, UndoQueueProvider shell.
- [ ] T008 [P] Define shared types & Zod schemas for todos in `frontend/src/lib/types/todo.ts` (Todo, TodoInput, filters, API error shape).
- [ ] T009 Implement API client layer in `frontend/src/lib/api/todos.ts` wrapping backend endpoints with Axios + schema validation.
- [ ] T010 Set up TanStack Query client utilities in `frontend/src/lib/query/client.ts` (cache keys, default retry/backoff policies).
- [ ] T011 Create Zustand UndoQueue store in `frontend/src/lib/state/undo-queue.ts` with 5s expiry + localStorage persistence helpers.
- [ ] T012 [P] Scaffold shared UI primitives via shadcn in `frontend/src/components/ui/` (Button, Card, Input, Skeleton, Toast).
- [ ] T013 Configure app-level styles (`frontend/src/app/globals.css`) with SaaS gradient theme, fonts, and dark-mode tokens.
- [ ] T014 [P] Add ErrorBoundary + suspense-ready wrappers for app routes in `frontend/src/app/(todos)/layout.tsx`.

**Checkpoint**: Providers render without runtime errors; base hooks can integrate with the API client and undo store.

---

## Phase 3: User Story 1 – "Create and View Todos" (Priority: P1) 🎯 MVP

**Goal**: Users can create todos with validation and immediately view the list sourced from backend APIs.
**Independent Test**: Start app, create a todo via form, ensure it appears in TodoList and persists on reload.

### Tests (write before implementation)
- [ ] T015 [P] [US1] Unit test TanStack query hook `useTodos` in `frontend/src/hooks/__tests__/useTodos.test.tsx` covering loading/error states.
- [ ] T016 [P] [US1] Component test for `TodoCreateForm` validation in `frontend/src/components/todos/__tests__/TodoCreateForm.test.tsx`.

### Implementation
- [ ] T017 [US1] Build `/todos` route structure in `frontend/src/app/(todos)/page.tsx` rendering TodosPage shell.
- [ ] T018 [P] [US1] Implement `useTodos` and `useCreateTodo` hooks in `frontend/src/hooks/useTodos.ts` using TanStack Query.
- [ ] T019 [US1] Create `TodoCreateForm` in `frontend/src/components/todos/TodoCreateForm.tsx` with Zod form validation and shadcn form primitives.
- [ ] T020 [P] [US1] Implement `TodosPage` container in `frontend/src/features/todos/TodosPage.tsx` wiring hooks + components.
- [ ] T021 [US1] Build `TodoList` display component in `frontend/src/components/todos/TodoList.tsx` covering empty/loading states.
- [ ] T022 [US1] Add optimistic cache updates for creation (prepending new todo) with rollback on failure.
- [ ] T023 [US1] Add toast notifications for create success/failure using global ToastProvider.

**Checkpoint**: Creating todos works end-to-end with validation, list reflects backend data, tests pass.

---

## Phase 4: User Story 2 – "Manage Existing Todos" (Priority: P2)

**Goal**: Users can inline edit titles, toggle completion, delete todos, and filter by status with resilient UX.
**Independent Test**: With seed todos, user can edit text, toggle complete, delete, and switch filters without reload.

### Tests
- [ ] T024 [P] [US2] Hook tests for `useUpdateTodo`, `useToggleTodo`, `useDeleteTodo` in `frontend/src/hooks/__tests__/useTodoMutations.test.ts`.
- [ ] T025 [P] [US2] Component test for FilterBar state switching in `frontend/src/components/todos/__tests__/FilterBar.test.tsx`.

### Implementation
- [ ] T026 [US2] Extend Todo type + schemas for filter params (`status`, `search`) and update API client methods.
- [ ] T027 [P] [US2] Implement `TodoListItem` component with inline edit, toggle, delete controls in `frontend/src/components/todos/TodoListItem.tsx`.
- [ ] T028 [US2] Build `FilterBar` component in `frontend/src/components/todos/FilterBar.tsx` with shadcn SegmentedControl + query sync.
- [ ] T029 [US2] Wire TanStack query filter params via `useTodoFilters` hook in `frontend/src/hooks/useTodoFilters.ts` (URL/search params integration).
- [ ] T030 [US2] Add optimistic mutation handlers for update/toggle/delete with cache syncing and snackbars.
- [ ] T031 [US2] Create `ErrorBanner` component in `frontend/src/components/common/ErrorBanner.tsx` for surfaced API failures.
- [ ] T032 [US2] Implement `EmptyStateCard` component with CTA + gradient art in `frontend/src/components/common/EmptyStateCard.tsx`.

**Checkpoint**: Managing todos (edit/toggle/delete) and filtering works with graceful error/empty states; tests green.

---

## Phase 5: User Story 3 – "Undo & Optimistic UX Enhancements" (Priority: P3)

**Goal**: Provide undo queue with TTL, undo toast UI, and resilient optimistic experiences across actions.
**Independent Test**: Delete a todo, see UndoToast, click undo within 5s, todo returns without page reload.

### Tests
- [ ] T033 [P] [US3] Unit tests for `UndoQueue` Zustand store in `frontend/src/lib/state/__tests__/undo-queue.test.ts` covering expiry + persistence.
- [ ] T034 [P] [US3] Component test for `UndoToast` interactions in `frontend/src/components/todos/__tests__/UndoToast.test.tsx`.

### Implementation
- [ ] T035 [US3] Finalize UndoQueue store (enqueue, expire, replay) with localStorage hydration guard in `frontend/src/lib/state/undo-queue.ts`.
- [ ] T036 [US3] Build `UndoToast` component in `frontend/src/components/todos/UndoToast.tsx` hooking into ToastProvider + UndoQueue events.
- [ ] T037 [US3] Integrate UndoToast into TodosPage: on delete, enqueue undo action, show toast, revert via API call if confirmed.
- [ ] T038 [US3] Add optimistic patching helpers in `frontend/src/lib/query/optimistic.ts` to ensure Undo + cache coherence.
- [ ] T039 [US3] Implement global error boundary fallback + retry CTA for failed optimistic operations.

**Checkpoint**: Undo flows and optimistic UX enhancements operate reliably with automated coverage.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Styling, docs, and optional E2E automation once core stories function.

- [ ] T040 [P] Apply SaaS visual polish (cards, shadows, gradients, icons) across todos components via Tailwind tokens.
- [ ] T041 Harden accessibility (aria labels, focus traps, keyboard shortcuts) in `TodoListItem`, `FilterBar`, `UndoToast`.
- [ ] T042 [P] Add hook + component storybook stories in `frontend/.storybook/` for regression testing.
- [ ] T043 Configure Playwright and optional E2E spec `frontend/tests/e2e/todos.spec.ts` covering create/edit/delete/undo flow.
- [ ] T044 Update root `README.md` with frontend install/run/test instructions and feature overview.
- [ ] T045 Run manual QA against FR-001..FR-007 checklist and log outcomes in `specs/003-rich-todo-suite/quickstart.md` (once generated).

---

## Dependencies & Execution Order

### Phase Dependencies
- Phase 1 (Setup) has no prerequisites.
- Phase 2 (Foundational) depends on Phase 1 completion and blocks all user stories.
- Phase 3 (US1) can start after Phase 2.
- Phase 4 (US2) depends on Phases 1-2 and shares hooks/components from Phase 3 but remains independently testable.
- Phase 5 (US3) requires Phase 4 mutation + delete hooks.
- Phase 6 (Polish) begins after desired user stories (at least US1-US3) stabilize.

### User Story Dependencies
- **US1**: None beyond Foundational infrastructure.
- **US2**: Consumes hooks + components from US1 and extends API schema.
- **US3**: Builds on undo-capable mutations introduced by US2 (delete) and global providers from Phase 2.

### Within Each Story
- Write tests first (T015–T016, etc.) to enforce TDD.
- Implement hooks → components → containers.
- Apply optimistic + undo logic after core CRUD surfaces exist.

### Parallel Opportunities
- Tasks marked [P] touch distinct files (e.g., hook tests vs component tests, UI primitives vs state store).
- During Phase 4, FilterBar (T028) can proceed in parallel with TodoListItem (T027).
- Phase 6 polish tasks (T040–T042) are largely parallelizable once core stories land.

---

## Parallel Example: User Story 2

```bash
# Run hook + component tests concurrently after writing them:
Task T024: Hook tests for useTodo mutation suite
Task T025: FilterBar component tests

# Parallel implementation after tests:
Task T027: TodoListItem inline editing
Task T028: FilterBar UI & logic
Task T029: useTodoFilters hook
```

---

## Implementation Strategy

### MVP First (US1)
1. Complete Phase 1 + Phase 2 infrastructure.
2. Deliver US1 end-to-end (create+list) with passing tests.
3. Demo/validate before expanding scope.

### Incremental Delivery
1. After MVP, add US2 to unlock full CRUD management.
2. Layer US3 to introduce undo + polished optimistic UX.
3. Execute Polish tasks to finalize styling, docs, and E2E automation.

### Parallel Team Strategy
- Team completes Phases 1–2 together.
- Assign US1, US2, US3 to different engineers once foundations ready.
- Merge via feature branches ensuring tests per story stay green.
