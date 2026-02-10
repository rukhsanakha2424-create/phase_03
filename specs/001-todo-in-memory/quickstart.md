# Quickstart: Todo In-Memory CLI

**Feature**: 001-todo-in-memory | **Date**: 2026-01-03

## Installation

```bash
# Clone the repository
cd todo-app

# Install dependencies (if any)
pip install -e .
```

## Usage

### Add a Task
```bash
python -m src.cli.main add "Buy groceries"
```

### List All Tasks
```bash
python -m src.cli.main list
```

### Update a Task
```bash
python -m src.cli.main update 1 "Buy groceries and milk"
```

### Complete a Task
```bash
python -m src.cli.main complete 1
```

### Delete a Task
```bash
python -m src.cli.main delete 1
```

## Full Workflow Example

```bash
# Add tasks
python -m src.cli.main add "Learn Python"
python -m src.cli.main add "Build a todo app"
python -m src.cli.main add "Write tests"

# List tasks
python -m src.cli.main list

# Complete first task
python -m src.cli.main complete 1

# Update second task
python -m src.cli.main update 2 "Build an awesome todo app"

# Delete third task
python -m src.cli.main delete 3

# List remaining tasks
python -m src.cli.main list
```

## Exit Codes

- `0`: Success
- `1`: User error (invalid input, task not found, etc.)
- `2`: System error (unexpected failure)
