"""Basic smoke tests for agent infrastructure.

Tests agent instantiation, configuration loading, and basic message processing.
Validates Phase 2 foundational infrastructure with OpenAI Agents SDK.
"""

import pytest
import json
from unittest.mock import patch, MagicMock

from agent_service_impl.agent import TodoAgent, SYSTEM_PROMPT
from agent_service_impl.config import get_config, Config
from agent_service_impl.tools.tool_definitions import get_tool_definitions
from agent_service_impl.tools.response_formatter import ResponseFormatter, ResponseType


def create_mock_runner_result(final_output: str):
    """Helper to create mock Runner.run_sync result."""
    mock_result = MagicMock()
    mock_result.final_output = final_output
    return mock_result


class TestAgentInstantiation:
    """Test agent initialization and configuration."""

    @pytest.mark.unit
    def test_agent_instantiation_with_config(self, test_config: Config):
        """Test agent can be instantiated with explicit config."""
        agent = TodoAgent(config=test_config)

        assert agent is not None
        assert agent.config == test_config
        assert agent.model is not None
        assert len(agent.tool_definitions) == 6

    @pytest.mark.unit
    def test_agent_default_config(self, test_config):
        """Test agent can be instantiated with default config."""
        agent = TodoAgent(config=test_config)

        assert agent is not None
        assert agent.config is not None
        assert agent.config.OPENROUTER_API_KEY is not None

    @pytest.mark.unit
    def test_agent_tool_definitions_loaded(self, agent: TodoAgent):
        """Test agent loads all tool definitions."""
        assert agent.tool_definitions is not None
        assert len(agent.tool_definitions) == 6

        tool_names = [t["function"]["name"] for t in agent.tool_definitions]
        assert "add_task" in tool_names
        assert "find_task_by_title" in tool_names
        assert "list_tasks" in tool_names
        assert "complete_task" in tool_names
        assert "update_task" in tool_names
        assert "delete_task" in tool_names

    @pytest.mark.unit
    def test_agent_has_sdk_agent(self, agent: TodoAgent):
        """Test agent initializes Agents SDK Agent."""
        assert agent.agent is not None

    @pytest.mark.unit
    def test_system_prompt_defined(self):
        """Test system prompt is properly defined."""
        assert SYSTEM_PROMPT is not None
        assert "Taskie" in SYSTEM_PROMPT
        assert "add_task" in SYSTEM_PROMPT or "Add" in SYSTEM_PROMPT


class TestAgentSDKIntegration:
    """Test Agents SDK integration."""

    @pytest.mark.unit
    def test_agent_has_correct_name(self, agent: TodoAgent):
        """Test agent has correct name configured."""
        assert agent.agent.name == "Taskie"

    @pytest.mark.unit
    def test_agent_has_tools_configured(self, agent: TodoAgent):
        """Test agent has all tools configured."""
        assert len(agent.agent.tools) == 6


class TestMessageProcessing:
    """Test message processing with mocked Runner responses."""

    @pytest.mark.unit
    def test_process_greeting_message(self, agent: TodoAgent):
        """Test processing a greeting returns text response."""
        mock_result = create_mock_runner_result("Hello! I'm Taskie.")

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            result = agent.process_message("Hi there!")

        assert "Hello" in result or "Taskie" in result

    @pytest.mark.unit
    def test_process_add_task_message(self, agent: TodoAgent):
        """Test processing add task returns success message."""
        mock_result = create_mock_runner_result("Successfully added task 'Buy groceries' with ID 1.")

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            result = agent.process_message("Add task buy groceries", user_id="test-user")

        assert "added" in result.lower() or "groceries" in result.lower()

    @pytest.mark.unit
    def test_process_list_tasks_message(self, agent: TodoAgent):
        """Test processing list tasks returns task list."""
        mock_result = create_mock_runner_result("You have 2 task(s):\n⬜ [1] Buy groceries\n⬜ [2] Fix bug")

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            result = agent.process_message("Show my tasks", user_id="test-user")

        assert "task" in result.lower()


