"""update_task MCP tool handler."""

import json

from pydantic import ValidationError

from src.db.connection import DatabasePool
from src.errors.handlers import (
    format_error_response,
    handle_database_error,
    handle_generic_error,
    handle_validation_error,
)
from src.models.schemas import UpdateTaskInput, UpdateTaskOutput


async def handle_update_task(arguments: dict) -> str:
    """Handle update_task tool invocation.

    Updates task title and/or description if the user owns the task.
    Only updates specified fields; leaves other fields unchanged.

    Args:
        arguments: Tool arguments dict with keys: user_id, task_id, title (optional), description (optional)

    Returns:
        JSON string with tool output (task_id, title, status, updated_at) or error

    Database Operation:
        UPDATE tasks SET title = $1, description = $2, updated_at = NOW()
        WHERE id = $3 AND user_id = $4
        RETURNING id, title, status, updated_at
    """
    try:
        # Step 1: Validate inputs using Pydantic schema
        input_data = UpdateTaskInput(**arguments)

        # Step 2: Update task in database with user_id isolation
        pool = DatabasePool.get_pool()

        async with pool.acquire() as connection:
            # Build dynamic UPDATE query based on which fields are provided
            updates = []
            params = []
            param_index = 1

            if input_data.title is not None:
                updates.append(f"title = ${param_index}")
                params.append(input_data.title)
                param_index += 1

            if input_data.description is not None:
                updates.append(f"description = ${param_index}")
                params.append(input_data.description)
                param_index += 1

            # Always update the updated_at timestamp
            updates.append(f"updated_at = CURRENT_TIMESTAMP")

            if not updates:
                # If no fields to update, query without SET clause
                query = f"""
                SELECT id, title, status, updated_at
                FROM tasks
                WHERE id = $1 AND user_id = $2;
                """
                params = [input_data.task_id, input_data.user_id]
            else:
                set_clause = ", ".join(updates)
                # Add WHERE parameters
                params.append(input_data.task_id)
                params.append(input_data.user_id)

                query = f"""
                UPDATE tasks
                SET {set_clause}
                WHERE id = ${param_index} AND user_id = ${param_index + 1}
                RETURNING id, title, status, updated_at;
                """

            row = await connection.fetchrow(query, *params)

            # Check if task was found and belongs to user
            if not row:
                return format_error_response("Task not found or access denied")

        # Step 3: Build response
        output = UpdateTaskOutput(
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
