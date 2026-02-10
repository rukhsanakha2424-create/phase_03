# Research: Phase II Full-Stack Todo Web Application

**Feature**: 002-fullstack-todo | **Date**: 2026-01-05

## Decision 1: Undo Buffering Strategy
- **Decision**: Keep undo metadata client-side (React state + LocalStorage fallback) while the backend issues signed undo tokens with each deletion response.
- **Rationale**: Prevents long-lived soft deletes in Neon, honours 5 s undo window, and keeps persistence deterministic.
- **Alternatives Considered**:
  1. Server-side soft delete table with TTL cleanup — rejected due to added schema complexity and violation of deterministic delete semantics.
  2. Redis/queue-backed undo buffer — rejected because it introduces a new datastore outside the constitution.

## Decision 2: Optimistic Update Reconciliation
- **Decision**: Each PATCH/DELETE request includes a UUID `request_id`; FastAPI returns the updated Todo so the UI reconciles without extra fetches.
- **Rationale**: Ensures idempotency, supports offline-like editing, and aligns with typed contracts.
- **Alternatives Considered**:
  1. Post-operation polling (GET after every mutation) — increases latency and load.
  2. WebSocket push for confirmation — scope creep for Phase II.

## Decision 3: Neon Connection Management
- **Decision**: FastAPI uses SQLAlchemy engine with PgBouncer-compatible connection string (max pool 5). Next.js interacts only through the backend API, not the database.
- **Rationale**: Avoids exhausting Neon limits, keeps architecture within clean separation principle.
- **Alternatives Considered**:
  1. Direct Next.js DB access — violates clean architecture separation.
  2. Larger pool sizes — unnecessary for MVP concurrency and risks hitting Neon cap.

## Decision 4: Contract Sharing
- **Decision**: Generate OpenAPI schema from FastAPI routers; run `openapi-typescript` to produce TS types plus `zod-to-ts` for UI validation parity.
- **Rationale**: Guarantees deterministic typed contracts across backend/frontend with zero drift.
- **Alternatives Considered**:
  1. Handwritten TypeScript interfaces — error-prone and drifts from backend behavior.
  2. GraphQL schema — introduces new stack outside scope.

## Decision 5: Testing Stack Alignment
- **Decision**: Backend uses pytest + httpx client + pytest-asyncio; frontend uses Playwright for E2E flows (desktop + mobile viewports) and Jest/RTL for components. Contract tests run via schemathesis against OpenAPI snapshots.
- **Rationale**: Covers unit, integration, and E2E layers with deterministic tooling and automated diffing of API schemas.
- **Alternatives Considered**:
  1. Cypress for E2E — less native support for Next.js App Router streaming responses.
  2. Manual QA — insufficient for production-ready requirements.
