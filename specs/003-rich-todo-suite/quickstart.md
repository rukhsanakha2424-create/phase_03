# Quickstart: Rich Todo Suite Frontend

## Prerequisites
- Node.js 20+
- npm 10+
- Running FastAPI backend (see `backend/README.md`) exposing `/api/v1/todos`
- `.env.local` configured with:
  ```env
  NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
  UNDO_TTL_MS=5000
  ```

## Install
```bash
cd frontend
npm install
```

## Local Development
```bash
npm run dev
```
- Opens at http://localhost:3000
- Requires backend reachable at `${NEXT_PUBLIC_API_BASE_URL}`

## Linting & Tests
```bash
npm run lint        # ESLint + Next rules
npm run test        # Jest/Vitest component + hook tests
npx playwright test # (optional) E2E create/edit/toggle/delete/undo flow
```

## Manual QA Checklist
1. Create todo → appears instantly, persists on refresh.
2. Inline edit title → saves without reload.
3. Toggle completion → status pill updates, filter respects change.
4. Delete → Undo toast appears; clicking Undo within 5 s restores item.
5. Switch filters (All/Pending/Completed) → query params update.
6. Offline/network error simulation → ErrorBanner + optimistic rollback triggered.

## Troubleshooting
| Symptom | Fix |
|---------|-----|
| 401/403 errors | Confirm backend auth disabled or provide token headers if required. |
| CORS failure | Ensure FastAPI `ALLOW_ORIGINS` includes http://localhost:3000. |
| Undo not working | Backend must support `/todos/{id}/undo`; ensure server logs show delete + undo endpoints invoked within 5 s. |
| Hook tests failing on fetch | Run `npm run test -- --runInBand` to avoid race conditions; ensure MSW handlers match contract. |

## Backend Coordination
- Backend lives under `backend/`; no changes required for this feature.
- Ensure backend `.env` matches frontend base URL.
- Use seeded data for QA to cover filters + undo scenarios.
