"""Task SQLModel definition for MCP Adapter."""

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    """Task entity representing a todo item owned by a user.

    Attributes:
        id: Unique task identifier (auto-generated)
        user_id: User who owns this task (foreign key to auth system)
        title: Task title (required, max 255 characters)
        description: Optional task description
        status: Task status (enum: "pending" or "completed")
        created_at: Timestamp of task creation
        updated_at: Timestamp of last modification
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Indexed for user-scoped queries
    title: str = Field(max_length=255)
    description: Optional[str] = None
    status: str = Field(default="pending")  # "pending" or "completed"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """SQLModel configuration."""

        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "user123",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "status": "pending",
                "created_at": "2026-02-01T12:00:00",
                "updated_at": "2026-02-01T12:00:00",
            }
        }
