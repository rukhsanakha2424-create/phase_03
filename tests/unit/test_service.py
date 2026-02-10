"""Unit tests for TaskService with in-memory storage."""

import pytest
from src.core.service import TaskService
from src.core.storage import InMemoryStorage


def _create_service():
    """Create a TaskService with fresh in-memory storage."""
    storage = InMemoryStorage()
    return TaskService(storage=storage)


def test_add_task():
    service = _create_service()
    task = service.add("Test task")
    assert task.id == 1
    assert task.description == "Test task"
    assert task.completed is False


def test_add_empty_task():
    service = _create_service()
    with pytest.raises(ValueError, match="Description cannot be empty"):
        service.add("")


def test_get_all_tasks():
    service = _create_service()
    service.add("Task 1")
    service.add("Task 2")
    tasks = service.list()
    assert len(tasks) == 2


def test_complete_task():
    service = _create_service()
    service.add("Task 1")
    service.complete(1)
    task = service.get(1)
    assert task.completed is True


def test_complete_toggles_status():
    service = _create_service()
    service.add("Task 1")
    # First complete → marks as complete
    service.complete(1)
    assert service.get(1).completed is True
    # Second complete → toggles back to incomplete
    service.complete(1)
    assert service.get(1).completed is False


def test_update_task():
    service = _create_service()
    service.add("Task 1")
    service.update(1, "Updated task")
    task = service.get(1)
    assert task.description == "Updated task"


def test_delete_task():
    service = _create_service()
    service.add("Task 1")
    assert len(service.list()) == 1
    service.delete(1)
    assert len(service.list()) == 0


def test_delete_non_existent_task():
    service = _create_service()
    # Should return False, not raise
    result = service.delete(99)
    assert result is False


def test_get_non_existent_task():
    service = _create_service()
    task = service.get(99)
    assert task is None


def test_update_non_existent_task():
    service = _create_service()
    with pytest.raises(KeyError, match="Task 99 not found"):
        service.update(99, "New description")


def test_complete_non_existent_task():
    service = _create_service()
    with pytest.raises(KeyError, match="Task 99 not found"):
        service.complete(99)


def test_update_with_empty_description():
    service = _create_service()
    service.add("Task 1")
    with pytest.raises(ValueError, match="Description cannot be empty"):
        service.update(1, "")


def test_sequential_ids():
    service = _create_service()
    t1 = service.add("Task 1")
    t2 = service.add("Task 2")
    t3 = service.add("Task 3")
    assert t1.id == 1
    assert t2.id == 2
    assert t3.id == 3


def test_count():
    service = _create_service()
    assert service.count() == 0
    service.add("Task 1")
    assert service.count() == 1
    service.add("Task 2")
    assert service.count() == 2
    service.delete(1)
    assert service.count() == 1
