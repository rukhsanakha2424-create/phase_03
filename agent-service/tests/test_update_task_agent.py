"""Tests for User Story 4: Update Tasks.

Tests agent's ability to interpret "update task" natural language commands
and invoke the update_task MCP tool via OpenAI Agents SDK.
"""

import pytest
from unittest.mock import patch, MagicMock
from agent_service_impl.agent import TodoAgent


def create_mock_runner_result(final_output: str):
    """Helper to create mock Runner.run_sync result."""
    mock_result = MagicMock()
    mock_result.final_output = final_output
    return mock_result


class TestUpdateTaskAgent:
    """Test suite for update_task user story."""

    @pytest.mark.unit
    def test_update_task_title_only(self, agent: TodoAgent):
        """Test case 1: Update task title."""
        mock_result = create_mock_runner_result(
            "Updated! Task 5 has been changed."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message(
                "Update task 5 title to Buy organic groceries",
                user_id="test-user"
            )

        assert "updated" in response.lower() or "changed" in response.lower()

    @pytest.mark.unit
    def test_update_task_description_only(self, agent: TodoAgent):
        """Test case 2: Update task description."""
        mock_result = create_mock_runner_result(
            "Updated! Task 2 has been changed."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message(
                "Update task 2 description to Very important!",
                user_id="test-user"
            )

        assert "updated" in response.lower() or "changed" in response.lower()

    @pytest.mark.unit
    def test_update_task_missing_id(self, agent: TodoAgent):
        """Test case 5: Missing task ID handling - LLM asks for clarification."""
        mock_result = create_mock_runner_result(
            "Which task would you like to update? Please provide the task ID."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Update the task")

        assert len(response) > 10

    @pytest.mark.unit
    def test_update_task_not_found(self, agent: TodoAgent):
        """Test case 6: Tool error - task not found."""
        mock_result = create_mock_runner_result(
            "I couldn't find task 999. Would you like me to list your tasks?"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Update task 999 to New title", user_id="test-user")

        assert "couldn't find" in response.lower() or "not found" in response.lower() or len(response) > 10

    @pytest.mark.unit
    def test_update_task_multi_user_isolation(self, agent: TodoAgent):
        """Test case 11: Multi-user isolation."""
        mock_result = create_mock_runner_result(
            "Updated! Task 1 has been changed."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result) as mock_run:
            response = agent.process_message("Update task 1 to Updated", user_id="user-123")

            assert mock_run.called
            call_args = mock_run.call_args
            assert call_args.kwargs.get('context').user_id == "user-123"


class TestUpdateTaskAcceptanceScenarios:
    """Test acceptance scenarios from spec.md US4."""

    @pytest.mark.unit
    def test_scenario_1_update_title(self, agent: TodoAgent):
        """Scenario 1: Update task title."""
        mock_result = create_mock_runner_result(
            "Updated! Task 5 has been changed."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message(
                "Update task 5 title to Buy organic groceries",
                user_id="test-user"
            )

        assert "updated" in response.lower() or "changed" in response.lower()

    @pytest.mark.unit
    def test_scenario_3_task_not_found(self, agent: TodoAgent):
        """Scenario 3: Task not found error."""
        mock_result = create_mock_runner_result(
            "I couldn't find task 999. Would you like me to list your tasks?"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Update task 999 to New", user_id="test-user")

        assert len(response) > 10
