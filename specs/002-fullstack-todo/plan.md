# Implementation Plan: Phase II Full-Stack Todo Web Application

**Branch**: `002-fullstack-todo` | **Date**: 2026-01-05 | **Spec**: specs/002-fullstack-todo/spec.md
**Input**: Feature specification from `/specs/002-fullstack-todo/spec.md`

## Summary
Deliver a production-ready, full-stack Todo experience that mirrors Phase I CLI logic while adding a responsive Next.js UI, FastAPI backend, and Neon PostgreSQL persistence. The plan phases in backend/API foundations, database migrations, typed contracts, frontend construction with shadcn/ui, and end-to-end validation covering inline edits, completion toggles, filtering, and deletion with undo.

## Technical Context
**Language/Version**: Python 3.13 (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Pydantic v2, Alembic, Next.js (App Router), React 18, Tailwind CSS, shadcn/ui, Zod, Playwright
**Storage**: Neon-hosted PostgreSQL (managed via SQLModel + Alembic)
**Testing**: pytest + httpx for backend, Playwright for E2E, Jest/RTL for component behavior
**Target Platform**: Backend: Linux container (uvicorn). Frontend: Vercel-compatible Next.js build.
**Project Type**: Dual project (backend + frontend) sharing domain contracts
**Performance Goals**: p95 API latency < 300 ms for CRUD calls; UI create+persist < 1 s for 95% of events
**Constraints**: Deterministic typed contracts, no alternate datastores, undo grace window fixed at 5 s, all code agent-generated
**Scale/Scope**: Single tenant MVP supporting ≤100 concurrent users, thousands of todos

## Constitution Check
1. Spec-first execution ✅ — spec v1 approved before plan
2. Agent-generated code ✅ — plan references Spec-Kit automation, no manual coding
3. Phase I logic parity ✅ — plan mirrors add/list/update/delete/complete semantics across layers
4. Clean architecture separation ✅ — distinct UI/API/Domain/Persistence steps defined
5. Deterministic typed contracts ✅ — OpenAPI + shared TypeScript types scheduled
6. Neon PostgreSQL persistence ✅ — migrations + repository layers tied to Neon branch
7. Reviewable artifacts ✅ — research, data-model, contracts, quickstart produced before implementation
8. Production-ready delivery ✅ — observability, CI hooks, environment validation and undo behavior included

Gate status: PASS — proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)
```text
specs/002-fullstack-todo/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── todos.openapi.json (and derived client schemas)
└── tasks.md (created by /sp.tasks)
```

### Source Code (repository root)
```text
backend/
├── src/
│   ├── app/__init__.py
│   ├── app/main.py
│   ├── app/config.py
│   ├── app/api/v1/todos.py
│   ├── app/domain/todos/service.py
│   ├── app/domain/todos/models.py
│   ├── app/db/session.py
│   ├── app/db/migrations/
│   └── app/observability/
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── api/
│   ├── components/
│   └── (server actions)
└── tests/
    └── e2e/
```

**Structure Decision**: Dual repo layout keeps backend and frontend isolated per Principle 4 while enabling shared contract generation (OpenAPI → TypeScript) via scripts.

## Complexity Tracking
_Not required — no constitution violations identified._

## Phase 0: Research & Unknown Resolution

### Objectives
- Resolve technology choices around undo persistence, optimistic UI strategy, Neon connection sizing, and concurrency conflicts.
- Document best practices ensuring typed parity between FastAPI and Next.js (OpenAPI client generation, Zod schema alignment).
- Capture deployment/environment considerations for both projects.

### Tasks
1. **Undo buffering strategy** — Investigate storing undo tokens in browser LocalStorage vs. React state; confirm server does not retain deleted records beyond undo window.
2. **Optimistic update reconciliation** — Research FastAPI + PostgreSQL patterns for idempotent PATCH updates to avoid conflicts, referencing SQLModel session management.
3. **Neon connection management** — Determine pool sizing and connection string formats for serverless (Next.js server actions) vs. FastAPI backend.
4. **Shared contract generation** — Evaluate tooling (e.g., openapi-typescript, Orval) to derive TS clients from FastAPI schema, ensuring alignment with Zod validation.
5. **Testing stack** — Gather best practices for Playwright against Next.js App Router with FastAPI backend to cover cross-origin scenarios.

### Deliverable
`specs/002-fullstack-todo/research.md` capturing each decision with Rationale + Alternatives.

