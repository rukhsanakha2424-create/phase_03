"""MCP tool invocation via HTTP protocol.

Handles communication with MCP tool endpoints, retry logic, error handling,
and response parsing.
"""

import json
import asyncio
from typing import Any, Optional
import httpx
from agent_service_impl.config import Config
from agent_service_impl.tools.system_interactor import (
    read_frontend_file,
    read_backend_file,
    update_frontend_file,
    update_backend_file,
    list_frontend_directory,
    list_backend_directory,
    restart_services
)


class ToolInvocationError(Exception):
    """Raised when tool invocation fails."""

    pass


async def invoke_mcp_tool(
    tool_name: str,
    arguments: dict[str, Any],
    config: Config,
    retries: int = 2,
    user_id: str = None,
) -> dict[str, Any]:
    """Invoke an MCP tool via HTTP endpoint or local function.

    Args:
        tool_name: Name of the tool to invoke (add_task, list_tasks, etc.)
        arguments: Tool parameters as dictionary
        config: Configuration object with MCP_TOOL_ENDPOINT
        retries: Number of retry attempts for transient failures
        user_id: User ID for authorization (overrides config.USER_ID if provided)

    Returns:
        Tool response as dictionary with keys:
        - status: "success" or "error"
        - result: Tool result (if status="success")
        - error: Error message (if status="error")
        - error_code: Error code for classification

    Raises:
        ToolInvocationError: If tool invocation fails after retries
    """
    
    # Handle local system interaction tools directly
    local_tools = {
        'read_frontend_file': read_frontend_file,
        'read_backend_file': read_backend_file,
        'update_frontend_file': update_frontend_file,
        'update_backend_file': update_backend_file,
        'list_frontend_directory': list_frontend_directory,
        'list_backend_directory': list_backend_directory,
        'restart_services': restart_services,
    }
    
    if tool_name in local_tools:
        # Call the local function directly
        try:
            result = local_tools[tool_name](**arguments, config=config)
            return result
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "error_code": "local_tool_error"
            }
    
    # For non-local tools, use HTTP endpoint
    endpoint = config.MCP_TOOL_ENDPOINT
    timeout = config.TIMEOUT_SECONDS
    max_retries = retries or config.MAX_RETRIES

    # Construct request URL
    url = f"{endpoint}/tools/{tool_name}"

    # Prepare request payload - use passed user_id or fall back to config
    payload = {
        "user_id": user_id or config.USER_ID,
        "arguments": arguments,
    }

    last_error = None

    for attempt in range(max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )

                # Parse response
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 400:
                    # User error (validation failure)
                    return {
                        "status": "error",
                        "error_code": "validation_error",
                        "error": response.json().get(
                            "detail", "Invalid parameters"
                        ),
                    }
                elif response.status_code == 404:
                    # Resource not found
                    return {
                        "status": "error",
                        "error_code": "not_found",
                        "error": f"Task not found",
                    }
                elif response.status_code == 500:
                    # Server error - retry
                    last_error = response.json().get("detail", "Server error")
                    if attempt < max_retries:
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    raise ToolInvocationError(last_error)
                else:
                    # Unexpected status
                    last_error = f"HTTP {response.status_code}"
                    if attempt < max_retries:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    raise ToolInvocationError(last_error)

        except httpx.TimeoutException as e:
            last_error = f"Request timeout after {timeout}s"
            if attempt < max_retries:
                await asyncio.sleep(2 ** attempt)
                continue
            raise ToolInvocationError(last_error) from e

        except httpx.RequestError as e:
            last_error = f"Connection error: {str(e)}"
            if attempt < max_retries:
                await asyncio.sleep(2 ** attempt)
                continue
            raise ToolInvocationError(last_error) from e

    # All retries exhausted
    raise ToolInvocationError(f"Tool invocation failed after {max_retries + 1} attempts: {last_error}")


def invoke_mcp_tool_sync(
    tool_name: str,
    arguments: dict[str, Any],
    config: Config,
    retries: int = 2,
    user_id: str = None,
) -> dict[str, Any]:
    """Synchronous wrapper for tool invocation.

    Args:
        tool_name: Name of the tool to invoke
        arguments: Tool parameters
        config: Configuration object
        retries: Number of retry attempts
        user_id: User ID for authorization

    Returns:
        Tool response dictionary
    """
    try:
        return asyncio.run(
            invoke_mcp_tool(tool_name, arguments, config, retries, user_id)
        )
    except ToolInvocationError as e:
        return {
            "status": "error",
            "error_code": "invocation_error",
            "error": str(e),
        }
