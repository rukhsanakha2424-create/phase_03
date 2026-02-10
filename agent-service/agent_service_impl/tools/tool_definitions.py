"""Tool definitions for OpenAI Agents SDK.

Defines 5 MCP tools for todo task management:
1. add_task - Create a new task
2. list_tasks - List tasks with optional status filter
3. complete_task - Mark a task as completed
4. update_task - Update task title or description
5. delete_task - Delete a task (requires confirmation)
"""

from typing import Any


def get_tool_definitions() -> list[dict[str, Any]]:
    """Get OpenAI SDK tool definitions for all MCP tools.

    Returns:
        List of tool definition dictionaries in OpenAI SDK format.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task with a title and optional description.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Task title (required, max 255 characters)",
                        },
                        "description": {
                            "type": "string",
                            "description": "Task description (optional, max 2000 characters)",
                        },
                    },
                    "required": ["title"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List tasks with optional status filter (pending, completed, or all).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["pending", "completed", "all"],
                            "description": "Filter tasks by status (default: all)",
                        },
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as completed by task ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to complete",
                        },
                    },
                    "required": ["task_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update a task's title and/or description.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to update",
                        },
                        "title": {
                            "type": "string",
                            "description": "New task title (optional, max 255 characters)",
                        },
                        "description": {
                            "type": "string",
                            "description": "New task description (optional, max 2000 characters)",
                        },
                    },
                    "required": ["task_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task by task ID (requires explicit confirmation from user).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to delete",
                        },
                    },
                    "required": ["task_id"],
                },
            },
        },
    ]
