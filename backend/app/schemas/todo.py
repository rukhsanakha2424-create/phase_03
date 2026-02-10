from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from app.domain.todos.models import Priority


class TodoBase(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=140)]
    notes: Annotated[str | None, Field(max_length=500)] = None
    priority: Priority = Priority.medium


class CreateTodoRequest(TodoBase):
    pass


class UpdateTodoRequest(BaseModel):
    title: Annotated[str | None, Field(min_length=1, max_length=140)] = None
    notes: Annotated[str | None, Field(max_length=500)] = None
    priority: Priority | None = None


class TodoRead(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None


class DeleteResponse(BaseModel):
    undo_token: str
    expires_at: datetime


class UndoRequest(BaseModel):
    undo_token: str


class ErrorEnvelope(BaseModel):
    code: str
    message: str
    details: dict | None = None
