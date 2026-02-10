"""Tests for list_tasks MCP tool - User Story 2."""

import json

import pytest


class TestListTasksContract:
    """Contract tests for list_tasks tool inputs/outputs."""

    @pytest.mark.asyncio
    async def test_list_tasks_all_status(self, create_sample_task, db_pool):
        """Test: list_tasks with status='all' returns all tasks."""
        from src.tools.list_tasks import handle_list_tasks

        # Create sample tasks
        await create_sample_task("user123", "Task 1")
        await create_sample_task("user123", "Task 2")

        arguments = {
            "user_id": "user123",
            "status": "all",
        }

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        # Verify response structure
        assert "tasks" in result_dict
        assert isinstance(result_dict["tasks"], list)
        assert len(result_dict["tasks"]) == 2

    @pytest.mark.asyncio
    async def test_list_tasks_pending_filter(self, create_sample_task, db_pool):
        """Test: list_tasks with status='pending' filters correctly."""
        from src.tools.list_tasks import handle_list_tasks

        # Create pending tasks
        await create_sample_task("user123", "Pending 1")
        await create_sample_task("user123", "Pending 2")

        arguments = {
            "user_id": "user123",
            "status": "pending",
        }

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        # Verify pending filter
        assert len(result_dict["tasks"]) == 2
        assert all(t["status"] == "pending" for t in result_dict["tasks"])

    @pytest.mark.asyncio
    async def test_list_tasks_completed_filter(self, db_pool):
        """Test: list_tasks with status='completed' returns only completed tasks."""
        from src.tools.list_tasks import handle_list_tasks

        arguments = {
            "user_id": "user123",
            "status": "completed",
        }

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        # Should return empty (no completed tasks created in this test)
        assert result_dict["tasks"] == []

    @pytest.mark.asyncio
    async def test_list_tasks_empty_user(self, db_pool):
        """Test: list_tasks for user with no tasks returns empty array."""
        from src.tools.list_tasks import handle_list_tasks

        arguments = {
            "user_id": "nonexistent_user",
        }

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        assert result_dict["tasks"] == []

    @pytest.mark.asyncio
    async def test_list_tasks_invalid_status(self):
        """Test: list_tasks validates status parameter."""
        from src.tools.list_tasks import handle_list_tasks

        arguments = {
            "user_id": "user123",
            "status": "invalid_status",
        }

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict

    @pytest.mark.asyncio
    async def test_list_tasks_missing_user_id(self):
        """Test: list_tasks requires user_id parameter."""
        from src.tools.list_tasks import handle_list_tasks

        arguments = {}

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict


class TestListTasksIntegration:
    """Integration tests for list_tasks with database."""

    @pytest.mark.asyncio
    async def test_list_tasks_user_isolation(self, create_sample_task, db_pool):
        """Test: list_tasks enforces user isolation."""
        from src.tools.list_tasks import handle_list_tasks

        # Create tasks for different users
        await create_sample_task("userA", "Task A")
        await create_sample_task("userB", "Task B")

        # List tasks for user A
        arguments = {
            "user_id": "userA",
        }

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        # Verify only user A's tasks are returned
        assert len(result_dict["tasks"]) == 1
        assert result_dict["tasks"][0]["user_id"] == "userA"
        assert result_dict["tasks"][0]["title"] == "Task A"

    @pytest.mark.asyncio
    async def test_list_tasks_contains_metadata(self, create_sample_task, db_pool):
        """Test: list_tasks returns all task metadata."""
        from src.tools.list_tasks import handle_list_tasks

        await create_sample_task("user123", "Task with metadata")

        arguments = {
            "user_id": "user123",
        }

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        task = result_dict["tasks"][0]

        # Verify all required fields present
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "status" in task
        assert "created_at" in task
        assert "updated_at" in task

    @pytest.mark.asyncio
    async def test_list_tasks_sorted_by_created_at(self, create_sample_task, db_pool):
        """Test: list_tasks returns tasks ordered by created_at DESC."""
        from src.tools.list_tasks import handle_list_tasks
        import time

        # Create tasks with time gap
        await create_sample_task("user123", "Task 1")
        await create_sample_task("user123", "Task 2")
        await create_sample_task("user123", "Task 3")

        arguments = {
            "user_id": "user123",
        }

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        tasks = result_dict["tasks"]

        # Verify ordering (most recent first)
        assert tasks[0]["title"] == "Task 3"
        assert tasks[1]["title"] == "Task 2"
        assert tasks[2]["title"] == "Task 1"

    @pytest.mark.asyncio
    async def test_list_tasks_default_status_all(self, create_sample_task, db_pool):
        """Test: list_tasks without status filter defaults to 'all'."""
        from src.tools.list_tasks import handle_list_tasks

        await create_sample_task("user123", "Any task")

        arguments = {
            "user_id": "user123",
        }

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        # Should return task (no status filter)
        assert len(result_dict["tasks"]) == 1


class TestListTasksEdgeCases:
    """Edge case tests for list_tasks tool."""

    @pytest.mark.asyncio
    async def test_list_tasks_many_tasks(self, create_sample_task, db_pool):
        """Test: list_tasks handles many tasks efficiently."""
        from src.tools.list_tasks import handle_list_tasks

        # Create 50 tasks
        for i in range(50):
            await create_sample_task("user123", f"Task {i+1}")

        arguments = {
            "user_id": "user123",
        }

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        # Should return all 50 tasks
        assert len(result_dict["tasks"]) == 50

    @pytest.mark.asyncio
    async def test_list_tasks_mixed_statuses(self, db_pool):
        """Test: list_tasks status filter works with mixed pending/completed."""
        from src.tools.list_tasks import handle_list_tasks
        from src.db.connection import DatabasePool

        pool = DatabasePool.get_pool()

        # Create mixed status tasks
        async with pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO tasks (user_id, title, status, created_at, updated_at)
                VALUES ($1, $2, $3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
                """,
                "user123",
                "Pending task",
                "pending",
            )
            await connection.execute(
                """
                INSERT INTO tasks (user_id, title, status, created_at, updated_at)
                VALUES ($1, $2, $3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
                """,
                "user123",
                "Completed task",
                "completed",
            )

        # List pending only
        arguments = {
            "user_id": "user123",
            "status": "pending",
        }

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        assert len(result_dict["tasks"]) == 1
        assert result_dict["tasks"][0]["status"] == "pending"

    @pytest.mark.asyncio
    async def test_list_tasks_case_sensitivity(self):
        """Test: list_tasks status filter is case-sensitive."""
        from src.tools.list_tasks import handle_list_tasks

        arguments = {
            "user_id": "user123",
            "status": "PENDING",  # uppercase
        }

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        # Should fail - invalid status
        assert "error" in result_dict

    @pytest.mark.asyncio
    async def test_list_tasks_whitespace_user_id(self):
        """Test: list_tasks rejects whitespace-only user_id."""
        from src.tools.list_tasks import handle_list_tasks

        arguments = {
            "user_id": "   ",
        }

        result = await handle_list_tasks(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict
