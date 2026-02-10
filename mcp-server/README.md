# MCP Adapter for Todo Operations

A stateless MCP (Model Context Protocol) server that exposes todo task functionality as tools for AI agent invocation.

## Overview

This MCP Adapter provides 5 task management tools that agents can invoke:
- **add_task**: Create a new task with title and optional description
- **list_tasks**: Retrieve user's tasks with optional status filter
- **update_task**: Modify a task's title and/or description
- **complete_task**: Mark a task as completed
- **delete_task**: Remove a task from the database

All tools enforce user isolation via `user_id` and persist state to PostgreSQL.

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL (Neon Serverless or local instance)
- pip or poetry

### Setup

1. Clone the repository and navigate to the mcp-server directory:
```bash
cd mcp-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and set DATABASE_URL to your PostgreSQL connection string
```

4. (Optional) Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Project Structure

```
mcp-server/
├── src/
│   ├── main.py                    # MCP server entry point
│   ├── tools/
│   │   ├── add_task.py            # add_task tool handler
│   │   ├── list_tasks.py          # list_tasks tool handler
│   │   ├── update_task.py         # update_task tool handler
│   │   ├── complete_task.py       # complete_task tool handler
│   │   └── delete_task.py         # delete_task tool handler
│   ├── models/
│   │   ├── task.py                # Task SQLModel
│   │   └── schemas.py             # Pydantic schemas for tool I/O
│   ├── db/
│   │   └── connection.py          # PostgreSQL connection pool
│   └── errors/
│       └── handlers.py            # Error response utilities
├── tests/
│   ├── test_add_task.py
│   ├── test_list_tasks.py
│   ├── test_update_task.py
│   ├── test_complete_task.py
│   ├── test_delete_task.py
│   ├── test_integration_all_tools.py
│   ├── test_error_handling.py
│   ├── test_user_isolation.py
│   └── conftest.py                # pytest fixtures
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## Running the MCP Server

Start the server with:
```bash
python src/main.py
```

**Expected output:**
```
MCP Adapter Server starting...
Database connection pool initialized (min: 5, max: 20)
MCP server listening on stdio
Tools registered: add_task, list_tasks, update_task, complete_task, delete_task
Ready for agent connections
```

## Tool Contracts

### add_task
Create a new task for the authenticated user.

**Inputs:**
- `user_id` (string, required): Unique identifier of the user
- `title` (string, required): Task title (max 255 characters)
- `description` (string, optional): Task description

**Output:**
- `task_id` (integer): Unique task identifier
- `title` (string): Task title
- `status` (string): Task status (always "pending" for new tasks)
- `created_at` (string): ISO 8601 timestamp

**Errors:**
- "user_id is required"
- "Title is required"
- "Title must be 255 characters or less"
- "Database connection failed"

### list_tasks
Retrieve all tasks owned by the authenticated user.

**Inputs:**
- `user_id` (string, required): Unique identifier of the user
- `status` (string, optional): Filter by status ("all", "pending", "completed")

**Output:**
- `tasks` (array): List of task objects with id, title, description, status, created_at, updated_at

**Errors:**
- "user_id is required"
- "Invalid status filter. Must be 'all', 'pending', or 'completed'"
- "Database connection failed"

### update_task
Update an existing task's title and/or description.

**Inputs:**
- `user_id` (string, required): Unique identifier of the user
- `task_id` (integer, required): ID of the task to update
- `title` (string, optional): New task title (max 255 characters)
- `description` (string, optional): New task description

**Output:**
- `id` (integer): Task ID
- `title` (string): Updated title
- `status` (string): Task status (unchanged)
- `updated_at` (string): ISO 8601 timestamp

**Errors:**
- "user_id is required"
- "task_id must be an integer"
- "Title must be 255 characters or less"
- "Task not found or access denied"

### complete_task
Mark a task as completed.

**Inputs:**
- `user_id` (string, required): Unique identifier of the user
- `task_id` (integer, required): ID of the task to complete

**Output:**
- `id` (integer): Task ID
- `title` (string): Task title
- `status` (string): Task status ("completed")
- `updated_at` (string): ISO 8601 timestamp

**Errors:**
- "user_id is required"
- "task_id must be an integer"
- "Task not found or access denied"

### delete_task
Delete a task.

**Inputs:**
- `user_id` (string, required): Unique identifier of the user
- `task_id` (integer, required): ID of the task to delete

**Output:**
- `id` (integer): ID of the deleted task
- `status` (string): "deleted"

**Errors:**
- "user_id is required"
- "task_id must be an integer"
- "Task not found or access denied"

## Testing

Run the test suite:
```bash
# All tests
pytest

# Specific test file
pytest tests/test_add_task.py -v

# With coverage
pytest --cov=src --cov-report=html
```

## User Isolation

All tools enforce user isolation at the database level. A user can only see, modify, or delete their own tasks:

```python
# User A creates a task
add_task(user_id="userA", title="Task A")

# User B cannot see or modify User A's task
list_tasks(user_id="userB")  # Does not include Task A
update_task(user_id="userB", task_id=1)  # Returns "Task not found or access denied"
```

## Stateless Design

The MCP Adapter is stateless:
- No in-memory task state
- Each tool invocation acquires a database connection, executes, and releases
- Safe for horizontal scaling and concurrent requests
- Session interruption/restart does not lose state

## Performance

Target response times:
- **add_task**: < 100ms
- **list_tasks**: < 200ms (depending on task count)
- **update_task**: < 100ms
- **complete_task**: < 100ms
- **delete_task**: < 100ms

## Configuration

Environment variables:
- `DATABASE_URL`: PostgreSQL connection string (required)
- `DB_POOL_MIN_SIZE`: Minimum connection pool size (default: 5)
- `DB_POOL_MAX_SIZE`: Maximum connection pool size (default: 20)
- `DB_COMMAND_TIMEOUT`: Query timeout in seconds (default: 60)

## Development

For development with auto-reload and debugging:

1. Install dev dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest tests/ -v
```

3. Format code:
```bash
black src/ tests/
```

4. Lint:
```bash
ruff check src/ tests/
```

## Architecture

### Thin Wrapper Pattern
Each tool is a thin adapter over database operations:
1. Validate input parameters
2. Enforce user ownership (WHERE user_id = $user_id)
3. Execute SQL query via asyncpg
4. Return structured response or error

### Error Handling
All errors return structured JSON:
```json
{
  "error": "error_message"
}
```

### Connection Pooling
asyncpg connection pool with configurable min/max size enables:
- Efficient resource reuse across concurrent tool invocations
- Automatic connection management
- Graceful error handling on connection failures

## License

MIT

## Support

For issues or questions, see the project repository's issue tracker.
