"""complete_task MCP tool handler."""

import json

from pydantic import ValidationError

from src.db.connection import DatabasePool
from src.errors.handlers import (
    format_error_response,
    handle_database_error,
    handle_generic_error,
    handle_validation_error,
)
from src.models.schemas import CompleteTaskInput, CompleteTaskOutput


async def handle_complete_task(arguments: dict) -> str:
    """Handle complete_task tool invocation.

    Marks a task as completed. This operation is idempotent - marking an already-
    completed task returns success without error.

    Args:
        arguments: Tool arguments dict with keys: user_id, task_id

    Returns:
        JSON string with tool output (task_id, title, status, updated_at) or error

    Database Operation:
        UPDATE tasks SET status = 'completed', updated_at = NOW()
        WHERE id = $1 AND user_id = $2
        RETURNING id, title, status, updated_at
    """
    try:
        # Step 1: Validate inputs using Pydantic schema
        input_data = CompleteTaskInput(**arguments)

        # Step 2: Update task status in database with user_id isolation
        pool = DatabasePool.get_pool()

        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                """
                UPDATE tasks
                SET status = 'completed', updated_at = CURRENT_TIMESTAMP
                WHERE id = $1 AND user_id = $2
                RETURNING id, title, status, updated_at;
                """,
                input_data.task_id,
                input_data.user_id,
            )

            # Check if task was found and belongs to user
            if not row:
                return format_error_response("Task not found or access denied")

        # Step 3: Build response
        output = CompleteTaskOutput(
            id=row["id"],
            title=row["title"],
            status=row["status"],
            updated_at=row["updated_at"],
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
