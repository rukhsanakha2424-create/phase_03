"""Tests for update_task MCP tool - User Story 3."""

import json

import pytest


class TestUpdateTaskContract:
    """Contract tests for update_task tool inputs/outputs."""

    @pytest.mark.asyncio
    async def test_update_task_title_only(self, create_sample_task, db_pool):
        """Test: update_task with only title parameter."""
        from src.tools.update_task import handle_update_task

        # Create a sample task
        task_row = await create_sample_task("user123", "Original Title", "Original description")
        task_id = task_row["id"]

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
            "title": "Updated Title",
        }

        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        # Verify response structure
        assert "id" in result_dict
        assert result_dict["title"] == "Updated Title"
        assert "status" in result_dict
        assert "updated_at" in result_dict

    @pytest.mark.asyncio
    async def test_update_task_description_only(self, create_sample_task, db_pool):
        """Test: update_task with only description parameter."""
        from src.tools.update_task import handle_update_task

        # Create a sample task
        task_row = await create_sample_task("user123", "Task Title", "Original description")
        task_id = task_row["id"]

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
            "description": "Updated description",
        }

        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        # Verify response structure
        assert "id" in result_dict
        assert result_dict["id"] == task_id
        assert "status" in result_dict
        assert "updated_at" in result_dict

    @pytest.mark.asyncio
    async def test_update_task_both_fields(self, create_sample_task, db_pool):
        """Test: update_task with both title and description."""
        from src.tools.update_task import handle_update_task

        # Create a sample task
        task_row = await create_sample_task("user123", "Original Title", "Original description")
        task_id = task_row["id"]

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
            "title": "New Title",
            "description": "New description",
        }

        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        # Verify response structure
        assert "id" in result_dict
        assert result_dict["title"] == "New Title"
        assert "status" in result_dict
        assert "updated_at" in result_dict

    @pytest.mark.asyncio
    async def test_update_task_title_too_long(self):
        """Test: update_task with title > 255 characters."""
        from src.tools.update_task import handle_update_task

        arguments = {
            "user_id": "user123",
            "task_id": 1,
            "title": "a" * 256,
        }

        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict

    @pytest.mark.asyncio
    async def test_update_task_missing_task_id(self):
        """Test: update_task requires task_id parameter."""
        from src.tools.update_task import handle_update_task

        arguments = {
            "user_id": "user123",
            "title": "New Title",
        }

        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict

    @pytest.mark.asyncio
    async def test_update_task_missing_user_id(self):
        """Test: update_task requires user_id parameter."""
        from src.tools.update_task import handle_update_task

        arguments = {
            "task_id": 1,
            "title": "New Title",
        }

        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict


class TestUpdateTaskIntegration:
    """Integration tests for update_task with database."""

    @pytest.mark.asyncio
    async def test_update_task_persists_to_database(self, create_sample_task, fetch_task, db_pool):
        """Test: update_task changes persist to database."""
        from src.tools.update_task import handle_update_task

        # Create a sample task
        task_row = await create_sample_task("user123", "Original Title", "Original description")
        task_id = task_row["id"]

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
            "title": "Updated Title",
            "description": "Updated description",
        }

        # Update task
        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        # Verify update persisted
        updated_task = await fetch_task(task_id)
        assert updated_task["title"] == "Updated Title"
        assert updated_task["description"] == "Updated description"

    @pytest.mark.asyncio
    async def test_update_task_user_isolation(self, create_sample_task, db_pool):
        """Test: update_task enforces user ownership."""
        from src.tools.update_task import handle_update_task

        # Create task for user A
        task_row = await create_sample_task("userA", "Task A", "Description A")
        task_id = task_row["id"]

        # Try to update as user B
        arguments = {
            "user_id": "userB",
            "task_id": task_id,
            "title": "Hacked Title",
        }

        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        # Should fail - user doesn't own task
        assert "error" in result_dict

    @pytest.mark.asyncio
    async def test_update_task_preserves_status(self, create_sample_task, fetch_task, db_pool):
        """Test: update_task preserves status field."""
        from src.tools.update_task import handle_update_task

        # Create a sample task
        task_row = await create_sample_task("user123", "Task Title", "Task description")
        task_id = task_row["id"]
        original_status = task_row["status"]

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
            "title": "Updated Title",
        }

        # Update task
        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        # Status should not change
        assert result_dict["status"] == original_status

        # Verify in database
        updated_task = await fetch_task(task_id)
        assert updated_task["status"] == original_status

    @pytest.mark.asyncio
    async def test_update_task_updates_timestamp(self, create_sample_task, fetch_task, db_pool):
        """Test: update_task updates the updated_at timestamp."""
        from src.tools.update_task import handle_update_task
        import time

        # Create a sample task
        task_row = await create_sample_task("user123", "Task Title", "Task description")
        task_id = task_row["id"]
        original_updated_at = task_row["updated_at"]

        # Wait a bit to ensure timestamp difference
        await asyncio.sleep(0.1)

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
            "title": "Updated Title",
        }

        # Update task
        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        # Verify timestamp is updated
        updated_task = await fetch_task(task_id)
        assert updated_task["updated_at"] > original_updated_at