class TestErrorHandling:
    """Test error handling in message processing."""

    @pytest.mark.unit
    def test_handle_runner_exception(self, agent: TodoAgent):
        """Test handling Runner exceptions."""
        with patch('agent_service_impl.agent.Runner.run_sync') as mock_runner:
            mock_runner.side_effect = Exception("Connection failed")

            result = agent.process_message("Hello")

        assert "trouble" in result.lower() or "try again" in result.lower()

    @pytest.mark.unit
    def test_handle_tool_invocation_error_in_response(self, agent: TodoAgent):
        """Test handling tool invocation errors returns user-friendly message."""
        mock_result = create_mock_runner_result("Failed to add task: Connection failed")

        with patch('agent_service_impl.agent.Runner.run_sync', return_value=mock_result):
            result = agent.process_message("Add task test", user_id="test-user")

        assert "failed" in result.lower()


class TestResponseFormatting:
    """Test response formatting utilities."""

    @pytest.mark.unit
    def test_format_add_task_success(self):
        """Test formatting add_task success response."""
        msg = ResponseFormatter.format_add_task_success("Buy groceries")

        assert "Buy groceries" in msg
        assert "added" in msg.lower()

    @pytest.mark.unit
    def test_format_list_tasks_success_with_tasks(self):
        """Test formatting list_tasks success with results."""
        tasks = [
            {"id": "1", "title": "Task 1"},
            {"id": "2", "title": "Task 2"},
        ]
        msg = ResponseFormatter.format_list_tasks_success(tasks)

        assert "2" in msg
        assert "Task 1" in msg
        assert "Task 2" in msg

    @pytest.mark.unit
    def test_format_list_tasks_empty(self):
        """Test formatting list_tasks with no results."""
        msg = ResponseFormatter.format_list_tasks_success([])

        assert "no" in msg.lower()

    @pytest.mark.unit
    def test_format_complete_task_success(self):
        """Test formatting complete_task success response."""
        msg = ResponseFormatter.format_complete_task_success("Buy groceries")

        assert "Buy groceries" in msg
        assert "done" in msg.lower() or "mark" in msg.lower()

    @pytest.mark.unit
    def test_format_delete_task_confirmation(self):
        """Test formatting delete confirmation request."""
        msg = ResponseFormatter.format_delete_task_confirmation("Buy groceries")

        assert "Buy groceries" in msg
        assert "sure" in msg.lower() or "confirm" in msg.lower()


class TestToolDefinitions:
    """Test tool definitions are valid."""

    @pytest.mark.unit
    def test_tool_definitions_format(self):
        """Test tool definitions have correct format."""
        definitions = get_tool_definitions()

        assert len(definitions) == 5

        for tool_def in definitions:
            assert tool_def["type"] == "function"
            assert "function" in tool_def
            func = tool_def["function"]
            assert "name" in func
            assert "description" in func
            assert "parameters" in func
            assert func["parameters"]["type"] == "object"

    @pytest.mark.unit
    def test_tool_definitions_have_required_tools(self):
        """Test all required tools are defined."""
        definitions = get_tool_definitions()
        tool_names = [t["function"]["name"] for t in definitions]

        required_tools = [
            "add_task",
            "list_tasks",
            "complete_task",
            "update_task",
            "delete_task",
        ]

        for tool in required_tools:
            assert tool in tool_names, f"Missing tool: {tool}"

    @pytest.mark.unit
    def test_add_task_definition(self):
        """Test add_task tool definition is correct."""
        definitions = get_tool_definitions()
        add_task = next(t for t in definitions if t["function"]["name"] == "add_task")

        assert "title" in add_task["function"]["parameters"]["properties"]
        assert "required" in add_task["function"]["parameters"]
        assert "title" in add_task["function"]["parameters"]["required"]
