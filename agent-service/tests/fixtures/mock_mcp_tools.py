"""Mock MCP tool responses for testing.

Provides mock responses that simulate MCP tool behavior for various scenarios:
- Happy path (successful operations)
- Error scenarios (validation, not found, connection errors)
"""

from typing import Any, Callable, Optional
import json


class MockMCPTools:
    """Mock implementations of MCP tools for testing."""

    # Mock task data for testing
    MOCK_TASKS = [
        {
            "id": "1",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "status": "pending",
        },
        {
            "id": "2",
            "title": "Fix login bug",
            "description": "Users can't reset passwords",
            "status": "pending",
        },
        {
            "id": "3",
            "title": "Review PR #42",
            "description": None,
            "status": "completed",
        },
    ]

    @staticmethod
    def mock_add_task_success(
        title: str, description: Optional[str] = None, task_id: str = "4"
    ) -> dict[str, Any]:
        """Mock successful add_task response."""
        return {
            "status": "success",
            "result": {
                "id": task_id,
                "title": title,
                "description": description,
                "status": "pending",
                "created_at": "2026-02-02T10:00:00Z",
            },
        }

    @staticmethod
    def mock_add_task_validation_error(reason: str) -> dict[str, Any]:
        """Mock add_task validation error."""
        return {
            "status": "error",
            "error_code": "validation_error",
            "error": f"Title validation failed: {reason}",
        }

    @staticmethod
    def mock_list_tasks_success(
        status: str = "all", count: int = 3
    ) -> dict[str, Any]:
        """Mock successful list_tasks response."""
        tasks = MockMCPTools.MOCK_TASKS

        if status == "pending":
            tasks = [t for t in tasks if t["status"] == "pending"]
        elif status == "completed":
            tasks = [t for t in tasks if t["status"] == "completed"]

        return {
            "status": "success",
            "result": {
                "tasks": tasks[:count],
                "total": len(tasks),
                "status_filter": status,
            },
        }

    @staticmethod
    def mock_list_tasks_empty() -> dict[str, Any]:
        """Mock list_tasks with no results."""
        return {
            "status": "success",
            "result": {
                "tasks": [],
                "total": 0,
                "status_filter": "all",
            },
        }

    @staticmethod
    def mock_complete_task_success(task_id: str) -> dict[str, Any]:
        """Mock successful complete_task response."""
        return {
            "status": "success",
            "result": {
                "id": task_id,
                "title": "Buy groceries",
                "status": "completed",
                "completed_at": "2026-02-02T10:05:00Z",
            },
        }

    @staticmethod
    def mock_complete_task_not_found(task_id: str) -> dict[str, Any]:
        """Mock complete_task with task not found."""
        return {
            "status": "error",
            "error_code": "not_found",
            "error": f"Task {task_id} not found",
        }

    @staticmethod
    def mock_update_task_success(
        task_id: str, title: Optional[str] = None, description: Optional[str] = None
    ) -> dict[str, Any]:
        """Mock successful update_task response."""
        return {
            "status": "success",
            "result": {
                "id": task_id,
                "title": title or "Updated task",
                "description": description,
                "status": "pending",
                "updated_at": "2026-02-02T10:10:00Z",
            },
        }

    @staticmethod
    def mock_update_task_not_found(task_id: str) -> dict[str, Any]:
        """Mock update_task with task not found."""
        return {
            "status": "error",
            "error_code": "not_found",
            "error": f"Task {task_id} not found",
        }

    @staticmethod
    def mock_delete_task_success(task_id: str) -> dict[str, Any]:
        """Mock successful delete_task response."""
        return {
            "status": "success",
            "result": {
                "id": task_id,
                "deleted_at": "2026-02-02T10:15:00Z",
                "message": "Task deleted successfully",
            },
        }

    @staticmethod
    def mock_delete_task_not_found(task_id: str) -> dict[str, Any]:
        """Mock delete_task with task not found."""
        return {
            "status": "error",
            "error_code": "not_found",
            "error": f"Task {task_id} not found",
        }

    @staticmethod
    def mock_connection_error() -> dict[str, Any]:
        """Mock connection/invocation error."""
        return {
            "status": "error",
            "error_code": "invocation_error",
            "error": "Failed to connect to MCP server",
        }

    @staticmethod
    def mock_timeout_error() -> dict[str, Any]:
        """Mock timeout error."""
        return {
            "status": "error",
            "error_code": "timeout",
            "error": "Request timed out after 30 seconds",
        }


def create_mock_tool_invoker(
    responses: dict[str, Callable[..., dict[str, Any]]]
) -> Callable:
    """Create a mock tool invoker that returns predefined responses.

    Args:
        responses: Dictionary mapping tool names to response generators

    Returns:
        Mock invoker function
    """

    def mock_invoke(tool_name: str, arguments: dict[str, Any], **kwargs) -> dict[str, Any]:
        if tool_name in responses:
            response_fn = responses[tool_name]
            if callable(response_fn):
                return response_fn(**arguments)
            return response_fn
        return {
            "status": "error",
            "error_code": "unknown_tool",
            "error": f"Unknown tool: {tool_name}",
        }

    return mock_invoke
