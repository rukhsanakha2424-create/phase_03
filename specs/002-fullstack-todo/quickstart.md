# Quickstart: Phase II Full-Stack Todo Web Application

## Prerequisites
- Python 3.13 with uv, poetry, or pipx tooling
- Node.js 20 LTS + pnpm
- Neon account with provisioned database branch
- OpenSSL for generating signing secrets

## Environment Setup
1. Copy `.env.example` to backend `.env` and set:
   - `DATABASE_URL` (Neon pooled connection string)
   - `NEON_CA_CERT` path (if needed)
   - `REQUEST_ID_HEADER=X-Request-ID`
   - `UNDO_TOKEN_SECRET`
2. Copy `.env.example` to frontend `.env.local` and set:
   - `API_BASE_URL=http://localhost:8000`
   - `NEXT_PUBLIC_APP_NAME=Todo`

## Install Dependencies
```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
pnpm install
```

## Database Migration
```bash
cd backend
alembic upgrade head
```

## Running Services
```bash
# Backend
uvicorn app.main:app --reload --port 8000

# Frontend
cd ../frontend
pnpm dev --port 3000
```

## Testing
```bash
# Backend unit/integration
cd backend
pytest

# Contract diff
pytest tests/contract

# Frontend + E2E
cd ../frontend
pnpm test
pnpm exec playwright test
```

## Workflow
1. Start backend then frontend.
2. Launch http://localhost:3000 to use the UI.
3. Use Playwright tests for regression before commit.
