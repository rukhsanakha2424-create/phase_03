"""Tests for delete_task MCP tool - User Story 5."""

import json

import pytest


class TestDeleteTaskContract:
    """Contract tests for delete_task tool inputs/outputs."""

    @pytest.mark.asyncio
    async def test_delete_task_valid_input(self, create_sample_task, db_pool):
        """Test: delete_task with valid user_id and task_id."""
        from src.tools.delete_task import handle_delete_task

        # Create a sample task
        task_row = await create_sample_task("user123", "Task Title")
        task_id = task_row["id"]

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
        }

        result = await handle_delete_task(arguments)
        result_dict = json.loads(result)

        # Verify response structure
        assert "id" in result_dict
        assert result_dict["id"] == task_id
        assert "status" in result_dict

    @pytest.mark.asyncio
    async def test_delete_task_missing_task_id(self):
        """Test: delete_task requires task_id parameter."""
        from src.tools.delete_task import handle_delete_task

        arguments = {
            "user_id": "user123",
        }

        result = await handle_delete_task(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict

    @pytest.mark.asyncio
    async def test_delete_task_missing_user_id(self):
        """Test: delete_task requires user_id parameter."""
        from src.tools.delete_task import handle_delete_task

        arguments = {
            "task_id": 1,
        }

        result = await handle_delete_task(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict


class TestDeleteTaskIntegration:
    """Integration tests for delete_task with database."""

    @pytest.mark.asyncio
    async def test_delete_task_removes_from_database(self, create_sample_task, fetch_task, db_pool):
        """Test: delete_task removes task from database."""
        from src.tools.delete_task import handle_delete_task

        # Create a sample task
        task_row = await create_sample_task("user123", "Task Title")
        task_id = task_row["id"]

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
        }

        # Delete the task
        result = await handle_delete_task(arguments)
        result_dict = json.loads(result)

        # Verify delete succeeded
        assert "error" not in result_dict
        assert result_dict["id"] == task_id

        # Verify task no longer in database
        deleted_task = await fetch_task(task_id)
        assert deleted_task is None

    @pytest.mark.asyncio
    async def test_delete_task_not_in_list_after_deletion(self, create_sample_task, fetch_user_tasks, db_pool):
        """Test: deleted task no longer appears in list_tasks."""
        from src.tools.delete_task import handle_delete_task

        # Create a sample task
        task_row = await create_sample_task("user123", "Task Title")
        task_id = task_row["id"]

        # Verify task is in list before deletion
        tasks_before = await fetch_user_tasks("user123")
        assert len(tasks_before) == 1
        assert tasks_before[0]["id"] == task_id

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
        }

        # Delete the task
        result = await handle_delete_task(arguments)
        result_dict = json.loads(result)

        # Verify task no longer in list
        tasks_after = await fetch_user_tasks("user123")
        assert len(tasks_after) == 0

    @pytest.mark.asyncio
    async def test_delete_task_not_idempotent(self, create_sample_task, db_pool):
        """Test: delete_task is NOT idempotent (re-deletion returns error)."""
        from src.tools.delete_task import handle_delete_task

        # Create a sample task
        task_row = await create_sample_task("user123", "Task Title")
        task_id = task_row["id"]

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
        }

        # Delete task first time
        result1 = await handle_delete_task(arguments)
        result1_dict = json.loads(result1)

        # Try to delete again (should fail)
        result2 = await handle_delete_task(arguments)
        result2_dict = json.loads(result2)

        # First delete should succeed, second should fail
        assert "error" not in result1_dict
        assert "error" in result2_dict

    @pytest.mark.asyncio
    async def test_delete_task_user_isolation(self, create_sample_task, db_pool):
        """Test: delete_task enforces user ownership."""
        from src.tools.delete_task import handle_delete_task

        # Create task for user A
        task_row = await create_sample_task("userA", "Task A")
        task_id = task_row["id"]

        # Try to delete as user B
        arguments = {
            "user_id": "userB",
            "task_id": task_id,
        }

        result = await handle_delete_task(arguments)
        result_dict = json.loads(result)

        # Should fail - user doesn't own task
        assert "error" in result_dict

    @pytest.mark.asyncio
    async def test_delete_task_nonexistent_task(self):
        """Test: delete_task on non-existent task returns error."""
        from src.tools.delete_task import handle_delete_task

        arguments = {
            "user_id": "user123",
            "task_id": 99999,
        }

        result = await handle_delete_task(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict
