"""Error handling utilities for MCP Adapter."""

import json
from typing import Any, Dict

from pydantic import ValidationError


def format_error_response(error_message: str) -> str:
    """Format an error message as a structured JSON response.

    Args:
        error_message: The error message to format

    Returns:
        JSON string with error field

    Example:
        >>> format_error_response("Title is required")
        '{"error": "Title is required"}'
    """
    error_dict: Dict[str, Any] = {"error": error_message}
    return json.dumps(error_dict)


def extract_validation_error(validation_error: ValidationError) -> str:
    """Extract the first validation error message from a Pydantic ValidationError.

    Args:
        validation_error: The Pydantic ValidationError to extract from

    Returns:
        The first error message, or a generic message if extraction fails

    Example:
        >>> try:
        ...     AddTaskInput(user_id="", title="Test")
        ... except ValidationError as e:
        ...     msg = extract_validation_error(e)
        ...     print(msg)
        user_id is required
    """
    if validation_error.errors():
        error_dict = validation_error.errors()[0]
        # Try to get custom message from validator
        if "ctx" in error_dict and "error" in error_dict["ctx"]:
            return str(error_dict["ctx"]["error"])
        # Try to get message from validation error
        if "msg" in error_dict:
            return error_dict["msg"]
    return "Invalid input parameters"


def handle_validation_error(validation_error: ValidationError) -> str:
    """Handle a Pydantic validation error and return formatted response.

    Args:
        validation_error: The ValidationError to handle

    Returns:
        Formatted JSON error response string
    """
    error_message = extract_validation_error(validation_error)
    return format_error_response(error_message)


def handle_database_error(error: Exception) -> str:
    """Handle a database error and return formatted response.

    Args:
        error: The database exception

    Returns:
        Formatted JSON error response string
    """
    error_type = type(error).__name__

    # Handle specific error types
    if "unique" in error_type.lower() or "constraint" in error_type.lower():
        return format_error_response("Task already exists or constraint violation")
    elif "connection" in error_type.lower() or "timeout" in error_type.lower():
        return format_error_response("Database connection failed")
    else:
        return format_error_response(f"Database error: {str(error)}")


def handle_generic_error(error: Exception) -> str:
    """Handle a generic error and return formatted response.

    Args:
        error: The exception to handle

    Returns:
        Formatted JSON error response string
    """
    error_message = str(error) or "An unexpected error occurred"
    return format_error_response(error_message)
