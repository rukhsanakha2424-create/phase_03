"""Parameter extraction from natural language messages.

Extracts tool parameters from user messages:
- add_task: title (required), description (optional)
- list_tasks: status (pending/completed/all)
- complete_task: task_id
- update_task: task_id, title or description
- delete_task: task_id
"""

import re
from typing import Any, Optional, NamedTuple


class ParameterExtractionResult(NamedTuple):
    """Result of parameter extraction."""

    parameters: dict[str, Any]
    missing: list[str]  # Required parameters not found
    confidence: float  # 0.0 to 1.0 confidence in extraction


def extract_add_task_params(message: str) -> ParameterExtractionResult:
    """Extract parameters for add_task from user message.

    Extracts:
    - title (required): Task title, max 255 characters
    - description (optional): Task description, max 2000 characters

    Args:
        message: User message (e.g., "Add task: Buy groceries")

    Returns:
        ParameterExtractionResult with extracted parameters

    Example:
        >>> result = extract_add_task_params("Add task: Buy milk")
        >>> result.parameters['title']
        'Buy milk'
        >>> result.missing
        []
    """
    params = {}
    confidence = 0.9

    # Try to extract title from common patterns
    patterns = [
        # "Add task: <title>" or "Create: <title>" with colon
        r"(?:add|create|new)\s*:?\s+(?:task|a\s+task|todo|a\s+todo)?\s*:?\s+(.+?)(?:\.|$)",
        # Handle "Add: <title>" or "Create: <title>"
        r"^(?:add|create|new)\s*:\s+(.+?)(?:\.|$)",
        # "task: <title>" or "todo: <title>"
        r"^(?:task|todo)\s*:?\s+(.+?)(?:\.|$)",
        # "Remind me to <action>"
        r"(?:remind|remind\s+me\s+to|don't\s+forget\s+to)\s+(.+?)(?:\.|$)",
        # "I need to <action>" or "I should <action>"
        r"^i\s+(?:need|should)\s+(?:to\s+)?(.+?)(?:\.|$)",
        # Simple "add <title>" without task keyword - very common pattern
        r"^(?:add|create)\s+(?!task|todo|a\s+task|a\s+todo)(.+?)(?:\.|$)",
        # Last resort: everything after first keyword
        r"(?:add|create|new|task|todo)\s+(.+?)(?:\.|$)",
    ]

    title = None
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            title = title.rstrip(".!?")
            if title and len(title) > 3:  # Must be at least 4 chars
                confidence = 0.95
                break

    if title:
        params["title"] = title[:255]  # Enforce max length
    else:
        confidence = 0.5

    # Try to extract description (optional, after description markers)
    description_patterns = [
        r"(?:with\s+description|description:?)\s+(.+?)(?:\.|$)",
        r"(?:details?:?)\s+(.+?)(?:\.|$)",
    ]

    description = None
    for pattern in description_patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            description = match.group(1).strip()
            description = description.rstrip(".!?")
            if description:
                params["description"] = description[:2000]  # Enforce max length
                confidence = 0.95
                break

    # Determine missing required parameters
    missing = []
    if "title" not in params:
        missing.append("title")
        confidence = 0.3

    return ParameterExtractionResult(
        parameters=params,
        missing=missing,
        confidence=confidence,
    )


def extract_list_tasks_params(message: str) -> ParameterExtractionResult:
    """Extract parameters for list_tasks from user message.

    Extracts:
    - status (optional): "pending", "completed", or "all" (default)

    Args:
        message: User message (e.g., "Show my pending tasks")

    Returns:
        ParameterExtractionResult with extracted parameters
    """
    params = {}
    confidence = 0.95

    # Default status is "all"
    status = "all"

    # Check for pending/todo status
    if re.search(r"\b(pending|todo|to\s+do|not\s+done|remaining)\b", message, re.IGNORECASE):
        status = "pending"
    # Check for completed/done status
    elif re.search(r"\b(completed|done|finished|closed)\b", message, re.IGNORECASE):
        status = "completed"
    # Explicit "all" request
    elif re.search(r"\b(all|everything)\b", message, re.IGNORECASE):
        status = "all"

    params["status"] = status

    return ParameterExtractionResult(
        parameters=params,
        missing=[],
        confidence=confidence,
    )


