# Research: Rich Todo Suite

## 1. Optimistic Data Strategy
- **Decision**: Use TanStack Query 5 for data fetching + mutations, backed by Axios.
- **Rationale**: Provides granular cache keys, built-in mutation rollback APIs, devtools visibility, and retry control per FR-001..FR-007.
- **Alternatives Considered**:
  - *SWR*: Lightweight but lacks mutation rollback primitives and would require custom cache management.
  - *React Query custom wrappers*: Duplicates TanStack Query features with more code.

## 2. Undo Queue Persistence
- **Decision**: Implement UndoQueue via Zustand store with `persist` middleware writing to `localStorage`, enforcing a 5-second TTL.
- **Rationale**: Keeps client-only undo state aligned with backend delete responses while meeting SC-002.
- **Alternatives**:
  - *IndexedDB*: Overkill for 5-second TTL and increases complexity.
  - *Backend undo tokens only*: Would require backend changes out of scope and delay UX feedback.

## 3. Error & Empty States
- **Decision**: Combine inline form validation (Zod + shadcn form components) with global `ErrorBanner` and toast notifications.
- **Rationale**: Ensures FR-007 by surfacing both field-level and global issues; toasts support optimistic rollback messaging.
- **Alternatives**:
  - *Modal-only errors*: Degrades accessibility and forces extra clicks.
  - *Silent failures*: Violates usability and success criteria.

## 4. Filtering UX Contract
- **Decision**: Mirror backend `status` query param and extend with optional `priority`. Sync with Next.js search params to allow shareable URLs and maintain state on refresh.
- **Rationale**: Keeps UI aligned with FastAPI filters (backend/src/app/api/v1/todos.py:23-33) while satisfying user story 2 acceptance tests.
- **Alternatives**:
  - *Client-side filtering only*: Risks drift with server state and breaks pagination or partial backends.
  - *Hash-based client filter state*: Less shareable and harder to test.

## 5. Testing & Tooling
- **Decision**: Jest/Vitest + Testing Library for hooks/components, MSW for contract mocking, Playwright for optional e2e.
- **Rationale**: Covers unit + integration layers required by tasks list while keeping CI lightweight.
- **Alternatives**:
  - *Cypress only*: Heavier, slower for hook tests.
  - *Unit tests only*: Would miss contract regressions and undo flows.
