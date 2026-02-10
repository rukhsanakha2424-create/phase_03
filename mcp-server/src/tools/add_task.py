"""add_task MCP tool handler."""

import json
from datetime import datetime

from pydantic import ValidationError

from src.db.connection import DatabasePool
from src.errors.handlers import (
    format_error_response,
    handle_database_error,
    handle_generic_error,
    handle_validation_error,
)
from src.models.schemas import AddTaskInput, AddTaskOutput


async def handle_add_task(arguments: dict) -> str:
    """Handle add_task tool invocation.

    Creates a new task with the given title and optional description.
    All tasks are created with status='pending' by default.

    Args:
        arguments: Tool arguments dict with keys: user_id, title, description (optional)

    Returns:
        JSON string with tool output (task_id, title, status, created_at) or error

    Database Operation:
        INSERT INTO tasks (user_id, title, description, status, created_at, updated_at)
        VALUES ($1, $2, $3, 'pending', NOW(), NOW())
        RETURNING id, title, status, created_at
    """
    try:
        # Step 1: Validate inputs using Pydantic schema
        input_data = AddTaskInput(**arguments)

        # Step 2: Insert task into database with user_id isolation
        pool = DatabasePool.get_pool()

        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                """
                INSERT INTO tasks (user_id, title, description, status, created_at, updated_at)
                VALUES ($1, $2, $3, 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING id, title, status, created_at;
                """,
                input_data.user_id,
                input_data.title,
                input_data.description,
            )

        # Step 3: Build response
        output = AddTaskOutput(
            task_id=row["id"],
            title=row["title"],
            status=row["status"],
            created_at=row["created_at"],
        )

        return output.model_dump_json()

    except ValidationError as e:
        # Handle Pydantic validation errors
        return handle_validation_error(e)
    except Exception as e:
        # Check if this is a database error
        if "asyncpg" in type(e).__module__:
            return handle_database_error(e)
        else:
            return handle_generic_error(e)
