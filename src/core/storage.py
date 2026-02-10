"""In-memory storage for tasks.

This module provides pure in-memory task storage.
Data is NOT persisted - it resets when the application restarts.
"""

from typing import Dict, List, Optional
from src.core.models import Task


class InMemoryStorage:
    """Pure in-memory task storage.

    All data is lost when the application restarts.
    This is intentional per Phase-I spec (no persistence).
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}

    def get_all(self) -> List[Task]:
        """Return all tasks."""
        return list(self._tasks.values())

    def get(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return self._tasks.get(task_id)

    def save(self, task: Task) -> None:
        """Save or update a task."""
        self._tasks[task.id] = task

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted, False if not found."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def clear(self) -> None:
        """Clear all tasks (for testing)."""
        self._tasks.clear()

    def count(self) -> int:
        """Return the number of tasks."""
        return len(self._tasks)
