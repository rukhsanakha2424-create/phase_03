# Agent Service

Natural language interpreter for todo commands using OpenAI Agents SDK and MCP protocol.

## Overview

The Agent Service processes natural language instructions from users and invokes MCP tools (from Spec 006) to manage tasks. It supports:

- Creating tasks with "add task", "create", etc.
- Listing tasks with filtering
- Completing tasks
- Updating task details
- Deleting tasks with confirmation

## Quick Start

### Setup

1. Clone and navigate to this directory:
```bash
cd agent-service
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key and MCP endpoint
```

5. Run tests:
```bash
pytest
```

## Usage

```python
from src.agent import TodoAgent
from src.config import get_config

config = get_config()
agent = TodoAgent(config)

response = agent.process_message("Add task: Buy groceries")
print(response)
```

## Architecture

- **Agent Core** (`src/agent.py`): Main agent class that processes messages
- **Tools** (`src/tools/`): Tool definitions and MCP integration
- **Prompts** (`src/prompts/`): System prompts and response templates
- **Handlers** (`src/handlers/`): Intent classification and parameter extraction
- **Tests** (`tests/`): Unit and integration tests

## Project Structure

```
agent-service/
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── agent.py            # Main agent class
│   ├── tools/              # Tool definitions and invoker
│   ├── prompts/            # System prompts and templates
│   └── handlers/           # Intent and parameter handlers
├── tests/
│   ├── __init__.py
│   ├── fixtures/           # Test data and mocks
│   ├── conftest.py         # Pytest configuration
│   └── test_*.py           # Test modules
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
├── pyproject.toml         # Project configuration
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Configuration

Required environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `MCP_TOOL_ENDPOINT`: HTTP endpoint for MCP tools (e.g., http://localhost:8000)

Optional:

- `USER_ID`: User identifier (default: "default-user")
- `AGENT_MODEL`: OpenAI model to use (default: "gpt-4")
- `MAX_RETRIES`: Retry attempts for tool calls (default: 2)
- `TIMEOUT_SECONDS`: Request timeout (default: 30)

## Testing

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_add_task_agent.py -v
```

Run with coverage:
```bash
pytest --cov=src
```

## Troubleshooting

### Import errors
Ensure you're in the virtual environment and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Configuration errors
Check that `.env` file exists with valid OpenAI API key:
```bash
cp .env.example .env
# Edit with your actual credentials
```

### MCP connection errors
Verify the MCP server is running at `MCP_TOOL_ENDPOINT`:
```bash
curl http://localhost:8000/health
```

## Implementation Status

- Phase 1: Setup & Project Initialization (T001-T012)
- Phase 2: Foundational Infrastructure (T013-T027)
- Phase 3: User Stories 1-3 - MVP (T028-T053)
- Phase 4: User Stories 4-6 - Extended (T054-T080)

See `specs/007-agent-tool-selection/tasks.md` for detailed task breakdown.

## Dependencies

See `requirements.txt` and `pyproject.toml` for complete dependency list.

## License

MIT
