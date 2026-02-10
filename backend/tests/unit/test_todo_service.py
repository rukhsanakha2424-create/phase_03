import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.domain.todos.models import Priority, Todo
from app.domain.todos.service import TodoNotFoundError, TodoService


def create_test_engine():
    return create_engine("sqlite://", connect_args={"check_same_thread": False})


def init_db(engine):
    SQLModel.metadata.create_all(engine)


@pytest.fixture()
def session():
    engine = create_test_engine()
    init_db(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture()
def service(session):
    return TodoService(session)


def test_create_todo_defaults(service):
    todo = service.create_todo(title="Buy milk", notes=None, priority=Priority.medium)
    assert todo.id is not None
    assert todo.completed is False
    assert todo.priority == Priority.medium


def test_list_todos_filters(service):
    todo1 = service.create_todo(title="Task 1", notes=None, priority=Priority.medium)
    todo2 = service.create_todo(title="Task 2", notes=None, priority=Priority.low)
    service.toggle_completion(todo2.id)

    all_todos = service.list_todos(status=None)
    pending = service.list_todos(status="pending")
    completed = service.list_todos(status="completed")

    assert {t.id for t in all_todos} == {todo1.id, todo2.id}
    assert {t.id for t in pending} == {todo1.id}
    assert {t.id for t in completed} == {todo2.id}


def test_update_todo_fields(service):
    todo = service.create_todo(title="Call mom", notes=None, priority=Priority.low)
    updated = service.update_todo(
        todo.id,
        title="Call dad",
        notes="Evening",
        priority=Priority.high,
    )
    assert updated.title == "Call dad"
    assert updated.notes == "Evening"
    assert updated.priority == Priority.high


def test_toggle_completion(service):
    todo = service.create_todo(title="Task", notes=None, priority=Priority.low)
    toggled = service.toggle_completion(todo.id)
    assert toggled.completed is True
    toggled = service.toggle_completion(todo.id)
    assert toggled.completed is False


def test_delete_todo(service, session):
    todo = service.create_todo(title="Task", notes=None, priority=Priority.low)
    deleted = service.delete_todo(todo.id)
    assert deleted.id == todo.id
    assert session.get(Todo, todo.id) is None


def test_get_missing_todo_raises(service):
    with pytest.raises(TodoNotFoundError):
        service.update_todo(999, title="x", notes=None, priority=None)
