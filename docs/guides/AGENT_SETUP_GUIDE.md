# Agent Setup & Integration Guide

**For Spec 008 Chat Interface**

---

## Overview

The Chat API expects an agent service that can:
1. Receive a user message and conversation history
2. Process the message with AI reasoning
3. Return a response and any tool calls made
4. Complete within 30 seconds

---

## Agent Interface

The agent must implement this interface:

```python
class Agent:
    """Agent service for processing chat messages"""

    async def process_message(
        self,
        message: str,                    # Latest user message
        history: List[Dict[str, Any]],  # Formatted conversation history
        user_id: str,                    # For context
        conversation_id: str = None      # Optional, for logging
    ) -> Dict[str, Any]:
        """
        Process a user message and return response.

        Args:
            message: The user's new message
            history: List of previous messages in conversation
            user_id: ID of the user
            conversation_id: ID of the conversation

        Returns:
            {
                "response": "Agent's response text",
                "tool_calls": [
                    {
                        "tool_name": "WebSearch",
                        "parameters": {"query": "..."},
                        "result": {"data": [...]}
                    }
                ],
                "metadata": {
                    "model": "claude-3-sonnet",
                    "tokens_used": 1234,
                    "reasoning": "..."
                }
            }
        """
        pass
```

---

## Integration Options

### Option 1: Claude AI (Recommended)

Using Claude as your agent via the Anthropic API:

#### Setup

```bash
# 1. Install dependencies
pip install anthropic

# 2. Set API key
export ANTHROPIC_API_KEY=your-key-here
```

#### Implementation

Create `agent_service/agent.py`:

```python
import asyncio
import json
from typing import List, Dict, Any
from anthropic import Anthropic

class ClaudeAgent:
    """Claude-powered agent for chat"""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        self.client = Anthropic()
        self.model = model

    def process_message(
        self,
        message: str,
        history: List[Dict[str, Any]],
        user_id: str = None,
        conversation_id: str = None
    ) -> Dict[str, Any]:
        """Process message with Claude"""

        try:
            # Format conversation history for Claude
            messages = []
            for msg in history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            # Add new user message
            messages.append({
                "role": "user",
                "content": message
            })

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system="You are a helpful AI assistant.",
                messages=messages
            )

            # Extract response
            assistant_message = response.content[0].text

            return {
                "response": assistant_message,
                "tool_calls": [],  # Claude tool use would go here
                "metadata": {
                    "model": self.model,
                    "tokens_used": response.usage.output_tokens,
                    "stop_reason": response.stop_reason
                }
            }

        except Exception as e:
            return {
                "response": f"Error: {str(e)}",
                "tool_calls": [],
                "metadata": {"error": str(e)}
            }

# Global agent instance
agent = ClaudeAgent()
```

### Option 2: Local LLM (Ollama)

Using Ollama for local inference:

#### Setup

```bash
# 1. Install Ollama
# https://ollama.ai

# 2. Pull a model
ollama pull mistral

# 3. Start Ollama server
ollama serve
```

#### Implementation

Create `agent_service/agent.py`:

```python
import requests
import json
from typing import List, Dict, Any

class OllamaAgent:
    """Local LLM agent using Ollama"""

    def __init__(self, model: str = "mistral", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def process_message(
        self,
        message: str,
        history: List[Dict[str, Any]],
        user_id: str = None,
        conversation_id: str = None
    ) -> Dict[str, Any]:
        """Process message with local LLM"""

        try:
            # Format conversation
            prompt = "You are a helpful AI assistant.\n\n"

            for msg in history:
                role = "User" if msg["role"] == "user" else "Assistant"
                prompt += f"{role}: {msg['content']}\n"

            prompt += f"User: {message}\nAssistant: "

            # Call Ollama API
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=30
            )

            if response.status_code != 200:
                raise Exception(f"Ollama error: {response.text}")

            result = response.json()

            return {
                "response": result.get("response", "").strip(),
                "tool_calls": [],
                "metadata": {
                    "model": self.model,
                    "eval_count": result.get("eval_count", 0),
                    "eval_duration": result.get("eval_duration", 0)
                }
            }

        except Exception as e:
            return {
                "response": f"Error: {str(e)}",
                "tool_calls": [],
                "metadata": {"error": str(e)}
            }

agent = OllamaAgent()
```

