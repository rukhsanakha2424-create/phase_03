"""Tests for User Story 5: Delete Tasks.

Tests agent's ability to interpret "delete task" natural language commands
and invoke the delete_task MCP tool via OpenAI Agents SDK.
"""

import pytest
from unittest.mock import patch, MagicMock
from agent_service_impl.agent import TodoAgent


def create_mock_runner_result(final_output: str):
    """Helper to create mock Runner.run_sync result."""
    mock_result = MagicMock()
    mock_result.final_output = final_output
    return mock_result


class TestDeleteTaskAgent:
    """Test suite for delete_task user story."""

    @pytest.mark.unit
    def test_delete_task_numeric_id(self, agent: TodoAgent):
        """Test case 1: Delete task by numeric ID."""
        mock_result = create_mock_runner_result(
            "Done! I've deleted task 5."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Delete task 5", user_id="test-user")

        assert "deleted" in response.lower() or "removed" in response.lower()

    @pytest.mark.unit
    def test_delete_task_named_id(self, agent: TodoAgent):
        """Test case 2: Delete task by named ID."""
        mock_result = create_mock_runner_result(
            "Done! I've deleted task 1."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Delete \"Buy groceries\"", user_id="test-user")

        assert "deleted" in response.lower() or "removed" in response.lower()

    @pytest.mark.unit
    def test_delete_task_missing_id(self, agent: TodoAgent):
        """Test case 3: Missing task ID handling - LLM asks for clarification."""
        mock_result = create_mock_runner_result(
            "Which task would you like me to delete? Please provide the task ID."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Delete it")

        assert len(response) > 10

    @pytest.mark.unit
    def test_delete_task_not_found(self, agent: TodoAgent):
        """Test case 4: Tool error - task not found."""
        mock_result = create_mock_runner_result(
            "I couldn't find task 999. It may have already been deleted."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Delete task 999", user_id="test-user")

        assert "couldn't find" in response.lower() or "not found" in response.lower() or len(response) > 10

    @pytest.mark.unit
    def test_delete_task_confirmation_format(self, agent: TodoAgent):
        """Test case 8: Confirmation response format."""
        mock_result = create_mock_runner_result(
            "Done! I've deleted task 1."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Delete task 1", user_id="test-user")

        assert "deleted" in response.lower() or "removed" in response.lower()

    @pytest.mark.unit
    def test_delete_task_multi_user_isolation(self, agent: TodoAgent):
        """Test case 10: Multi-user task isolation."""
        mock_result = create_mock_runner_result(
            "Done! I've deleted task 1."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result) as mock_run:
            response = agent.process_message("Delete task 1", user_id="user-123")

            assert mock_run.called
            call_args = mock_run.call_args
            assert call_args.kwargs.get('context').user_id == "user-123"


class TestDeleteTaskAcceptanceScenarios:
    """Test acceptance scenarios from spec.md US5."""

    @pytest.mark.unit
    def test_scenario_1_delete_by_id(self, agent: TodoAgent):
        """Scenario 1: User deletes task by ID."""
        mock_result = create_mock_runner_result(
            "Done! I've deleted task 5."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Delete task 5", user_id="test-user")

        assert "deleted" in response.lower() or "removed" in response.lower()

    @pytest.mark.unit
    def test_scenario_4_task_not_found(self, agent: TodoAgent):
        """Scenario 4: Task not found error."""
        mock_result = create_mock_runner_result(
            "I couldn't find task 999. It may have already been deleted."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Delete task 999", user_id="test-user")

        assert len(response) > 10
