from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime
from sqlmodel import Session

from app.db.session import get_session
from app.domain.todos.service import (
    get_todos as db_get_todos,
    create_todo as db_create_todo,
    update_todo as db_update_todo,
    delete_todo as db_delete_todo,
    toggle_todo_completion as db_toggle_todo_completion
)
from app.domain.todos.models import Todo as TodoModel, Priority

router = APIRouter(prefix="/todos", tags=["todos"])


class Todo(BaseModel):
    id: int
    title: str
    notes: str | None  # Changed from description to notes to match the model
    priority: str
    completed: bool
    agent_id: int | None = None  # Add agent association
    created_at: str
    updated_at: str
    completed_at: str | None = None

    class Config:
        from_attributes = True


class CreateTodoRequest(BaseModel):
    title: str
    notes: str | None = None  # Changed from description to notes
    priority: str = "medium"
    agent_id: int | None = None  # Add agent association


class UpdateTodoRequest(BaseModel):
    title: str | None = None
    notes: str | None = None  # Changed from description to notes
    priority: str | None = None
    completed: bool | None = None
    agent_id: int | None = None  # Add agent association


def format_datetime(dt):
    """Format datetime for API response"""
    if dt is None:
        return None
    if isinstance(dt, str):
        return dt
    return dt.isoformat()


def map_todo_to_response(todo: TodoModel) -> Todo:
    """Convert Todo model to API response format"""
    return Todo(
        id=todo.id,
        title=todo.title,
        notes=todo.notes,
        priority=todo.priority.value,
        completed=todo.completed,
        agent_id=todo.agent_id,
        created_at=format_datetime(todo.created_at),
        updated_at=format_datetime(todo.updated_at),
        completed_at=format_datetime(todo.completed_at)
    )


@router.get("", response_model=List[Todo])
async def get_todos(session: Session = Depends(get_session)):
    """Get list of all todos from database"""
    todos = db_get_todos(session)
    return [map_todo_to_response(todo) for todo in todos]


@router.post("", response_model=Todo)
async def create_todo(
    todo: CreateTodoRequest,
    session: Session = Depends(get_session)
):
    """Create a new todo in the database"""
    try:
        # Validate priority
        try:
            priority = Priority(todo.priority)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid priority: {todo.priority}. Valid values are: low, medium, high")
        
        # If agent_id is provided, validate that the agent exists
        if todo.agent_id is not None:
            from app.domain.agents.service import get_agent_by_id as get_agent_by_id_service
            agent = get_agent_by_id_service(session, todo.agent_id)
            if not agent:
                raise HTTPException(status_code=404, detail=f"Agent with ID {todo.agent_id} not found")
        
        new_todo = db_create_todo(
            session=session,
            title=todo.title,
            notes=todo.notes,
            priority=priority,
            agent_id=todo.agent_id
        )
        return map_todo_to_response(new_todo)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@router.put("/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: int,
    todo_update: UpdateTodoRequest,
    session: Session = Depends(get_session)
):
    """Update an existing todo in the database"""
    try:
        # Convert priority if provided
        priority = None
        if todo_update.priority is not None:
            try:
                priority = Priority(todo_update.priority)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid priority: {todo_update.priority}. Valid values are: low, medium, high")
        
        # If agent_id is provided, validate that the agent exists
        if todo_update.agent_id is not None:
            from app.domain.agents.service import get_agent_by_id as get_agent_by_id_service
            agent = get_agent_by_id_service(session, todo_update.agent_id)
            if not agent:
                raise HTTPException(status_code=404, detail=f"Agent with ID {todo_update.agent_id} not found")
        
        updated_todo = db_update_todo(
            session=session,
            todo_id=todo_id,
            title=todo_update.title,
            notes=todo_update.notes,
            priority=priority,
            completed=todo_update.completed,
            agent_id=todo_update.agent_id
        )
        
        if not updated_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        return map_todo_to_response(updated_todo)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session)
):
    """Delete a todo from the database"""
    try:
        success = db_delete_todo(session, todo_id)
        if not success:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {"message": "Todo deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")


@router.post("/{todo_id}/toggle", response_model=Todo)
async def toggle_todo_completion_status(
    todo_id: int,
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a todo"""
    try:
        toggled_todo = db_toggle_todo_completion(session, todo_id)
        if not toggled_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return map_todo_to_response(toggled_todo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to toggle task completion: {str(e)}")