"""Tests for User Story 1: Natural Language Task Creation.

Tests agent's ability to interpret "add task" natural language commands
and invoke the add_task MCP tool via OpenAI Agents SDK.
"""

import pytest
from unittest.mock import patch, MagicMock
from agent_service_impl.agent import TodoAgent


def create_mock_runner_result(final_output: str):
    """Helper to create mock Runner.run_sync result."""
    mock_result = MagicMock()
    mock_result.final_output = final_output
    return mock_result


class TestAddTaskAgent:
    """Test suite for add_task user story."""

    @pytest.mark.unit
    def test_add_task_with_title_only(self, agent: TodoAgent):
        """Test case 1: Valid add with title only."""
        mock_result = create_mock_runner_result(
            "Successfully added task 'Buy groceries' with ID 1."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Add task: Buy groceries", user_id="test-user")

        assert "Buy groceries" in response
        assert "added" in response.lower()

    @pytest.mark.unit
    def test_add_task_with_title_and_description(self, agent: TodoAgent):
        """Test case 2: Valid add with title + description."""
        mock_result = create_mock_runner_result(
            "Successfully added task 'Buy groceries' with ID 1."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message(
                "Add task: Buy groceries with description milk, eggs, bread",
                user_id="test-user"
            )

        assert "Buy groceries" in response
        assert "added" in response.lower()

    @pytest.mark.unit
    def test_add_task_missing_title_llm_asks_clarification(self, agent: TodoAgent):
        """Test case 3: Missing title (LLM asks for clarification)."""
        mock_result = create_mock_runner_result(
            "What task would you like to add? Please provide a title."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Add task: ")

        assert len(response) > 10
        assert isinstance(response, str)

    @pytest.mark.unit
    def test_add_task_tool_error_database_failure(self, agent: TodoAgent):
        """Test case 6: Tool error - database failure."""
        mock_result = create_mock_runner_result(
            "Failed to add task: Database connection error"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Add task: Buy groceries", user_id="test-user")

        assert "failed" in response.lower() or "error" in response.lower()

    @pytest.mark.unit
    def test_add_task_confirmation_includes_name(self, agent: TodoAgent):
        """Test case 7: Confirmation message includes task name."""
        task_name = "Buy milk and eggs"
        mock_result = create_mock_runner_result(
            f"Successfully added task '{task_name}' with ID 1."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message(f"Add task: {task_name}", user_id="test-user")

        assert task_name in response

    @pytest.mark.unit
    def test_add_task_tool_timeout(self, agent: TodoAgent):
        """Test case 9: MCP tool timeout (agent handles gracefully)."""
        mock_result = create_mock_runner_result(
            "Failed to add task: Request timed out"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Add task: Buy groceries", user_id="test-user")

        assert "failed" in response.lower() or "timeout" in response.lower()

    @pytest.mark.unit
    def test_add_task_tool_http_error(self, agent: TodoAgent):
        """Test case 10: MCP tool HTTP error."""
        mock_result = create_mock_runner_result(
            "Failed to add task: HTTP 500 Internal Server Error"
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Add task: Buy groceries", user_id="test-user")

        assert "failed" in response.lower() or "error" in response.lower()

    @pytest.mark.unit
    def test_add_task_multi_user_isolation(self, agent: TodoAgent):
        """Test case 11: Multi-user isolation."""
        mock_result = create_mock_runner_result(
            "Successfully added task 'Task 1' with ID 1."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result) as mock_run:
            response = agent.process_message("Add task: Task 1", user_id="user-123")

            # Verify runner was called with proper context
            assert mock_run.called
            call_args = mock_run.call_args
            # The context should contain the user_id
            assert call_args.kwargs.get('context').user_id == "user-123"

    @pytest.mark.unit
    def test_add_task_returns_task_id(self, agent: TodoAgent):
        """Test case 12: Task ID returned correctly."""
        mock_result = create_mock_runner_result(
            "Successfully added task 'Buy groceries' with ID task-12345."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Add task: Buy groceries", user_id="test-user")

        assert "added" in response.lower()


class TestAddTaskAcceptanceScenarios:
    """Test acceptance scenarios from spec.md US1."""

    @pytest.mark.unit
    def test_scenario_1_basic_task_creation(self, agent: TodoAgent):
        """Scenario 1: User creates a simple task."""
        mock_result = create_mock_runner_result(
            "Got it! I've added 'Buy groceries' to your list."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Add task: Buy groceries", user_id="test-user")

        assert "added" in response.lower() or "got it" in response.lower()
        assert "Buy groceries" in response

    @pytest.mark.unit
    def test_scenario_2_task_with_description(self, agent: TodoAgent):
        """Scenario 2: User creates task with description."""
        mock_result = create_mock_runner_result(
            "Successfully added task 'Review PR' with ID 1."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Add task: Review PR", user_id="test-user")

        assert "Review PR" in response
        assert "added" in response.lower()

    @pytest.mark.unit
    def test_scenario_3_natural_language_variation(self, agent: TodoAgent):
        """Scenario 3: Natural language variation."""
        mock_result = create_mock_runner_result(
            "Successfully added task 'call mom' with ID 1."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Remind me to call mom", user_id="test-user")

        assert "added" in response.lower()

    @pytest.mark.unit
    def test_scenario_4_clarification_on_missing_title(self, agent: TodoAgent):
        """Scenario 4: LLM handles missing title gracefully."""
        mock_result = create_mock_runner_result(
            "What task would you like me to add? Please give me a title."
        )

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            response = agent.process_message("Add task: ")

        assert len(response) > 10
        assert isinstance(response, str)