### Option 3: Mock Agent (for Testing)

For development and testing:

#### Implementation

Create `agent_service/agent.py`:

```python
from typing import List, Dict, Any
import time

class MockAgent:
    """Mock agent for testing"""

    def __init__(self):
        self.response_map = {
            "hello": "Hello! How can I help you today?",
            "what can you do": "I can help with:\n- Answering questions\n- Writing code\n- Explaining concepts\n- And much more!",
            "count to 10": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
        }

    def process_message(
        self,
        message: str,
        history: List[Dict[str, Any]],
        user_id: str = None,
        conversation_id: str = None
    ) -> Dict[str, Any]:
        """Process message with mock agent"""

        # Simulate processing time
        time.sleep(0.5)

        # Look up response
        response = self.response_map.get(
            message.lower(),
            f"You said: {message}. How can I help?"
        )

        return {
            "response": response,
            "tool_calls": [],
            "metadata": {
                "model": "mock",
                "processing_time_ms": 500
            }
        }

agent = MockAgent()
```

---

## Installation Steps

### Step 1: Create Agent Service Directory

```bash
mkdir -p backend/agent_service
touch backend/agent_service/__init__.py
```

### Step 2: Create Agent Implementation

Choose one of the options above and save as `backend/agent_service/agent.py`

### Step 3: Update Backend Imports

The chat API will automatically import the agent if available:

```python
# Already in backend/src/api/chat.py
try:
    from agent_service.agent import agent
except ImportError:
    agent = None
```

### Step 4: Configure Environment (if using Claude)

```bash
# For Claude API
export ANTHROPIC_API_KEY=sk-ant-...

# For Ollama (default is http://localhost:11434)
export OLLAMA_BASE_URL=http://localhost:11434
```

### Step 5: Start the Backend

```bash
cd backend
python -m uvicorn src.main:app --reload
```

### Step 6: Test the Agent

```bash
# Send a test message
curl -X POST http://localhost:8000/api/test-user/chat \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, what can you do?"}'
```

---

## Running the Agent

### Option A: Claude API (Production Recommended)

```bash
# 1. Set API key
export ANTHROPIC_API_KEY=your-key

# 2. Start backend
cd backend
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000

# 3. Agent is now running and handling requests
```

### Option B: Ollama (Local LLM)

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start backend
cd backend
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000

# Agent is now running with local model
```

### Option C: Mock Agent (Testing)

```bash
# Start backend with mock agent (built-in)
cd backend
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000

# Agent will respond with mock responses
```

---

## Testing the Agent Integration

### Test 1: Simple Message

```bash
curl -X POST http://localhost:8000/api/user-123/chat \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! How are you?"
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "conversation_id": "conv-abc123",
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "Hello! How are you?",
      "created_at": "2026-02-03T10:30:00Z",
      "tool_calls": []
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "I'm doing well, thank you for asking!",
      "created_at": "2026-02-03T10:30:05Z",
      "tool_calls": []
    }
  ]
}
```

### Test 2: Multi-turn Conversation

```bash
# First message
curl -X POST http://localhost:8000/api/user-123/chat \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is AI?"}'

# Get conversation ID from response
CONV_ID=conv-abc123

# Second message (same conversation)
curl -X POST http://localhost:8000/api/user-123/chat \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Tell me more\",
    \"conversation_id\": \"$CONV_ID\"
  }"
