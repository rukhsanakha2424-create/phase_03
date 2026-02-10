from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.db.session import get_session
from app.domain.todos.models import Priority
from app.domain.todos.service import TodoNotFoundError, TodoService
from app.schemas.todo import (
    CreateTodoRequest,
    DeleteResponse,
    TodoRead,
    UndoRequest,
    UpdateTodoRequest,
)

router = APIRouter(prefix="/todos", tags=["todos"])


def get_service(session=Depends(get_session)) -> TodoService:
    return TodoService(session)


@router.get("", response_model=list[TodoRead])
async def list_todos(
    status_filter: str | None = Query(None, alias="status"),
    service: TodoService = Depends(get_service),
):
    try:
        todos = service.list_todos(status=status_filter)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return todos


@router.post("", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_todo(payload: CreateTodoRequest, service: TodoService = Depends(get_service)):
    todo = service.create_todo(title=payload.title, notes=payload.notes, priority=payload.priority)
    return todo


@router.patch("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: int,
    payload: UpdateTodoRequest,
    service: TodoService = Depends(get_service),
):
    try:
        todo = service.update_todo(
            todo_id,
            title=payload.title,
            notes=payload.notes,
            priority=payload.priority or Priority.medium if payload.priority is None else payload.priority,
        )
    except TodoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return todo


@router.post("/{todo_id}/toggle", response_model=TodoRead)
async def toggle_todo(todo_id: int, service: TodoService = Depends(get_service)):
    try:
        todo = service.toggle_completion(todo_id)
    except TodoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return todo


@router.delete("/{todo_id}", response_model=DeleteResponse)
async def delete_todo(todo_id: int, service: TodoService = Depends(get_service)):
    try:
        service.delete_todo(todo_id)
    except TodoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    expires_at = datetime.utcnow() + timedelta(seconds=5)
    undo_token = f"todo:{todo_id}:{int(expires_at.timestamp())}"
    return DeleteResponse(undo_token=undo_token, expires_at=expires_at)


@router.post("/{todo_id}/undo", response_model=TodoRead)
async def undo_delete(todo_id: int, payload: UndoRequest, service: TodoService = Depends(get_service)):
    try:
        todo = service.undo_delete(todo_id, payload.undo_token)
    except NotImplementedError as exc:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(exc)) from exc
    except TodoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return todo
