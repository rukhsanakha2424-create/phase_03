"""Pydantic schemas for MCP tool inputs and outputs."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# add_task Tool Schemas
# ============================================================================


class AddTaskInput(BaseModel):
    """Input schema for add_task tool."""

    user_id: str = Field(..., description="Unique user identifier")
    title: str = Field(..., max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Optional task description")

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        """Validate user_id is not empty."""
        if not v or not v.strip():
            raise ValueError("user_id is required")
        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title is not empty."""
        if not v or not v.strip():
            raise ValueError("Title is required")
        return v


class AddTaskOutput(BaseModel):
    """Output schema for add_task tool."""

    task_id: int
    title: str
    status: str = "pending"
    created_at: datetime


# ============================================================================
# list_tasks Tool Schemas
# ============================================================================


class ListTasksInput(BaseModel):
    """Input schema for list_tasks tool."""

    user_id: str = Field(..., description="Unique user identifier")
    status: Optional[str] = Field(None, description="Filter by status: 'all', 'pending', or 'completed'")

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        """Validate user_id is not empty."""
        if not v or not v.strip():
            raise ValueError("user_id is required")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate status filter."""
        if v and v not in ("all", "pending", "completed"):
            raise ValueError("Invalid status filter. Must be 'all', 'pending', or 'completed'")
        return v


class TaskItem(BaseModel):
    """Task item in list response."""

    id: int
    title: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime


class ListTasksOutput(BaseModel):
    """Output schema for list_tasks tool."""

    tasks: List[TaskItem] = Field(default_factory=list)


# ============================================================================
# update_task Tool Schemas
# ============================================================================


class UpdateTaskInput(BaseModel):
    """Input schema for update_task tool."""

    user_id: str = Field(..., description="Unique user identifier")
    task_id: int = Field(..., description="ID of task to update")
    title: Optional[str] = Field(None, max_length=255, description="New task title")
    description: Optional[str] = Field(None, description="New task description")

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        """Validate user_id is not empty."""
        if not v or not v.strip():
            raise ValueError("user_id is required")
        return v

    @field_validator("task_id", mode="before")
    @classmethod
    def validate_task_id(cls, v) -> int:
        """Validate task_id is an integer."""
        try:
            return int(v)
        except (ValueError, TypeError):
            raise ValueError("task_id must be an integer")

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty if provided."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        return v


class UpdateTaskOutput(BaseModel):
    """Output schema for update_task tool."""

    id: int
    title: str
    status: str
    updated_at: datetime


# ============================================================================
# complete_task Tool Schemas
# ============================================================================


class CompleteTaskInput(BaseModel):
    """Input schema for complete_task tool."""

    user_id: str = Field(..., description="Unique user identifier")
    task_id: int = Field(..., description="ID of task to complete")

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        """Validate user_id is not empty."""
        if not v or not v.strip():
            raise ValueError("user_id is required")
        return v

    @field_validator("task_id", mode="before")
    @classmethod
    def validate_task_id(cls, v) -> int:
        """Validate task_id is an integer."""
        try:
            return int(v)
        except (ValueError, TypeError):
            raise ValueError("task_id must be an integer")


class CompleteTaskOutput(BaseModel):
    """Output schema for complete_task tool."""

    id: int
    title: str
    status: str = "completed"
    updated_at: datetime


# ============================================================================
# delete_task Tool Schemas
# ============================================================================


class DeleteTaskInput(BaseModel):
    """Input schema for delete_task tool."""

    user_id: str = Field(..., description="Unique user identifier")
    task_id: int = Field(..., description="ID of task to delete")

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        """Validate user_id is not empty."""
        if not v or not v.strip():
            raise ValueError("user_id is required")
        return v

    @field_validator("task_id", mode="before")
    @classmethod
    def validate_task_id(cls, v) -> int:
        """Validate task_id is an integer."""
        try:
            return int(v)
        except (ValueError, TypeError):
            raise ValueError("task_id must be an integer")


class DeleteTaskOutput(BaseModel):
    """Output schema for delete_task tool."""

    id: int
    status: str = "deleted"
