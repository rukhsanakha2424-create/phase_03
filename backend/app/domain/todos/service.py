from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from app.domain.todos.models import Todo, Priority


def get_todos(session: Session) -> List[Todo]:
    """Get all todos from the database"""
    statement = select(Todo).order_by(Todo.created_at.desc())
    todos = session.exec(statement).all()
    return todos


def get_todo_by_id(session: Session, todo_id: int) -> Optional[Todo]:
    """Get a specific todo by ID"""
    statement = select(Todo).where(Todo.id == todo_id)
    todo = session.exec(statement).first()
    return todo


def create_todo(session: Session, title: str, notes: Optional[str] = None, priority: Priority = Priority.medium, agent_id: Optional[int] = None) -> Todo:
    """Create a new todo in the database"""
    todo = Todo(
        title=title,
        notes=notes,
        priority=priority,
        agent_id=agent_id,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def update_todo(
    session: Session,
    todo_id: int,
    title: Optional[str] = None,
    notes: Optional[str] = None,
    priority: Optional[Priority] = None,
    completed: Optional[bool] = None,
    agent_id: Optional[int] = None
) -> Optional[Todo]:
    """Update an existing todo in the database"""
    todo = get_todo_by_id(session, todo_id)
    if not todo:
        return None
    
    # Update fields if provided
    if title is not None:
        todo.title = title
    if notes is not None:
        todo.notes = notes
    if priority is not None:
        todo.priority = priority
    if completed is not None:
        todo.completed = completed
        if completed and not todo.completed_at:
            todo.completed_at = datetime.utcnow()
        elif not completed:
            todo.completed_at = None
    if agent_id is not None:
        todo.agent_id = agent_id
    
    todo.updated_at = datetime.utcnow()
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def delete_todo(session: Session, todo_id: int) -> bool:
    """Delete a todo from the database"""
    todo = get_todo_by_id(session, todo_id)
    if not todo:
        return False
    
    session.delete(todo)
    session.commit()
    return True


def toggle_todo_completion(session: Session, todo_id: int) -> Optional[Todo]:
    """Toggle the completion status of a todo"""
    todo = get_todo_by_id(session, todo_id)
    if not todo:
        return None
    
    todo.completed = not todo.completed
    if todo.completed and not todo.completed_at:
        todo.completed_at = datetime.utcnow()
    elif not todo.completed:
        todo.completed_at = None
    
    todo.updated_at = datetime.utcnow()
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo