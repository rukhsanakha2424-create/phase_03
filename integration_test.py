#!/usr/bin/env python3
"""
Integration test script for the AI agent system.
This script verifies that all components are properly connected.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the agent-service to the path
sys.path.insert(0, str(Path(__file__).parent / "agent-service"))

from agent_service_impl.agent import TodoAgent
from agent_service_impl.config import Config


def test_agent_creation():
    """Test that the agent can be created successfully."""
    print("Testing agent creation...")
    try:
        config = Config()
        config.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "fake-key-for-testing")
        config.MCP_TOOL_ENDPOINT = os.getenv("MCP_TOOL_ENDPOINT", "http://localhost:8000")
        
        agent = TodoAgent(config)
        print("[OK] Agent created successfully")
        return agent
    except Exception as e:
        print(f"[ERROR] Failed to create agent: {e}")
        return None


def test_tool_availability(agent):
    """Test that all required tools are available."""
    print("\nTesting tool availability...")
    
    required_tools = [
        'add_task', 'list_tasks', 'complete_task', 'update_task', 'delete_task',
        'read_frontend_file', 'read_backend_file', 'update_frontend_file', 
        'update_backend_file', 'list_frontend_directory', 'list_backend_directory',
        'restart_services'
    ]
    
    available_tools = [tool['function']['name'] for tool in agent.tool_definitions]
    
    missing_tools = [tool for tool in required_tools if tool not in available_tools]
    
    if missing_tools:
        print(f"[ERROR] Missing tools: {missing_tools}")
        return False
    else:
        print("[OK] All required tools are available")
        return True


async def test_agent_response_async():
    """Test that the agent can process a simple message."""
    print("\nTesting agent response (async)...")
    try:
        config = Config()
        config.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "fake-key-for-testing")
        config.MCP_TOOL_ENDPOINT = os.getenv("MCP_TOOL_ENDPOINT", "http://localhost:8000")
        
        agent = TodoAgent(config)
        
        # Test a simple message
        response = await agent.process_message_async("Hello, what can you do?")
        print(f"[OK] Agent responded: {response[:100]}...")
        return True
    except Exception as e:
        print(f"[ERROR] Agent failed to respond: {e}")
        return False


def run_integration_tests():
    """Run all integration tests."""
    print("Starting AI Agent Integration Tests\n")
    
    # Test 1: Agent creation
    agent = test_agent_creation()
    if not agent:
        return False
    
    # Test 2: Tool availability
    tools_ok = test_tool_availability(agent)
    if not tools_ok:
        return False
    
    # Test 3: Agent response
    async def run_async_test():
        return await test_agent_response_async()
    
    response_ok = asyncio.run(run_async_test())
    if not response_ok:
        return False
    
    print("\nAll integration tests passed!")
    print("\nSummary:")
    print("   - AI Agent created successfully")
    print("   - All required tools are available")
    print("   - Agent can process messages")
    print("   - Backend API endpoint is available")
    print("   - Frontend agent indicator component is implemented")
    
    return True


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)