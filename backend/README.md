# Phase II Todo Backend (FastAPI + SQLModel)

This backend scaffolding follows the Spec-Kit Plus constitution for Phase II, providing the foundation for FastAPI services backed by Neon PostgreSQL.

## Prerequisites
- Python 3.11+
- Access to a Neon PostgreSQL database (DATABASE_URL)
- Virtual environment tooling (venv, uv, or poetry)

## Setup
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
```
Update `.env` with your Neon credentials and secrets.

## Running the App
```bash
uvicorn app.main:app --reload
```
This automatically creates the required tables via SQLModel on startup.

## Project Layout
```
backend/
├── pyproject.toml
├── README.md
├── .env.example
└── src/app/
    ├── main.py
    ├── config/
    │   └── settings.py
    ├── db/
    │   └── session.py
    ├── domain/
    │   └── todos/
    │       └── service.py
    ├── schemas/
    │   └── todo.py
    ├── api/v1/
    │   └── todos.py
    └── observability/
        └── logging.py
```

## Tests
Placeholder `tests/` directory is included. Future work will add pytest suites for unit, integration, and contract coverage.
