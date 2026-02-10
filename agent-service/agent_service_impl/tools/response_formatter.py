"""Response formatting utilities for tool results.

Converts MCP tool responses into user-friendly messages.
"""

from typing import Any
from enum import Enum


class ResponseType(Enum):
    """Types of agent responses."""

    SUCCESS = "success"
    ERROR = "error"
    CLARIFICATION = "clarification"


class ResponseFormatter:
    """Formats MCP tool responses for user presentation."""

    @staticmethod
    def format_add_task_success(title: str, description: str = None) -> str:
        """Format success response for add_task operation."""
        if description:
            return f"Got it! I've added '{title}' to your tasks (with description)."
        return f"Got it! I've added '{title}' to your tasks."

    @staticmethod
    def format_list_tasks_success(tasks: list[dict], status: str = "all") -> str:
        """Format success response for list_tasks operation."""
        if not tasks:
            status_text = status if status != "all" else ""
            status_text = f" {status}" if status_text else ""
            return f"You have no{status_text} tasks. Great job!"

        status_text = f" {status}" if status != "all" else ""
        lines = [f"You have {len(tasks)}{status_text} task(s):"]
        for i, task in enumerate(tasks, 1):
            title = task.get("title", "Untitled")
            task_id = task.get("id", "?")
            lines.append(f"{i}. {title} (ID: {task_id})")

        return "\n".join(lines)

    @staticmethod
    def format_complete_task_success(title: str) -> str:
        """Format success response for complete_task operation."""
        return f"Great! I've marked '{title}' as done."

    @staticmethod
    def format_update_task_success(title: str, field: str, new_value: str) -> str:
        """Format success response for update_task operation."""
        field_label = "title" if field == "title" else "description"
        return f"Updated! I've changed the {field_label} to '{new_value}'."

    @staticmethod
    def format_delete_task_success(title: str) -> str:
        """Format success response for delete_task operation."""
        return f"Done! I've deleted '{title}' from your tasks."

    @staticmethod
    def format_delete_task_confirmation(title: str) -> str:
        """Format confirmation request for delete_task operation."""
        return (
            f"Are you sure you want to delete '{title}'? "
            f"This can't be undone. Reply 'yes' to confirm or 'no' to cancel."
        )

    @staticmethod
    def format_validation_error(field: str, reason: str, suggestion: str = None) -> str:
        """Format validation error response."""
        msg = f"I couldn't process that because the {field} is {reason}."
        if suggestion:
            msg += f" {suggestion}"
        return msg

    @staticmethod
    def format_not_found_error(entity: str, identifier: str) -> str:
        """Format not found error response."""
        return (
            f"I couldn't find that {entity} ({identifier}). "
            f"Would you like me to show your tasks?"
        )

    @staticmethod
    def format_connection_error() -> str:
        """Format connection/service error response."""
        return (
            "I'm having trouble connecting to the task service. "
            "Could you try again in a moment?"
        )

    @staticmethod
    def format_clarification_request(question: str, options: list[str] = None) -> str:
        """Format clarification request response."""
        msg = f"{question}\n\n"
        if options:
            for i, option in enumerate(options, 1):
                msg += f"{i}. {option}\n"
        return msg.rstrip()

    @staticmethod
    def format_tool_response(
        tool_name: str,
        tool_response: dict[str, Any],
        user_context: dict[str, Any] = None,
    ) -> tuple[ResponseType, str]:
        """Format a tool response based on status and tool type.

        Args:
            tool_name: Name of the tool that was invoked
            tool_response: Response from the tool
            user_context: Additional context (task titles, etc.)

        Returns:
            Tuple of (ResponseType, formatted_message)
        """
        status = tool_response.get("status", "error")
        user_context = user_context or {}

        if status == "success":
            result = tool_response.get("result", {})

            if tool_name == "add_task":
                title = user_context.get("title", result.get("title", ""))
                msg = ResponseFormatter.format_add_task_success(title)
                return ResponseType.SUCCESS, msg

            elif tool_name == "list_tasks":
                tasks = result.get("tasks", [])
                status_filter = user_context.get("status", "all")
                msg = ResponseFormatter.format_list_tasks_success(tasks, status_filter)
                return ResponseType.SUCCESS, msg

            elif tool_name == "complete_task":
                title = user_context.get("title", result.get("title", ""))
                msg = ResponseFormatter.format_complete_task_success(title)
                return ResponseType.SUCCESS, msg

            elif tool_name == "update_task":
                title = user_context.get("title", result.get("title", ""))
                field = user_context.get("field", "")
                new_value = user_context.get("new_value", "")
                msg = ResponseFormatter.format_update_task_success(title, field, new_value)
                return ResponseType.SUCCESS, msg

            elif tool_name == "delete_task":
                title = user_context.get("title", result.get("title", ""))
                msg = ResponseFormatter.format_delete_task_success(title)
                return ResponseType.SUCCESS, msg

            return ResponseType.SUCCESS, "Operation completed successfully."

        elif status == "error":
            error_code = tool_response.get("error_code", "unknown")
            error_msg = tool_response.get("error", "Unknown error")

            if error_code == "validation_error":
                msg = ResponseFormatter.format_validation_error(
                    "input",
                    "is invalid",
                    f"Details: {error_msg}",
                )
                return ResponseType.ERROR, msg

            elif error_code == "not_found":
                entity = "task"
                identifier = user_context.get("task_id", "unknown")
                msg = ResponseFormatter.format_not_found_error(entity, identifier)
                return ResponseType.ERROR, msg

            elif error_code == "invocation_error":
                msg = ResponseFormatter.format_connection_error()
                return ResponseType.ERROR, msg

            else:
                return ResponseType.ERROR, f"Error: {error_msg}"

        return ResponseType.ERROR, "An unexpected error occurred."