def extract_complete_task_params(message: str) -> ParameterExtractionResult:
    """Extract parameters for complete_task from user message.

    Extracts:
    - task_id (required): Task ID or name

    Args:
        message: User message (e.g., "Mark task 5 as done")

    Returns:
        ParameterExtractionResult with extracted parameters
    """
    params = {}
    confidence = 0.8
    missing = []

    # Try to extract numeric task ID
    match = re.search(r"(?:task\s+)?#?(\d+)", message, re.IGNORECASE)
    if match:
        params["task_id"] = match.group(1)
        confidence = 0.95
    else:
        # Try to extract task name
        patterns = [
            r"(?:mark|complete|finish|done\s+with)\s+(?:task\s+)?(?:the\s+)?['\"]?([^'\"]+)['\"]?(?:\s+as\s+done)?",
            r"(?:done\s+with|finished\s+with)\s+(?:the\s+)?['\"]?([^'\"]+)['\"]?",
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                task_id = match.group(1).strip().rstrip(".!?")
                if task_id and len(task_id) > 1:
                    params["task_id"] = task_id
                    confidence = 0.85
                    break

    if "task_id" not in params:
        missing.append("task_id")
        confidence = 0.3

    return ParameterExtractionResult(
        parameters=params,
        missing=missing,
        confidence=confidence,
    )


def extract_update_task_params(message: str) -> ParameterExtractionResult:
    """Extract parameters for update_task from user message.

    Extracts:
    - task_id (required)
    - title (optional)
    - description (optional)

    Args:
        message: User message (e.g., "Update task 3 to 'Buy milk'")

    Returns:
        ParameterExtractionResult with extracted parameters
    """
    params = {}
    confidence = 0.85
    missing = []

    # Extract task ID
    match = re.search(r"(?:task\s+)?#?(\d+)", message, re.IGNORECASE)
    if match:
        params["task_id"] = match.group(1)
    else:
        missing.append("task_id")
        confidence = 0.3

    # Extract new title
    patterns = [
        r"(?:to|:)\s+['\"]?([^'\"]+)['\"]?(?:\.|$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            new_value = match.group(1).strip()
            if new_value and len(new_value) > 2:
                params["title"] = new_value
                confidence = 0.9
                break

    return ParameterExtractionResult(
        parameters=params,
        missing=missing,
        confidence=confidence,
    )


def extract_delete_task_params(message: str) -> ParameterExtractionResult:
    """Extract parameters for delete_task from user message.

    Extracts:
    - task_id (required)

    Args:
        message: User message (e.g., "Delete task 2")

    Returns:
        ParameterExtractionResult with extracted parameters
    """
    params = {}
    confidence = 0.85
    missing = []

    # Extract numeric task ID
    match = re.search(r"(?:task\s+)?#?(\d+)", message, re.IGNORECASE)
    if match:
        params["task_id"] = match.group(1)
        confidence = 0.95
    else:
        # Try to extract task name
        patterns = [
            r"(?:delete|remove|get\s+rid\s+of)\s+(?:task\s+)?['\"]?([^'\"]+)['\"]?(?:\.|$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                task_id = match.group(1).strip().rstrip(".!?")
                if task_id and len(task_id) > 1:
                    params["task_id"] = task_id
                    confidence = 0.80
                    break

    if "task_id" not in params:
        missing.append("task_id")
        confidence = 0.3

    return ParameterExtractionResult(
        parameters=params,
        missing=missing,
        confidence=confidence,
    )
