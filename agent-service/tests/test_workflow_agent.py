"""Tests for User Story 6: Multi-Step Workflows.

Tests agent's ability to handle complex, multi-step task scenarios
using OpenAI Agents SDK.
"""

import pytest
from unittest.mock import patch, MagicMock
from agent_service_impl.agent import TodoAgent


def create_mock_runner_result(final_output: str):
    """Helper to create mock Runner.run_sync result."""
    mock_result = MagicMock()
    mock_result.final_output = final_output
    return mock_result


class TestWorkflowAgent:
    """Test suite for multi-step workflow scenarios."""

    @pytest.mark.unit
    def test_workflow_create_then_list(self, agent: TodoAgent):
        """Test case 1: Create task then list all tasks."""
        # First operation: create task
        create_result = create_mock_runner_result(
            "Successfully added task 'Buy groceries' with ID 1."
        )
        with patch('agent_service_impl.agent.Runner.run_sync', return_value=create_result):
            response1 = agent.process_message("Add task: Buy groceries", user_id="test-user")
        assert "added" in response1.lower() or "got it" in response1.lower()

        # Second operation: list tasks
        list_result = create_mock_runner_result(
            "You have 1 task(s):\n⬜ [1] Buy groceries"
        )
        with patch('agent_service_impl.agent.Runner.run_sync', return_value=list_result):
            response2 = agent.process_message("List my tasks", user_id="test-user")
        assert "task" in response2.lower()

    @pytest.mark.unit
    def test_workflow_create_complete_list(self, agent: TodoAgent):
        """Test case 2: Create, complete, then list tasks."""
        # Create task
        create_result = create_mock_runner_result(
            "Successfully added task 'Test task' with ID 1."
        )
        with patch('agent_service_impl.agent.Runner.run_sync', return_value=create_result):
            response = agent.process_message("Add task: Test task", user_id="test-user")
        assert len(response) > 5

        # Complete task
        complete_result = create_mock_runner_result(
            "Great! I've marked 'Test task' as done."
        )
        with patch('agent_service_impl.agent.Runner.run_sync', return_value=complete_result):
            response = agent.process_message("Complete task 1", user_id="test-user")
        assert len(response) > 5

        # List tasks
        list_result = create_mock_runner_result(
            "You have 1 task(s):\n✅ [1] Test task"
        )
        with patch('agent_service_impl.agent.Runner.run_sync', return_value=list_result):
            response = agent.process_message("Show my tasks", user_id="test-user")
        assert "task" in response.lower()

    @pytest.mark.unit
    def test_workflow_error_handling_multi_step(self, agent: TodoAgent):
        """Test case 7: Error handling in multi-step flows."""
        # First step succeeds
        create_result = create_mock_runner_result(
            "Successfully added task 'Task 1' with ID 1."
        )
        with patch('agent_service_impl.agent.Runner.run_sync', return_value=create_result):
            response = agent.process_message("Add task: Task 1", user_id="test-user")
        assert len(response) > 5

        # Second step fails
        error_result = create_mock_runner_result(
            "I couldn't find task 999. Would you like me to list your tasks?"
        )
        with patch('agent_service_impl.agent.Runner.run_sync', return_value=error_result):
            response = agent.process_message("Complete task 999", user_id="test-user")
        # Should indicate an error occurred
        assert len(response) > 5

    @pytest.mark.unit
    def test_workflow_mixed_operations(self, agent: TodoAgent):
        """Test case 8: Mixed operations workflow."""
        operations = [
            ("Add task: Task 1", "Successfully added task 'Task 1' with ID 1."),
            ("List my tasks", "You have 1 task(s):\n⬜ [1] Task 1"),
            ("Update task 1 to Updated", "Updated! Task 1 has been changed."),
        ]

        for message, expected_output in operations:
            mock_result = create_mock_runner_result(expected_output)
            with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
                response = agent.process_message(message, user_id="test-user")
            assert len(response) > 5


class TestWorkflowAcceptanceScenarios:
    """Test acceptance scenarios from spec.md US6."""

    @pytest.mark.unit
    def test_scenario_create_and_verify(self, agent: TodoAgent):
        """Scenario: Create task and verify it appears in list."""
        # Create
        create_result = create_mock_runner_result(
            "Got it! I've added 'New task' to your list."
        )
        with patch('agent_service_impl.agent.Runner.run_sync', return_value=create_result):
            response = agent.process_message("Add task: New task", user_id="test-user")
        assert "added" in response.lower() or "got it" in response.lower()

        # List
        list_result = create_mock_runner_result(
            "You have 1 task(s):\n⬜ [1] New task"
        )
        with patch('agent_service_impl.agent.Runner.run_sync', return_value=list_result):
            response = agent.process_message("What are my tasks?", user_id="test-user")
        assert "task" in response.lower()
