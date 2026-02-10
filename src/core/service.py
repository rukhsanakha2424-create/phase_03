"""Task service for CRUD operations.

Provides pure in-memory task management.
Data resets on application restart per Phase-I spec.
"""

from typing import List, Optional
from src.core.models import Task
from src.core.storage import InMemoryStorage
from src.utils.id_gen import IDGenerator


class TaskService:
    """Service for managing tasks in memory.

    All operations work on in-memory data only.
    No file I/O, no persistence, data resets on restart.
    """

    def __init__(self, storage: Optional[InMemoryStorage] = None):
        self._storage = storage or InMemoryStorage()
        self._id_gen = IDGenerator()
        # Advance ID generator past highest existing ID
        tasks = self._storage.get_all()
        if tasks:
            max_id = max(t.id for t in tasks)
            for _ in range(max_id):
                self._id_gen.next_id()

    def add(self, description: str) -> Task:
        """Add a new task.

        Args:
            description: The task description

        Returns:
            The created Task

        Raises:
            ValueError: If description is empty
        """
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")

        task_id = self._id_gen.next_id()
        task = Task(id=task_id, description=description.strip(), completed=False)
        self._storage.save(task)
        return task

    def list(self) -> List[Task]:
        """List all tasks.

        Returns:
            List of all tasks (unsorted)
        """
        return self._storage.get_all()

    def get(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: The task ID

        Returns:
            Task if found, None otherwise
        """
        return self._storage.get(task_id)

    def update(self, task_id: int, description: str) -> Task:
        """Update a task's description.

        Args:
            task_id: The task ID
            description: The new description

        Returns:
            The updated Task

        Raises:
            KeyError: If task not found
            ValueError: If description is empty
        """
        task = self._storage.get(task_id)
        if task is None:
            raise KeyError(f"Task {task_id} not found")

        if not description or not description.strip():
            raise ValueError("Description cannot be empty")

        task.description = description.strip()
        self._storage.save(task)
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: The task ID

        Returns:
            True if deleted, False if not found
        """
        return self._storage.delete(task_id)

    def complete(self, task_id: int) -> Task:
        """Toggle task completion status.

        Args:
            task_id: The task ID

        Returns:
            The updated Task

        Raises:
            KeyError: If task not found
        """
        task = self._storage.get(task_id)
        if task is None:
            raise KeyError(f"Task {task_id} not found")

        task.completed = not task.completed
        self._storage.save(task)
        return task

    def count(self) -> int:
        """Return the number of tasks."""
        return self._storage.count()