class TestUpdateTaskEdgeCases:
    """Edge case tests for update_task tool."""

    @pytest.mark.asyncio
    async def test_update_task_nonexistent_task(self):
        """Test: update_task on non-existent task returns error."""
        from src.tools.update_task import handle_update_task

        arguments = {
            "user_id": "user123",
            "task_id": 99999,
            "title": "New Title",
        }

        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict

    @pytest.mark.asyncio
    async def test_update_task_exact_255_characters(self, create_sample_task, fetch_task, db_pool):
        """Test: update_task accepts exactly 255 character title."""
        from src.tools.update_task import handle_update_task

        # Create a sample task
        task_row = await create_sample_task("user123", "Task Title", "Task description")
        task_id = task_row["id"]

        title_255 = "a" * 255

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
            "title": title_255,
        }

        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        # Should succeed
        assert "error" not in result_dict
        assert result_dict["title"] == title_255

    @pytest.mark.asyncio
    async def test_update_task_with_special_characters(self, create_sample_task, fetch_task, db_pool):
        """Test: update_task handles special characters in title/description."""
        from src.tools.update_task import handle_update_task

        # Create a sample task
        task_row = await create_sample_task("user123", "Task Title", "Task description")
        task_id = task_row["id"]

        special_title = "Task with emoji! 🚀 and symbols @#$%"
        special_desc = "Description with special chars: <>&\""

        arguments = {
            "user_id": "user123",
            "task_id": task_id,
            "title": special_title,
            "description": special_desc,
        }

        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        # Should succeed
        assert "error" not in result_dict
        assert result_dict["title"] == special_title

        # Verify in database
        updated_task = await fetch_task(task_id)
        assert updated_task["title"] == special_title

    @pytest.mark.asyncio
    async def test_update_task_empty_title_invalid(self):
        """Test: update_task rejects empty title."""
        from src.tools.update_task import handle_update_task

        arguments = {
            "user_id": "user123",
            "task_id": 1,
            "title": "",
        }

        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict

    @pytest.mark.asyncio
    async def test_update_task_whitespace_only_title(self):
        """Test: update_task rejects whitespace-only title."""
        from src.tools.update_task import handle_update_task

        arguments = {
            "user_id": "user123",
            "task_id": 1,
            "title": "   ",
        }

        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        assert "error" in result_dict

    @pytest.mark.asyncio
    async def test_update_task_no_fields_to_update(self):
        """Test: update_task with neither title nor description is valid (no-op)."""
        from src.tools.update_task import handle_update_task

        arguments = {
            "user_id": "user123",
            "task_id": 1,
        }

        result = await handle_update_task(arguments)
        result_dict = json.loads(result)

        # This is technically valid - just updates nothing
        # Should return error for non-existent task, not for missing fields
        assert "error" in result_dict


# Import asyncio for sleep in tests
import asyncio
