"""Tests for add_task MCP tool - User Story 1."""

import json

import pytest

from src.models.schemas import AddTaskInput
from src.tools.add_task import handle_add_task


class TestAddTaskContract:
    """Contract tests for add_task tool inputs/outputs."""

    @pytest.mark.asyncio
    async def test_add_task_valid_input_with_description(self):
        """Test: add_task with title and description."""
        arguments = {
            "user_id": "user123",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
        }

        result = await handle_add_task(arguments)
        result_dict = json.loads(result)

        # Verify response structure
        assert "task_id" in result_dict
        assert isinstance(result_dict["task_id"], int)
        assert result_dict["title"] == "Buy groceries"
        assert result_dict["status"] == "pending"
        assert "created_at" in result_dict

    @pytest.mark.asyncio
    async def test_add_task_title_only(self):
        """Test: add_task with title only (no description)."""
        arguments = {
            "user_id": "user123",
            "title": "Review PR",
        }

        result = await handle_add_task(arguments)
        result_dict = json.loads(result)

        # Verify response
        assert result_dict["task_id"]
        assert result_dict["title"] == "Review PR"
        assert result_dict["status"] == "pending"

    @pytest.mark.asyncio
    async def test_add_task_missing_title(self):
        """Test: add_task without required title parameter."""
        arguments = {
            "user_id": "user123",
        }

        result = await handle_add_task(arguments)
        result_dict = json.loads(result)

        # Verify error response
        assert "error" in result_dict
        assert "required" in result_dict["error"].lower() or "title" in result_dict["error"].lower()

    @pytest.mark.asyncio
    async def test_add_task_missing_user_id(self):
        """Test: add_task without required user_id parameter."""
        arguments = {
            "title": "Buy groceries",
        }

        result = await handle_add_task(arguments)
        result_dict = json.loads(result)

        # Verify error response
        assert "error" in result_dict
        assert "user_id" in result_dict["error"].lower() or "required" in result_dict["error"].lower()

    @pytest.mark.asyncio
    async def test_add_task_title_too_long(self):
        """Test: add_task validates title max length (255 characters)."""
        long_title = "x" * 256

        arguments = {
            "user_id": "user123",
            "title": long_title,
        }

        result = await handle_add_task(arguments)
        result_dict = json.loads(result)

        # Verify error response
        assert "error" in result_dict
        assert "255" in result_dict["error"] or "characters" in result_dict["error"].lower()

    @pytest.mark.asyncio
    async def test_add_task_empty_title(self):
        """Test: add_task validates that title is not empty."""
        arguments = {
            "user_id": "user123",
            "title": "",
        }

        result = await handle_add_task(arguments)
        result_dict = json.loads(result)

        # Verify error response
        assert "error" in result_dict


class TestAddTaskIntegration:
    """Integration tests for add_task with database."""

    @pytest.mark.asyncio
    async def test_add_task_persists_to_database(self, create_sample_task, fetch_task):
        """Test: add_task persists task to database and is queryable."""
        # Use the create_sample_task fixture (which uses the actual add_task implementation)
        task_id = await create_sample_task("user123", "Buy groceries", "Milk, eggs, bread")

        # Fetch the task from database
        fetched_task = await fetch_task(task_id)

        # Verify persistence
        assert fetched_task is not None
        assert fetched_task["task_id"] == task_id or fetched_task["id"] == task_id
        assert fetched_task["user_id"] == "user123"
        assert fetched_task["title"] == "Buy groceries"
        assert fetched_task["status"] == "pending"

    @pytest.mark.asyncio
    async def test_add_task_user_isolation(self, create_sample_task, fetch_user_tasks):
        """Test: add_task creates task with correct user_id (user isolation)."""
        # Create task for user A
        task_id_a = await create_sample_task("userA", "Task A")

        # Create task for user B
        task_id_b = await create_sample_task("userB", "Task B")

        # Fetch user A's tasks
        user_a_tasks = await fetch_user_tasks("userA")

        # Verify user A only sees their task
        assert len(user_a_tasks) == 1
        assert user_a_tasks[0]["id"] == task_id_a
        assert user_a_tasks[0]["user_id"] == "userA"

        # Verify user B's task is not in user A's list
        task_titles = [t["title"] for t in user_a_tasks]
        assert "Task B" not in task_titles

    @pytest.mark.asyncio
    async def test_add_task_default_status_pending(self, create_sample_task, fetch_task):
        """Test: new task always has status='pending'."""
        task_id = await create_sample_task("user123", "New task")

        fetched_task = await fetch_task(task_id)

        # Verify default status
        assert fetched_task["status"] == "pending"

    @pytest.mark.asyncio
    async def test_add_task_timestamps(self, create_sample_task, fetch_task):
        """Test: add_task sets created_at and updated_at timestamps."""
        task_id = await create_sample_task("user123", "Task with timestamps")

        fetched_task = await fetch_task(task_id)

        # Verify timestamps exist and are not null
        assert fetched_task["created_at"] is not None
        assert fetched_task["updated_at"] is not None
        # They should be equal for a newly created task
        assert fetched_task["created_at"] == fetched_task["updated_at"]


class TestAddTaskEdgeCases:
    """Edge case tests for add_task tool."""

    @pytest.mark.asyncio
    async def test_add_task_with_special_characters(self):
        """Test: add_task handles titles with special characters."""
        arguments = {
            "user_id": "user123",
            "title": "Buy 🛒 items & supplies (urgent!)",
        }

        result = await handle_add_task(arguments)
        result_dict = json.loads(result)

        # Should succeed
        assert "task_id" in result_dict
        assert result_dict["title"] == "Buy 🛒 items & supplies (urgent!)"

    @pytest.mark.asyncio
    async def test_add_task_with_whitespace_title(self):
        """Test: add_task validates that title is not just whitespace."""
        arguments = {
            "user_id": "user123",
            "title": "   ",
        }

        result = await handle_add_task(arguments)
        result_dict = json.loads(result)

        # Should fail
        assert "error" in result_dict

    @pytest.mark.asyncio
    async def test_add_task_exact_255_characters(self):
        """Test: add_task allows title with exactly 255 characters."""
        title_255 = "x" * 255

        arguments = {
            "user_id": "user123",
            "title": title_255,
        }

        result = await handle_add_task(arguments)
        result_dict = json.loads(result)

        # Should succeed
        assert "task_id" in result_dict
        assert len(result_dict["title"]) == 255

    @pytest.mark.asyncio
    async def test_add_task_description_none_vs_missing(self):
        """Test: add_task handles missing description as null."""
        # Without description parameter
        arguments = {
            "user_id": "user123",
            "title": "Task without description",
        }

        result = await handle_add_task(arguments)
        result_dict = json.loads(result)

        # Should succeed (description is optional)
        assert "task_id" in result_dict
