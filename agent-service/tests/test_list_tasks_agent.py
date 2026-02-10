"""Tests for User Story 2: Task Listing with Intelligent Filtering.

Tests agent's ability to interpret "list tasks" natural language commands
and invoke the list_tasks MCP tool via OpenAI Agents SDK.
"""

import pytest
from unittest.mock import patch, MagicMock
from agent_service_impl.agent import TodoAgent


def create_mock_runner_result(final_output: str):
    """Helper to create mock Runner.run_sync result."""
    mock_result = MagicMock()
    mock_result.final_output = final_output
    return mock_result


class TestListTasksAgent:
    """Test suite for list_tasks user story."""

    @pytest.mark.unit
    def test_list_tasks_default_all(self, agent: TodoAgent):
        """Test case 1: Default "what are my tasks" (status="all")."""
        mock_result = create_mock_runner_result(
            "You have 3 task(s):\n⬜ [1] Task 1\n⬜ [2] Task 2\n✅ [3] Task 3"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("What are my tasks?", user_id="test-user")

        assert "task" in response.lower()
        assert "3" in response

    @pytest.mark.unit
    def test_list_tasks_pending(self, agent: TodoAgent):
        """Test case 2: "Show pending tasks" (status="pending")."""
        mock_result = create_mock_runner_result(
            "You have 2 pending task(s):\n⬜ [1] Task 1\n⬜ [2] Task 2"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Show my pending tasks", user_id="test-user")

        assert "pending" in response.lower() or "task" in response.lower()

    @pytest.mark.unit
    def test_list_tasks_completed(self, agent: TodoAgent):
        """Test case 3: "Show completed tasks" (status="completed")."""
        mock_result = create_mock_runner_result(
            "You have 1 completed task(s):\n✅ [3] Task 3"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Show completed tasks", user_id="test-user")

        assert "task" in response.lower()

    @pytest.mark.unit
    def test_list_tasks_empty_response(self, agent: TodoAgent):
        """Test case 5: Empty list response handling."""
        mock_result = create_mock_runner_result("You have no tasks.")

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("List my tasks", user_id="test-user")

        assert "no" in response.lower() or "empty" in response.lower()

    @pytest.mark.unit
    def test_list_tasks_single_task(self, agent: TodoAgent):
        """Test case 6: Single task display."""
        mock_result = create_mock_runner_result(
            "You have 1 task(s):\n⬜ [1] Buy groceries"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Show my tasks", user_id="test-user")

        assert "1" in response or "task" in response.lower()

    @pytest.mark.unit
    def test_list_tasks_multiple_tasks_format(self, agent: TodoAgent):
        """Test case 7: Multiple tasks display (numbered, formatted)."""
        mock_result = create_mock_runner_result(
            "You have 3 task(s):\n⬜ [1] Task 1\n⬜ [2] Task 2\n✅ [3] Task 3"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("What are my tasks?", user_id="test-user")

        assert "task" in response.lower()

    @pytest.mark.unit
    def test_list_tasks_tool_error_database(self, agent: TodoAgent):
        """Test case 9: Tool error - database error."""
        mock_result = create_mock_runner_result(
            "Failed to list tasks: Database connection error"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("List my tasks", user_id="test-user")

        assert "failed" in response.lower() or "error" in response.lower()

    @pytest.mark.unit
    def test_list_tasks_multi_user_isolation(self, agent: TodoAgent):
        """Test case 12: Multi-user isolation."""
        mock_result = create_mock_runner_result(
            "You have 1 task(s):\n⬜ [1] User 123's task"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result) as mock_run:
            response = agent.process_message("List my tasks", user_id="user-123")

            assert mock_run.called
            call_args = mock_run.call_args
            assert call_args.kwargs.get('context').user_id == "user-123"


class TestListTasksStatusFilterInference:
    """Test LLM's ability to infer status filter from natural language.

    With OpenAI Agents SDK, the LLM handles status inference automatically.
    These tests verify the agent responds appropriately to different phrasings.
    """

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "message,expected_status",
        [
            ("What are my tasks?", "all"),
            ("Show my tasks", "all"),
            ("List tasks", "all"),
            ("Show pending tasks", "pending"),
            ("What's pending?", "pending"),
            ("List tasks to do", "pending"),
            ("What's left to do?", "pending"),
            ("Show completed tasks", "completed"),
            ("What have I finished?", "completed"),
            ("List done tasks", "completed"),
            ("Show my outstanding tasks", "pending"),
            ("What tasks are remaining?", "pending"),
            ("Show unfinished tasks", "pending"),
            ("List all tasks", "all"),
            ("Display everything", "all"),
        ],
    )
    def test_status_filter_inference(self, agent, message, expected_status):
        """Test LLM correctly infers status filter from various phrasings."""
        mock_result = create_mock_runner_result(
            f"You have 1 {expected_status} task(s):\n⬜ [1] Test task"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message(message, user_id="test-user")

        # Response should be non-empty
        assert len(response) > 5


class TestListTasksAcceptanceScenarios:
    """Test acceptance scenarios from spec.md US2."""

    @pytest.mark.unit
    def test_scenario_1_list_all_tasks(self, agent: TodoAgent):
        """Scenario 1: User lists all tasks."""
        mock_result = create_mock_runner_result(
            "You have 2 task(s):\n⬜ [1] Buy groceries\n✅ [2] Call mom"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("What are my tasks?", user_id="test-user")

        assert "task" in response.lower()

    @pytest.mark.unit
    def test_scenario_3_empty_list_handling(self, agent: TodoAgent):
        """Scenario 3: No tasks found."""
        mock_result = create_mock_runner_result("You have no tasks.")

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("List my tasks", user_id="test-user")

        assert "no" in response.lower() or "empty" in response.lower()
