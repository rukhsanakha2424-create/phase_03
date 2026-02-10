"""Status filter inference for list_tasks operations.

Infers user's intended status filter from natural language messages.
Returns "pending", "completed", or "all" (default).
"""

import re
from typing import NamedTuple, Literal


class StatusFilterResult(NamedTuple):
    """Result of status filter inference."""

    status: Literal["all", "pending", "completed"]
    confidence: float  # 0.0 to 1.0
    reasoning: str  # Explanation of inference


def infer_status_filter(message: str) -> StatusFilterResult:
    """Infer status filter from user message.

    Args:
        message: User message (e.g., "Show my pending tasks")

    Returns:
        StatusFilterResult with inferred status

    Example:
        >>> result = infer_status_filter("Show my pending tasks")
        >>> result.status
        'pending'
        >>> result.confidence
        0.95
    """
    message_lower = message.lower().strip()

    # Pending/todo patterns
    pending_patterns = [
        (r"\b(pending|todo|to\s+do|not\s+done|remaining|outstanding)\b", 0.95),
        (r"\bwhat.{0,15}(?:left|todo|pending)\b", 0.90),
        (r"\bwhat.{0,10}do.{0,10}(?:need|have)\b", 0.85),
        (r"\bunfinished\b", 0.90),
    ]

    for pattern, conf in pending_patterns:
        if re.search(pattern, message_lower):
            return StatusFilterResult(
                status="pending",
                confidence=conf,
                reasoning=f"Matched pending pattern: {pattern}",
            )

    # Completed/done patterns
    completed_patterns = [
        (r"\b(completed|done|finished|closed)\b", 0.95),
        (r"\b(finished|complete)\s+(tasks|todos)\b", 0.98),
        (r"\bwhat.{0,15}(?:done|finished|completed)\b", 0.90),
        (r"\bwhat.{0,10}(have|i).{0,10}(?:done|finished)\b", 0.85),
    ]

    for pattern, conf in completed_patterns:
        if re.search(pattern, message_lower):
            return StatusFilterResult(
                status="completed",
                confidence=conf,
                reasoning=f"Matched completed pattern: {pattern}",
            )

    # All/no filter patterns
    if re.search(r"\b(all|everything|my\s+tasks)\b", message_lower):
        return StatusFilterResult(
            status="all",
            confidence=0.90,
            reasoning="Explicit 'all' or 'everything' request",
        )

    # Default to all if no filter specified
    return StatusFilterResult(
        status="all",
        confidence=0.70,
        reasoning="No specific status filter found, defaulting to all",
    )