```

### Test 3: Load Test

```bash
# Load test with 10 concurrent messages
locust -f load_test.py --users 10 --spawn-rate 1 --run-time 5m
```

---

## Agent Requirements Summary

| Requirement | Details |
|-------------|---------|
| **Response Time** | < 30 seconds (configurable) |
| **Input Format** | String (message) + List[Dict] (history) |
| **Output Format** | Dict with "response" key |
| **Error Handling** | Return error message in response |
| **Async Support** | Optional (runs in thread) |
| **Tool Support** | Optional (for future enhancement) |

---

## Common Issues

### Issue: "Agent service not available"

**Problem**: Import of agent fails
**Solution**:
```python
# Check agent file exists at:
backend/agent_service/agent.py

# Verify __init__.py exists:
backend/agent_service/__init__.py

# Check import is correct:
from agent_service.agent import agent
```

### Issue: Agent takes too long (timeout)

**Problem**: Agent response > 30 seconds
**Solution**:
```bash
# Increase timeout in config
export AGENT_TIMEOUT_SECONDS=60

# Or in backend/src/config.py:
AGENT_TIMEOUT_SECONDS = 60
```

### Issue: API Key not working

**Problem**: Anthropic/Ollama authentication fails
**Solution**:
```bash
# For Claude
export ANTHROPIC_API_KEY=sk-ant-your-actual-key

# For Ollama, check service is running
curl http://localhost:11434/api/tags

# Should return available models
```

### Issue: Agent returns empty response

**Problem**: Agent crashes silently
**Solution**:
```python
# Add error logging to agent
import logging
logger = logging.getLogger(__name__)

try:
    # agent code
except Exception as e:
    logger.error(f"Agent error: {e}", exc_info=True)
    raise
```

---

## Advanced Configuration

### Custom System Prompt

```python
class CustomAgent:
    def __init__(self):
        self.system_prompt = """You are a specialized AI assistant for...

        Your capabilities include:
        - Feature 1
        - Feature 2
        - Feature 3

        Always be helpful and accurate."""

    def process_message(self, message, history, user_id=None, conversation_id=None):
        # Use self.system_prompt when calling LLM
        pass
```

### Tool Integration

```python
def process_message(self, message, history, user_id=None, conversation_id=None):
    # Get response from LLM
    response = self.llm.call(...)

    # Extract tool calls if present
    tool_calls = self.extract_tool_calls(response)

    return {
        "response": response.text,
        "tool_calls": [
            {
                "tool_name": "WebSearch",
                "parameters": {"query": "..."},
                "result": {"data": [...]}
            }
        ]
    }
```

### Monitoring & Logging

```python
import time
import logging

logger = logging.getLogger(__name__)

def process_message(self, message, history, user_id=None, conversation_id=None):
    start_time = time.time()

    try:
        response = self.llm.call(...)
        duration = time.time() - start_time

        logger.info(
            f"Agent response for user {user_id}",
            extra={
                "conversation_id": conversation_id,
                "duration_ms": duration * 1000,
                "tokens_used": response.usage.output_tokens
            }
        )

        return {
            "response": response.text,
            "tool_calls": [],
            "metadata": {
                "duration_ms": duration * 1000,
                "tokens_used": response.usage.output_tokens
            }
        }
    except Exception as e:
        logger.error(f"Agent error: {e}", exc_info=True)
        raise
```

---

## Production Deployment

### Docker Setup

Create `Dockerfile.agent`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy agent service
COPY backend/agent_service ./agent_service
COPY backend/src ./src

# Set environment
ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
ENV PYTHONUNBUFFERED=1

# Start backend with agent
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -f Dockerfile.agent -t chat-agent .
docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY chat-agent
```

---

## Summary

**To get the agent running:**

1. **Choose an agent type** (Claude, Ollama, or Mock)
2. **Create `backend/agent_service/agent.py`** with your implementation
3. **Set environment variables** (API keys, etc.)
4. **Start the backend** - agent integration is automatic
5. **Test with curl or the frontend**

The chat API will automatically use the agent once it's available. The system is designed to work with any agent that implements the `process_message` interface.

---

**Status**: Ready to integrate your agent 🚀
