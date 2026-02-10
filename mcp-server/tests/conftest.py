"""Pytest configuration and fixtures for MCP Adapter tests."""

import asyncio
import os
from typing import AsyncGenerator

import asyncpg
import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.db.connection import DatabasePool


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_database_url() -> str:
    """Get the test database URL from environment or use a default."""
    return os.getenv(
        "TEST_DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/todos_test",
    )


@pytest.fixture(scope="session")
async def setup_test_database(test_database_url: str) -> AsyncGenerator[None, None]:
    """Set up test database schema.

    Creates the tasks table and initializes the connection pool.
    """
    # Initialize the database pool
    await DatabasePool.initialize(test_database_url)

    pool = DatabasePool.get_pool()

    # Create tasks table
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
    """

    async with pool.acquire() as connection:
        await connection.execute(create_table_sql)

    yield

    # Clean up: drop the table after tests
    async with pool.acquire() as connection:
        await connection.execute("DROP TABLE IF EXISTS tasks;")

    # Close the pool
    await DatabasePool.close()


@pytest.fixture
async def db_pool(setup_test_database) -> asyncpg.Pool:
    """Get the database connection pool for tests.

    This fixture depends on setup_test_database to ensure the schema is created.
    """
    return DatabasePool.get_pool()


@pytest.fixture
async def clean_database(db_pool: asyncpg.Pool) -> None:
    """Clean up tasks table between tests."""
    async with db_pool.acquire() as connection:
        await connection.execute("DELETE FROM tasks;")

    yield

    # Clean up after the test
    async with db_pool.acquire() as connection:
        await connection.execute("DELETE FROM tasks;")


@pytest.fixture
async def sample_user_id() -> str:
    """Provide a sample user ID for tests."""
    return "test_user_123"


@pytest.fixture
async def sample_task_data(sample_user_id: str) -> dict:
    """Provide sample task data for tests."""
    return {
        "user_id": sample_user_id,
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
    }


@pytest.fixture
async def create_sample_task(db_pool: asyncpg.Pool, clean_database):
    """Create a sample task in the database."""

    async def _create_task(user_id: str, title: str, description: str = None) -> int:
        async with db_pool.acquire() as connection:
            result = await connection.fetchrow(
                """
                INSERT INTO tasks (user_id, title, description, status, created_at, updated_at)
                VALUES ($1, $2, $3, 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING id;
                """,
                user_id,
                title,
                description,
            )
            return result["id"]

    return _create_task


@pytest.fixture
async def fetch_task(db_pool: asyncpg.Pool):
    """Fetch a task from the database."""

    async def _fetch_task(task_id: int) -> dict:
        async with db_pool.acquire() as connection:
            return await connection.fetchrow(
                "SELECT * FROM tasks WHERE id = $1;",
                task_id,
            )

    return _fetch_task


@pytest.fixture
async def fetch_user_tasks(db_pool: asyncpg.Pool):
    """Fetch all tasks for a user."""

    async def _fetch_user_tasks(user_id: str, status: str = None) -> list:
        async with db_pool.acquire() as connection:
            if status and status != "all":
                return await connection.fetch(
                    "SELECT * FROM tasks WHERE user_id = $1 AND status = $2 ORDER BY created_at DESC;",
                    user_id,
                    status,
                )
            else:
                return await connection.fetch(
                    "SELECT * FROM tasks WHERE user_id = $1 ORDER BY created_at DESC;",
                    user_id,
                )

    return _fetch_user_tasks
