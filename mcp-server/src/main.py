"""MCP Server for Todo Operations - Entry point."""

import asyncio
import logging
import os
import sys
from typing import Any

from mcp.server import Server
from mcp.types import Tool

from src.db.connection import DatabasePool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Initialize MCP server
server = Server("mcp-adapter-todo")


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[dict[str, Any]]:
    """Handle tool calls from the MCP client.

    Args:
        name: Name of the tool to call
        arguments: Tool arguments as a dictionary

    Returns:
        List of result blocks with tool output

    Raises:
        ValueError: If tool not found or validation fails
    """
    logger.info(f"Tool called: {name} with arguments: {arguments}")

    # Import tool handlers (deferred to avoid circular imports)
    if name == "add_task":
        from src.tools.add_task import handle_add_task

        result = await handle_add_task(arguments)
    elif name == "list_tasks":
        from src.tools.list_tasks import handle_list_tasks

        result = await handle_list_tasks(arguments)
    elif name == "update_task":
        from src.tools.update_task import handle_update_task

        result = await handle_update_task(arguments)
    elif name == "complete_task":
        from src.tools.complete_task import handle_complete_task

        result = await handle_complete_task(arguments)
    elif name == "delete_task":
        from src.tools.delete_task import handle_delete_task

        result = await handle_delete_task(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

    # Result should be a JSON string from the tool handler
    return [{"type": "text", "text": result}]


async def setup_tools() -> None:
    """Register all MCP tools with the server."""
    tools: list[Tool] = [
        Tool(
            name="add_task",
            description="Create a new task with title and optional description",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "Unique identifier of the user",
                    },
                    "title": {
                        "type": "string",
                        "description": "Task title (max 255 characters)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description",
                    },
                },
                "required": ["user_id", "title"],
            },
        ),
        Tool(
            name="list_tasks",
            description="Retrieve user's tasks with optional status filter",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "Unique identifier of the user",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter by status (default: all)",
                    },
                },
                "required": ["user_id"],
            },
        ),
        Tool(
            name="update_task",
            description="Update a task's title and/or description",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "Unique identifier of the user",
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to update",
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (max 255 characters)",
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description",
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "Unique identifier of the user",
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to complete",
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
        Tool(
            name="delete_task",
            description="Delete a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "Unique identifier of the user",
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to delete",
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
    ]

    for tool in tools:
        server.add_tool(tool)

    logger.info(f"Registered {len(tools)} tools: add_task, list_tasks, update_task, complete_task, delete_task")


async def main() -> None:
    """Main entry point for the MCP server."""
    try:
        print("MCP Adapter Server starting...")

        # Initialize database connection pool
        await DatabasePool.initialize()

        # Register tools with the MCP server
        await setup_tools()

        print("MCP server listening on stdio")
        print("Tools registered: add_task, list_tasks, update_task, complete_task, delete_task")
        print("Ready for agent connections")

        # Run the MCP server
        async with server:
            await server.wait_for_shutdown()

    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # Clean up database connections
        await DatabasePool.close()


if __name__ == "__main__":
    asyncio.run(main())
