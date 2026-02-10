"""Pytest configuration and fixtures for agent service tests."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_service_impl.config import Config, get_config
from agent_service_impl.agent import TodoAgent
from tests.fixtures.mock_mcp_tools import MockMCPTools


@pytest.fixture
def test_config(monkeypatch) -> Config:
    """Create test configuration.

    Returns:
        Config instance with test values
    """
    import importlib

    # Override environment first
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    monkeypatch.setenv("MCP_TOOL_ENDPOINT", "http://localhost:8000")
    monkeypatch.setenv("USER_ID", "test-user")
    monkeypatch.setenv("AGENT_MODEL", "gpt-4")

    # Reload config module to pick up new env vars
    import agent_service_impl.config
    importlib.reload(agent_service_impl.config)

    from agent_service_impl.config import get_config
    return get_config()


@pytest.fixture
def mock_openai_client():
    """Create a mock OpenAI client for testing (legacy compatibility)."""
    mock_client = MagicMock()
    return mock_client


@pytest.fixture
def mock_runner_result():
    """Create a mock Runner result for Agents SDK testing."""
    mock_result = MagicMock()
    mock_result.final_output = "Mock response"
    return mock_result


@pytest.fixture
def agent(test_config: Config, mock_openai_client):
    """Create a TodoAgent instance for testing.

    Args:
        test_config: Test configuration fixture
        mock_openai_client: Mock OpenAI client (for legacy compatibility)

    Returns:
        Initialized TodoAgent instance
    """
    # Create agent - it now uses Agents SDK internally
    agent = TodoAgent(config=test_config)
    # Add mock client for legacy test compatibility
    agent.client = mock_openai_client
    return agent


@pytest.fixture
def mock_mcp_tools() -> MockMCPTools:
    """Provide access to mock MCP tool responses.

    Returns:
        MockMCPTools instance
    """
    return MockMCPTools()


@pytest.fixture
def mock_tool_invoker():
    """Create a mock tool invoker for testing.

    Mocks the invoke_mcp_tool_sync function to return predefined responses
    without making actual HTTP calls.

    Returns:
        Mock invoker function
    """

    def _mock_invoke(tool_name: str, arguments: dict, **kwargs):
        """Mock tool invocation."""
        # Return success by default; tests can override
        return {
            "status": "success",
            "result": {"id": "1", "title": "Mock task"},
        }

    return _mock_invoke


@pytest.fixture
def sample_tasks() -> list[dict]:
    """Provide sample task data for testing.

    Returns:
        List of mock task dictionaries
    """
    return [
        {
            "id": "1",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "status": "pending",
        },
        {
            "id": "2",
            "title": "Fix login bug",
            "description": "Users can't reset passwords",
            "status": "pending",
        },
        {
            "id": "3",
            "title": "Review PR #42",
            "description": None,
            "status": "completed",
        },
    ]


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Set up environment variables for all tests.

    Args:
        monkeypatch: Pytest monkeypatch fixture
    """
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("MCP_TOOL_ENDPOINT", "http://localhost:8000")
    monkeypatch.setenv("USER_ID", "test-user")
    monkeypatch.setenv("AGENT_MODEL", "gpt-4")


def create_mock_openai_response(tool_calls=None, content=None):
    """Helper to create mock OpenAI API responses.

    Args:
        tool_calls: List of tool call dicts with 'name' and 'arguments'
        content: Text content for non-tool responses

    Returns:
        Mock response object
    """
    mock_response = MagicMock()
    mock_message = MagicMock()

    if tool_calls:
        mock_tool_calls = []
        for i, tc in enumerate(tool_calls):
            mock_tool_call = MagicMock()
            mock_tool_call.function.name = tc['name']
            mock_tool_call.function.arguments = tc['arguments']
            mock_tool_call.id = f"call_{i}"
            mock_tool_calls.append(mock_tool_call)
        mock_message.tool_calls = mock_tool_calls
        mock_message.content = None
    else:
        mock_message.tool_calls = None
        mock_message.content = content or ""

    mock_response.choices = [MagicMock(message=mock_message)]
    return mock_response


# Test markers
def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow"
    )
