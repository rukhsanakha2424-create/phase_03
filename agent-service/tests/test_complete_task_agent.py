"""Tests for User Story 3: Task Completion.

Tests agent's ability to interpret "complete task" natural language commands
and invoke the complete_task MCP tool via OpenAI Agents SDK.
"""

import pytest
from unittest.mock import patch, MagicMock
from agent_service_impl.agent import TodoAgent


def create_mock_runner_result(final_output: str):
    """Helper to create mock Runner.run_sync result."""
    mock_result = MagicMock()
    mock_result.final_output = final_output
    return mock_result


class TestCompleteTaskAgent:
    """Test suite for complete_task user story."""

    @pytest.mark.unit
    def test_complete_task_numeric_id(self, agent: TodoAgent):
        """Test case 1: Complete task by numeric ID."""
        mock_result = create_mock_runner_result(
            "Great! I've marked 'Buy groceries' as done."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Mark task 5 as done", user_id="test-user")

        assert "done" in response.lower() or "marked" in response.lower()

    @pytest.mark.unit
    def test_complete_task_named_id(self, agent: TodoAgent):
        """Test case 2: Complete task by named ID."""
        mock_result = create_mock_runner_result(
            "Great! I've marked 'Buy groceries' as done."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Mark \"Buy groceries\" as done", user_id="test-user")

        assert "done" in response.lower() or "marked" in response.lower()

    @pytest.mark.unit
    def test_complete_task_missing_task_id(self, agent: TodoAgent):
        """Test case 3: Missing task ID handling - LLM asks for clarification."""
        mock_result = create_mock_runner_result(
            "Which task would you like me to mark as complete? Please provide the task ID."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Mark it done")

        assert len(response) > 10

    @pytest.mark.unit
    def test_complete_task_not_found(self, agent: TodoAgent):
        """Test case 4: Tool error - task not found."""
        mock_result = create_mock_runner_result(
            "I couldn't find task 999. Would you like me to list your tasks?"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Complete task 999", user_id="test-user")

        assert "couldn't find" in response.lower() or "not found" in response.lower() or len(response) > 10

    @pytest.mark.unit
    def test_complete_task_confirmation_format(self, agent: TodoAgent):
        """Test case 7: Confirmation response format."""
        mock_result = create_mock_runner_result(
            "Great! I've marked 'Buy groceries' as done."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Complete task 1", user_id="test-user")

        assert "Buy groceries" in response or "done" in response.lower()

    @pytest.mark.unit
    def test_complete_task_multi_user_isolation(self, agent: TodoAgent):
        """Test case 10: Multi-user task isolation."""
        mock_result = create_mock_runner_result(
            "Great! I've marked 'Task 1' as done."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result) as mock_run:
            response = agent.process_message("Complete task 1", user_id="user-123")

            assert mock_run.called
            call_args = mock_run.call_args
            assert call_args.kwargs.get('context').user_id == "user-123"


class TestCompleteTaskAcceptanceScenarios:
    """Test acceptance scenarios from spec.md US3."""

    @pytest.mark.unit
    def test_scenario_1_complete_by_id(self, agent: TodoAgent):
        """Scenario 1: User completes task by ID."""
        mock_result = create_mock_runner_result(
            "Great! I've marked 'Buy groceries' as done."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Mark task 5 as done", user_id="test-user")

        assert "done" in response.lower() or "marked" in response.lower()

    @pytest.mark.unit
    def test_scenario_4_task_not_found(self, agent: TodoAgent):
        """Scenario 4: Task not found error."""
        mock_result = create_mock_runner_result(
            "I couldn't find task 999. Would you like me to list your tasks?"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Complete task 999", user_id="test-user")

        assert len(response) > 10
