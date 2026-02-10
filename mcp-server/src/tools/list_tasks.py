"""list_tasks MCP tool handler."""

import json

from pydantic import ValidationError

from src.db.connection import DatabasePool
from src.errors.handlers import (
    format_error_response,
    handle_database_error,
    handle_generic_error,
    handle_validation_error,
)
from src.models.schemas import ListTasksInput, ListTasksOutput


async def handle_list_tasks(arguments: dict) -> str:
    """Handle list_tasks tool invocation.

    Returns all tasks owned by the user, optionally filtered by status.
    Default status filter is 'all' (no filtering by status).

    Args:
        arguments: Tool arguments dict with keys: user_id, status (optional)

    Returns:
        JSON string with tool output (array of tasks) or error

    Database Operation:
        SELECT id, title, description, status, created_at, updated_at
        FROM tasks
        WHERE user_id = $1 [AND status = $2 if status filter provided]
        ORDER BY created_at DESC
    """
    try:
        # Step 1: Validate inputs using Pydantic schema
        input_data = ListTasksInput(**arguments)

        # Step 2: Query tasks from database with user_id isolation
        pool = DatabasePool.get_pool()

        async with pool.acquire() as connection:
            # Build dynamic query based on status filter
            if input_data.status and input_data.status != "all":
                query = """
                SELECT id, title, description, status, created_at, updated_at
                FROM tasks
                WHERE user_id = $1 AND status = $2
                ORDER BY created_at DESC;
                """
                rows = await connection.fetch(query, input_data.user_id, input_data.status)
            else:
                query = """
                SELECT id, title, description, status, created_at, updated_at
                FROM tasks
                WHERE user_id = $1
                ORDER BY created_at DESC;
                """
                rows = await connection.fetch(query, input_data.user_id)

        # Step 3: Build response
        tasks = []
        for row in rows:
            task_dict = {
                "id": row["id"],
                "user_id": input_data.user_id,  # Include user_id in response
                "title": row["title"],
                "description": row["description"],
                "status": row["status"],
                "created_at": row["created_at"].isoformat() if hasattr(row["created_at"], "isoformat") else str(row["created_at"]),
                "updated_at": row["updated_at"].isoformat() if hasattr(row["updated_at"], "isoformat") else str(row["updated_at"]),
            }
            tasks.append(task_dict)

        output = ListTasksOutput(tasks=tasks)
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
