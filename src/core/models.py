"""Task models for the Todo application."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier (assigned by system)
        description: User-provided task description
        completed: Whether the task is complete (False by default)
    """
    id: int
    description: str
    completed: bool = False

    def to_dict(self):
        """Convert to dictionary (for potential future serialization)."""
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed
        }
