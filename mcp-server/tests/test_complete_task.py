"""Tests for complete_task MCP tool - User Story 4."""

import json

import pytest


class TestCompleteTaskContract:
    """Contract tests for complete_task tool inputs/outputs."""

    @pytest.mark.asyncio
    async def test_complete_task_valid_input(self, create_sample_task, db_pool):
        """Test: complete_task with valid user_id and task_id."""
        from src.tools.complete_task import handle_complete_task

        # Create a sample task
        task_row = await create_sample_task("user123", "Task Title")
        task_id = task_row["id"]

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
        }

        result = await handle_complete_task(arguments)
        result_dict = json.loads(result)

        # Verify response structure
        assert "id" in result_dict
        assert result_dict["id"] == task_id
        assert "title" in result_dict
        assert "status" in result_dict
        assert result_dict["status"] == "completed"
        assert "updated_at" in result_dict

    @pytest.mark.asyncio
    async def test_complete_task_missing_task_id(self):
        """Test: complete_task requires task_id parameter."""
        from src.tools.complete_task import handle_complete_task

        arguments = {
            "user_id": "user123",
        }

        result = await handle_complete_task(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict

    @pytest.mark.asyncio
    async def test_complete_task_missing_user_id(self):
        """Test: complete_task requires user_id parameter."""
        from src.tools.complete_task import handle_complete_task

        arguments = {
            "task_id": 1,
        }

        result = await handle_complete_task(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict


class TestCompleteTaskIntegration:
    """Integration tests for complete_task with database."""

    @pytest.mark.asyncio
    async def test_complete_task_changes_status(self, create_sample_task, fetch_task, db_pool):
        """Test: complete_task changes status to completed."""
        from src.tools.complete_task import handle_complete_task

        # Create a sample task with status='pending'
        task_row = await create_sample_task("user123", "Task Title")
        task_id = task_row["id"]
        assert task_row["status"] == "pending"

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
        }

        # Complete the task
        result = await handle_complete_task(arguments)
        result_dict = json.loads(result)

        # Verify status changed
        assert result_dict["status"] == "completed"

        # Verify in database
        completed_task = await fetch_task(task_id)
        assert completed_task["status"] == "completed"

    @pytest.mark.asyncio
    async def test_complete_task_is_idempotent(self, create_sample_task, fetch_task, db_pool):
        """Test: complete_task is idempotent (completing twice returns same result)."""
        from src.tools.complete_task import handle_complete_task

        # Create a sample task
        task_row = await create_sample_task("user123", "Task Title")
        task_id = task_row["id"]

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
        }

        # Complete task first time
        result1 = await handle_complete_task(arguments)
        result1_dict = json.loads(result1)

        # Complete task second time (idempotent)
        result2 = await handle_complete_task(arguments)
        result2_dict = json.loads(result2)

        # Both should succeed and return same status
        assert "error" not in result1_dict
        assert "error" not in result2_dict
        assert result1_dict["status"] == "completed"
        assert result2_dict["status"] == "completed"

    @pytest.mark.asyncio
    async def test_complete_task_user_isolation(self, create_sample_task, db_pool):
        """Test: complete_task enforces user ownership."""
        from src.tools.complete_task import handle_complete_task

        # Create task for user A
        task_row = await create_sample_task("userA", "Task A")
        task_id = task_row["id"]

        # Try to complete as user B
        arguments = {
            "user_id": "userB",
            "task_id": task_id,
        }

        result = await handle_complete_task(arguments)
        result_dict = json.loads(result)

        # Should fail - user doesn't own task
        assert "error" in result_dict

    @pytest.mark.asyncio
    async def test_complete_task_nonexistent_task(self):
        """Test: complete_task on non-existent task returns error."""
        from src.tools.complete_task import handle_complete_task

        arguments = {
            "user_id": "user123",
            "task_id": 99999,
        }

        result = await handle_complete_task(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict
