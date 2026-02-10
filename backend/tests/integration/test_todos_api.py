from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.api.v1.todos import router
from app.db.session import get_session
from app.domain.todos.service import TodoService
from app.main import app

engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)


def override_get_session():
    with Session(engine) as session:
        yield session


def override_get_service():
    with Session(engine) as session:
        yield TodoService(session)


app.dependency_overrides[get_session] = override_get_session
app.include_router(router, prefix="/api/v1")
client = TestClient(app)


def test_create_and_list_todos():
    response = client.post(
        "/api/v1/todos",
        json={"title": "Test", "notes": "Note", "priority": "medium"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test"

    list_response = client.get("/api/v1/todos")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_toggle_completion():
    todo = client.post(
        "/api/v1/todos",
        json={"title": "Toggle", "notes": None, "priority": "low"},
    ).json()
    todo_id = todo["id"]

    toggle_response = client.post(f"/api/v1/todos/{todo_id}/toggle")
    assert toggle_response.status_code == 200
    assert toggle_response.json()["completed"] is True


def test_delete_todo():
    todo = client.post(
        "/api/v1/todos",
        json={"title": "Delete", "notes": None, "priority": "low"},
    ).json()
    todo_id = todo["id"]

    delete_response = client.delete(f"/api/v1/todos/{todo_id}")
    assert delete_response.status_code == 200
    assert "undo_token" in delete_response.json()

    list_response = client.get("/api/v1/todos")
    assert all(t["id"] != todo_id for t in list_response.json())
