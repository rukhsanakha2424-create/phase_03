"""Intent classification handler for user messages.

Identifies user intent and classifies messages into tool types:
- add_task (create, new task)
- list_tasks (list, show, view)
- complete_task (complete, done, finish)
- update_task (update, change, edit)
- delete_task (delete, remove)
"""

import re
from enum import Enum
from typing import NamedTuple


class Intent(Enum):
    """User intent types."""

    ADD_TASK = "add_task"
    LIST_TASKS = "list_tasks"
    COMPLETE_TASK = "complete_task"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"
    GREETING = "greeting"
    HELP = "help"
    CLARIFICATION_NEEDED = "clarification_needed"
    UNKNOWN = "unknown"


class IntentResult(NamedTuple):
    """Result of intent classification."""

    intent: Intent
    confidence: float  # 0.0 to 1.0
    reasoning: str  # Explanation of classification


def classify_intent(message: str) -> IntentResult:
    """Classify user message intent.

    Uses pattern matching to identify the user's intent and returns
    a classification with confidence score and reasoning.

    Args:
        message: User input message

    Returns:
        IntentResult with intent, confidence, and reasoning

    Example:
        >>> result = classify_intent("Add task: Buy groceries")
        >>> result.intent
        <Intent.ADD_TASK: 'add_task'>
        >>> result.confidence
        0.98
    """
    message_lower = message.lower().strip()

    # Add task patterns - high confidence
    add_patterns = [
        (r"^(add|create|new)\s+.*(task|todo)", 0.98),  # add/create/new ... task
        (r"^(add|create)\s*:", 0.95),
        (r"^(add|create)\s+\w", 0.90),  # add <something>
        (r"^(task|todo)\s*:", 0.90),
        (r"^(remind|remind\s+me|don't\s+forget)\s+(to|me\s+to)", 0.95),
        (r"\bi\s+need\s+to\b", 0.85),
        (r"^new\s+\w", 0.85),  # new <something>
        # More flexible patterns
        (r"^add\b", 0.85),  # just "add" at start
        (r"^create\b", 0.85),  # just "create" at start
        (r"^(make|set)\s+(a\s+)?(task|todo|reminder)", 0.90),
        (r"^(put|write)\s+.*(list|task|todo)", 0.85),
    ]

    for pattern, conf in add_patterns:
        if re.search(pattern, message_lower):
            return IntentResult(
                intent=Intent.ADD_TASK,
                confidence=conf,
                reasoning=f"Matched add_task pattern: {pattern}",
            )

    # List tasks patterns
    list_patterns = [
        (r"^(list|show|view|see|display)\s+.*(tasks|todos)", 0.98),  # show/list ...tasks
        (r"^(what\s+are|what's)\s+.*(tasks|todos)", 0.95),
        (r"^(show|list)\s+(pending|completed)", 0.98),
        (r"^(what\s+do\s+i\s+have\s+to\s+do|what's\s+left)", 0.90),
        (r"^(list|show)\s*$", 0.75),
        (r"^(display|list)\s+.*tasks", 0.90),
        # More flexible patterns
        (r"^(my\s+)?tasks\s*$", 0.85),  # "tasks" or "my tasks"
        (r"^(my\s+)?todos?\s*$", 0.85),  # "todo" or "my todo"
        (r"^(show|see|view|list)\s+(my\s+)?(tasks|todos?|list)", 0.95),
        (r"^what.*tasks", 0.90),  # "what tasks do I have"
        (r"^(pending|completed)\s+tasks", 0.90),  # "pending tasks"
        (r"^(show|list|view)\s*(me\s+)?(everything|all)", 0.85),
        (r"^all\s+tasks", 0.90),
        (r"^what\s+(should|do)\s+i\s+(do|have)", 0.85),
    ]

    for pattern, conf in list_patterns:
        if re.search(pattern, message_lower):
            return IntentResult(
                intent=Intent.LIST_TASKS,
                confidence=conf,
                reasoning=f"Matched list_tasks pattern: {pattern}",
            )

    # Complete task patterns
    complete_patterns = [
        (r"^(mark|complete|finish)\s+.*(task|it)", 0.98),  # mark task 5
        (r"^(mark|complete)\s+['\"]", 0.95),  # mark "task name"
        (r"^(check\s+off|done\s+with)", 0.95),
        (r"^(done|finished|completed)\s+with", 0.90),
        # More flexible patterns
        (r"^(complete|finish|done)\s+\d+", 0.95),  # "complete 1"
        (r"^(mark|check)\s+\d+", 0.90),  # "mark 1"
        (r"^(i\s+)?(finished|completed|done)\s+\d+", 0.90),  # "finished 1"
        (r"^task\s+\d+\s+(is\s+)?(done|complete|finished)", 0.90),  # "task 1 done"
        (r"^\d+\s+(is\s+)?(done|complete|finished)", 0.85),  # "1 done"
        (r"^(i\s+)?(did|finished|completed)\s+.*(task|it)", 0.85),
    ]

    for pattern, conf in complete_patterns:
        if re.search(pattern, message_lower):
            return IntentResult(
                intent=Intent.COMPLETE_TASK,
                confidence=conf,
                reasoning=f"Matched complete_task pattern: {pattern}",
            )

    # Update task patterns
    update_patterns = [
        (r"^(update|change|edit|modify)\s+(task|it)", 0.98),
        (r"^(update|change|edit)\s*:", 0.95),
        (r"^(rename|update)\s+(task|it)\s+to", 0.95),
        # More flexible patterns
        (r"^(update|change|edit|modify)\s+\d+", 0.90),  # "update 1"
        (r"^(rename|change)\s+.+\s+to\s+", 0.90),  # "rename X to Y"
    ]

    for pattern, conf in update_patterns:
        if re.search(pattern, message_lower):
            return IntentResult(
                intent=Intent.UPDATE_TASK,
                confidence=conf,
                reasoning=f"Matched update_task pattern: {pattern}",
            )

    # Delete task patterns
    delete_patterns = [
        (r"^(delete|remove|get\s+rid\s+of)\s+.*(task|it)", 0.98),
        (r"^(delete|remove)\s+['\"]", 0.95),  # delete "task name"
        (r"^(delete|remove)\s*:", 0.95),
        (r"^(discard)\s+(task|it)", 0.90),
        # More flexible patterns
        (r"^(delete|remove)\s+\d+", 0.95),  # "delete 1"
        (r"^(cancel|clear)\s+(task\s+)?\d+", 0.85),
    ]

    for pattern, conf in delete_patterns:
        if re.search(pattern, message_lower):
            return IntentResult(
                intent=Intent.DELETE_TASK,
                confidence=conf,
                reasoning=f"Matched delete_task pattern: {pattern}",
            )

    # Greeting patterns
    greeting_patterns = [
        (r"^(hi|hello|hey|hiya|howdy)\s*$", 0.98),
        (r"^(hi|hello|hey)\s+(there|taskie|bot|assistant)", 0.98),
        (r"^good\s+(morning|afternoon|evening|day)", 0.95),
        (r"^(what'?s\s+up|sup|yo)\s*$", 0.90),
        (r"^(greetings|salutations)", 0.95),
        (r"^(hi|hello|hey)\s*[!.,]*\s*$", 0.95),
    ]

    for pattern, conf in greeting_patterns:
        if re.search(pattern, message_lower):
            return IntentResult(
                intent=Intent.GREETING,
                confidence=conf,
                reasoning=f"Matched greeting pattern: {pattern}",
            )

    # Help patterns
    help_patterns = [
        (r"^(help|help\s+me)\s*$", 0.98),
        (r"^what\s+can\s+you\s+do", 0.95),
        (r"^how\s+(do\s+i|does\s+this|can\s+i)", 0.90),
        (r"^(what|who)\s+are\s+you", 0.90),
        (r"^(commands|options|features)", 0.85),
    ]

    for pattern, conf in help_patterns:
        if re.search(pattern, message_lower):
            return IntentResult(
                intent=Intent.HELP,
                confidence=conf,
                reasoning=f"Matched help pattern: {pattern}",
            )

    # Unknown intent
    return IntentResult(
        intent=Intent.UNKNOWN,
        confidence=0.0,
        reasoning="No recognized intent pattern matched",
    )
