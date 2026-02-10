"""delete_task MCP tool handler."""

import json

from pydantic import ValidationError

from src.db.connection import DatabasePool
from src.errors.handlers import (
    format_error_response,
    handle_database_error,
    handle_generic_error,
    handle_validation_error,
)
from src.models.schemas import DeleteTaskInput, DeleteTaskOutput


async def handle_delete_task(arguments: dict) -> str:
    """Handle delete_task tool invocation.

    Deletes a task owned by the user. This operation is NOT idempotent - attempting
    to delete a non-existent task returns an error.

    Args:
        arguments: Tool arguments dict with keys: user_id, task_id

    Returns:
        JSON string with tool output (task_id, status) or error

    Database Operation:
        DELETE FROM tasks
        WHERE id = $1 AND user_id = $2
        RETURNING id
    """
    try:
        # Step 1: Validate inputs using Pydantic schema
        input_data = DeleteTaskInput(**arguments)

        # Step 2: Delete task from database with user_id isolation
        pool = DatabasePool.get_pool()

        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                """
                DELETE FROM tasks
                WHERE id = $1 AND user_id = $2
                RETURNING id;
                """,
                input_data.task_id,
                input_data.user_id,
            )

            # Check if task was found and belongs to user
            if not row:
                return format_error_response("Task not found or access denied")

        # Step 3: Build response
        output = DeleteTaskOutput(
            id=row["id"],
            status="deleted",
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