## Phase 1: Design & Contracts
_Prerequisite: research.md complete and approved._

### Data Model (data-model.md)
1. Model Todo entity with SQLModel including fields from spec (id, title, notes, completed, timestamps, completed_at, priority).
2. Define enumerations/defaults (priority levels, status). Map to Pydantic schemas for API responses.
3. Document validation rules, relationships, and state transitions (pending ↔ completed, deletion lifecycle with undo token states).

### API Contracts (contracts/)
1. Create OpenAPI v3 specification for `/todos` collection:
   - POST /todos (create)
   - GET /todos (list with `status` filter)
   - PATCH /todos/{id} (partial update inline edits)
   - PATCH /todos/{id}/toggle (completion)
   - DELETE /todos/{id} (with undo token in response)
   - POST /todos/{id}/undo (restore within window)
2. Include request/response schemas referencing Todo and Error envelopes per constitution typed contract rules.
3. Generate TypeScript client + Zod schemas from OpenAPI for frontend consumption.

### Quickstart (quickstart.md)
Document environment setup: Neon branch creation, backend `.env` variables, frontend `.env.local`, commands to run backend (uvicorn) and frontend (next dev), plus instructions to execute migrations and Playwright tests.

### Agent Context Update
Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude` to sync new dependencies and architectural notes for future commands.

### Constitution Re-check
After design artifacts are produced, re-evaluate gate compliance (ensuring typed contracts, Neon usage, reviewable docs). Document status in plan.

## Phase 2 Preview (Implementation Prep)
_Implementation deferred to `/sp.tasks` & coding phases; captured here for ordering only._
1. Backend foundation (FastAPI app scaffold, config, logging, health checks).
2. Database migrations + SQLModel models.
3. Repository + domain services aligning with Phase I logic.
4. API routers + validation + structured errors.
5. Frontend initial layout, global styles (Tailwind, shadcn).
6. UI components for list, inline edit, completion toggle, delete/undo.
7. API integration (hooks/server actions, optimistic updates, undo queue, error banners).
8. Testing (unit, integration, E2E) aligned with success criteria.

---

# research.md

## Research Decisions
1. **Undo Buffering**
   - Decision: Keep undo metadata client-side (LocalStorage + React state) and send undo tokens with deletion responses for validation.
   - Rationale: Avoids server-side soft deletes while meeting 5 s undo window; simplifies Neon schema.
   - Alternatives: (a) Server-side soft delete table (adds complexity) (b) Redis queue (introduces new dependency).

2. **Optimistic Updates**
   - Decision: Use UUID-based request IDs and PATCH endpoints returning updated Todo to reconcile UI state.
   - Rationale: Aligns with deterministic contracts, prevents double submissions.
   - Alternatives: Polling after submission (adds latency), websockets (overkill for Phase II).

3. **Neon Connections**
   - Decision: Use PgBouncer-compatible connection string with SQLAlchemy pooling (max 5 connections) for FastAPI; Next.js interacts only through backend API (no direct DB access).
   - Rationale: Keeps architecture clean and avoids connection exhaustion.
   - Alternatives: Direct Next.js DB access (violates clean separation).

4. **Contract Sharing**
   - Decision: Generate OpenAPI from FastAPI and produce TypeScript types via openapi-typescript + Zod inference, consumed by Next.js server actions.
   - Rationale: Guarantees parity and typed safety.
   - Alternatives: Handwritten types (error-prone), GraphQL (scope creep).

5. **Testing Stack**
   - Decision: Use pytest + httpx for backend, Playwright for browser flows, and contract diff checking via schemathesis/OpenAPI snapshots.
   - Rationale: Covers API + UI parity and prevents regressions.
   - Alternatives: Cypress (less SSR aware), manual testing (not acceptable).

---

# data-model.md (planned content)
- Todo entity definition with SQLModel + Pydantic.
- Validation tables for each field.
- State diagrams for pending ↔ completed + deleted with undo tokens.
- Repository responsibilities and invariants.

# contracts/
- `todos.openapi.json`: canonical spec with endpoints, schemas, errors.
- `schemas/` TypeScript + Zod outputs for frontend.

# quickstart.md
- Prereqs (Python, Node, Neon account)
- Setup commands for backend/frontend
- Running migrations, dev servers, Playwright suite.

# tasks.md (future via /sp.tasks)
- Will consume this plan to create executable tasks.
