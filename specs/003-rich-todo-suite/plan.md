# Implementation Plan: Rich Todo Suite

**Branch**: `003-rich-todo-suite` | **Date**: 2026-01-06 | **Spec**: `specs/003-rich-todo-suite/spec.md`
**Input**: Feature specification from `/specs/003-rich-todo-suite/spec.md`

## Summary
Deliver a production-ready Next.js 16 App Router frontend that mirrors the Phase I CLI todo behaviors (create/list/edit/toggle/delete/undo) while consuming the existing FastAPI `/api/v1/todos` endpoints. The UI must provide optimistic feedback, a 5-second undo queue, SaaS-quality styling, and accessibility that satisfies FR-001..FR-007 and success criteria SC-001..SC-004 (spec.md:59-79).

## Technical Context
**Language/Version**: TypeScript 5.x, React 19, Next.js 16 App Router.
**Primary Dependencies**: TanStack Query 5 (data/cache), Zustand (UndoQueue store), Zod (validation), shadcn/ui + Tailwind 4, Lucide icons, Axios for HTTP.
**Storage**: Backend persistence handled by existing FastAPI + Neon; frontend keeps transient optimistic state and UndoQueue snapshots in memory + `localStorage`.
**Testing**: Jest/Vitest + Testing Library for hooks/components, MSW for contract fidelity, Playwright (optional per task list) for e2e verification.
**Target Platform**: Modern browsers + Vercel-style deployment for frontend, consuming `/api/v1/todos` via `NEXT_PUBLIC_API_BASE_URL`.
**Project Type**: Web application with separate `frontend/` and `backend/` directories.
**Performance Goals**: Create flow <300 ms p95 with optimistic paint <50 ms (SC-001); undo success ≥99 % within 5 s (SC-002).
**Constraints**: No backend changes (scope decision). Must maintain typed contracts, optimistic rollback, 5 s undo TTL, URL-driven filters, and accessibility parity.
**Scale/Scope**: Single-page experience managing dozens of todos with filters, inline editing, and undo.

## Constitution Check
| Principle | Plan Compliance |
|-----------|-----------------|
| Spec-First Execution | Spec finalized (spec.md) and referenced throughout plan |
| Agent-Generated Code Only | All forthcoming code derived via Spec-Kit workflows; manual edits prohibited |
| Phase I Logic Parity | Map CLI behaviors to UI flows + existing FastAPI endpoints |
| Clean Architecture Separation | UI strictly consumes `/api/v1/todos`; no domain/persistence leakage |
| Deterministic Typed Contracts | Shared TS types + Zod schemas mirroring backend Pydantic models |
| Neon PostgreSQL Persistence | Backend already compliant; frontend remains stateless aside from undo cache |
| Reviewable Artifacts | Plan/research/data-model/contracts/quickstart tracked under `specs/003-rich-todo-suite/` |
| Production-Ready Delivery | Plan mandates linting, testing, accessibility, manual QA per FR-001..FR-007 |

No gate violations. Re-validate after Phase 1 artifacts are authored.

## Project Structure
### Documentation (this feature)
```text
specs/003-rich-todo-suite/
├── plan.md            # This document
├── research.md        # Phase 0 findings
├── data-model.md      # Entities + view models
├── quickstart.md      # Run/test instructions
├── contracts/
│   └── todos.http.yaml  # Frontend↔backend contract notes
└── tasks.md           # Generated earlier via checklist synthesis
```

### Source Code (repository root)
```text
backend/               # Existing FastAPI service (read-only for this feature)
├── src/app/api/v1/todos.py
└── ...

frontend/
├── package.json
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Providers, theming, QueryClient
│   │   └── (todos)/page.tsx    # TodosPage route
│   ├── components/
│   │   ├── todos/
│   │   │   ├── TodoCreateForm.tsx
│   │   │   ├── TodoList.tsx
│   │   │   ├── TodoListItem.tsx
│   │   │   └── UndoToast.tsx
│   │   └── common/
│   │       ├── ErrorBanner.tsx
│   │       └── EmptyStateCard.tsx
│   ├── hooks/
│   │   ├── useTodos.ts
│   │   └── useUndoQueue.ts
│   └── lib/
│       ├── api/todos.ts
│       ├── types/todo.ts
│       ├── query/client.ts
│       └── state/undo-queue.ts
└── tests/
    ├── unit/
    └── e2e/
```
**Structure Decision**: Web-app structure with dedicated directories for pages, components, hooks, lib utilities, and tests to respect clean layering.

## Complexity Tracking
| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| TanStack Query + Zustand combo | Needed for optimistic CRUD + undo TTL queue without backend changes | Plain React state would complicate cache invalidation and optimistic rollback guarantees |

## Phase 0: Research (see `research.md`)
1. Optimistic strategy: Compare TanStack Query vs. SWR; choose TanStack Query for granular cache keys, mutation rollback, and devtool insight.
2. Undo persistence: Evaluate `localStorage` vs. IndexedDB; select `localStorage` for simplicity and 5 s TTL enforcement; document hydration approach to avoid SSR mismatch.
3. Error/empty state UX: Blend inline field validation (Zod) with global `ErrorBanner` + toast notifications to cover FR-007.
4. Filter contract: Mirror backend `status` query param, introduce optional `priority` param, and sync with Next.js search params for shareable URLs.
5. Testing stack: Choose Jest/Vitest + Testing Library for components, MSW for contract mocking, Playwright optional for e2e per task list.

## Phase 1: Design Artifacts
- **data-model.md**: Document `Todo`, `TodoViewModel`, and `UndoAction` shapes, validation rules (title length, trimming), derived fields (`isOptimistic`, `undoableUntil`), and state diagrams for optimistic + undo workflows.
- **contracts/todos.http.yaml**: Capture GET/POST/PATCH/POST(toggle)/DELETE/POST(undo) routes, JSON schemas, query params, status codes, and `{code,message,details}` error taxonomy; note dependency on `NEXT_PUBLIC_API_BASE_URL`.
- **quickstart.md**: Provide environment setup (Node 20+, backend URL), installation (`npm install`), running (`npm run dev`), lint/test commands, Playwright optional steps, and troubleshooting (CORS, backend availability).
- **Agent context update**: After authoring above files, run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude` to log new stack details.

## Phase 2 (Hand-off to `/sp.tasks`)
Already generated `tasks.md` describes Setup → Foundational → US1..US3 → Polish phases aligned with this plan.

## Risks & Mitigations
1. **Backend availability**: Document fallback base URL and timeouts; highlight need for backend dev instance.
2. **Undo race conditions**: Write unit tests for concurrent deletes + TTL expiry; ensure queue handles multiple entries.
3. **Accessibility debt**: Include Axe audit tasks and ARIA checks in Polish phase; treat as release gate.
4. **Optimistic drift**: Rely on TanStack Query invalidation patterns and MSW contract tests to prevent stale cache when backend changes.

## Success Criteria Alignment
- FR-001..FR-007 mapped to hooks/components in tasks and plan.
- SC-001..SC-004 enforced via performance budgets, undo success metrics, QA checklist, and accessibility audits in Polish phase.
- Manual QA to verify create/list/edit/toggle/delete/undo flows before release.

## Pending Actions
1. Author `research.md`, `data-model.md`, `contracts/todos.http.yaml`, and `quickstart.md` per plan.
2. Update agent context script once artifacts exist.
3. Create Prompt History Record referencing this planning session.
4. Consider documenting the TanStack Query + Zustand decision via `/sp.adr frontend-optimistic-state-stack` once implementation begins.
