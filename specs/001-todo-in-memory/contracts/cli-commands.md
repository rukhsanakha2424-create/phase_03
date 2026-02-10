# CLI Command Contracts

**Feature**: 001-todo-in-memory | **Date**: 2026-01-03
**Purpose**: Define the command-line interface for the todo application

## Overview

The todo application is invoked via `python -m src.cli.main` with argparse subcommands. Each command executes and terminates with output; no interactive sessions.

---

## Command: add

**Purpose**: Create a new task with the provided description

**Syntax**:
```bash
python -m src.cli.main add <description>
```

**Arguments**:
- `description` (required, positional): Task description text (any whitespace supported)

**Input Validation**:
- Must not be empty (argparse enforces at least one word)
- Max length: 1000 characters

**Success Output**:
```
Task added: [id] description
```

**Error Output**:
```
error: the following arguments are required: description
```

**Exit Codes**:
- `0`: Task successfully added
- `1`: Invalid input (empty description)

**Examples**:
```bash
$ python -m src.cli.main add Buy groceries
Task added: [1] Buy groceries

$ python -m src.cli.main add "Call mom at 5pm"
Task added: [2] Call mom at 5pm
```

---

## Command: list

**Purpose**: Display all tasks with their identifiers and completion status

**Syntax**:
```bash
python -m src.cli.main list
```

**Arguments**: None

**Input Validation**: None

**Success Output**:

When tasks exist:
```
  [1] Buy groceries
✓ [2] Call mom
  [3] Write report
```

When no tasks exist:
```
No tasks found.
```

**Exit Codes**:
- `0`: Successfully displayed task list

**Examples**:
```bash
$ python -m src.cli.main list
  [1] Buy groceries
✓ [2] Call mom
  [3] Write report

$ python -m src.cli.main list
No tasks found.
```

---

## Command: update

**Purpose**: Modify the description of an existing task

**Syntax**:
```bash
python -m src.cli.main update <id> <description>
```

**Arguments**:
- `id` (required, positional): Task identifier (integer)
- `description` (required, positional): New task description

**Input Validation**:
- `id` must be a valid integer
- `description` must not be empty
- `id` must correspond to an existing task

**Success Output**:
```
Task updated: [id] new description
```

**Error Outputs**:
```
error: argument id: invalid int value: 'abc'
```
```
Task with ID 99 not found
```

**Exit Codes**:
- `0`: Task successfully updated
- `1`: Invalid ID format or task not found

**Examples**:
```bash
$ python -m src.cli.main update 1 "Buy groceries and milk"
Task updated: [1] Buy groceries and milk

$ python -m src.cli.main update 99 "Invalid"
Task with ID 99 not found
```

---

## Command: delete

**Purpose**: Remove a task from the list

**Syntax**:
```bash
python -m src.cli.main delete <id>
```

**Arguments**:
- `id` (required, positional): Task identifier (integer)

**Input Validation**:
- `id` must be a valid integer
- `id` must correspond to an existing task

**Success Output**:
```
Task deleted: [id] description
```

**Error Outputs**:
```
error: argument id: invalid int value: 'abc'
```
```
Task with ID 99 not found
```

**Exit Codes**:
- `0`: Task successfully deleted
- `1`: Invalid ID format or task not found

**Examples**:
```bash
$ python -m src.cli.main delete 2
Task deleted: [2] Call mom

$ python -m src.cli.main delete 99
Task with ID 99 not found
```

---

## Command: complete

**Purpose**: Toggle the completion status of a task (mark complete/incomplete)

**Syntax**:
```bash
python -m src.cli.main complete <id>
```

**Arguments**:
- `id` (required, positional): Task identifier (integer)

**Input Validation**:
- `id` must be a valid integer
- `id` must correspond to an existing task

**Success Output**:
```
Task marked as complete: [id] description
```
or
```
Task marked as incomplete: [id] description
```

**Error Outputs**:
```
error: argument id: invalid int value: 'abc'
```
```
Task with ID 99 not found
```

**Exit Codes**:
- `0`: Task status successfully toggled
- `1`: Invalid ID format or task not found

**Examples**:
```bash
$ python -m src.cli.main complete 1
Task marked as complete: [1] Buy groceries

$ python -m src.cli.main complete 1
Task marked as incomplete: [1] Buy groceries

$ python -m src.cli.main complete 99
Task with ID 99 not found
```

---

## Global Behaviors

### Help Command
```bash
python -m src.cli.main -h
```
or
```bash
python -m src.cli.main <command> -h
```

### No Persistence
- All data is stored in memory only
- Tasks are lost when the process exits
- Each command execution is independent (no session state)

### Output Format Consistency
- All success messages include task ID
- All error messages are user-friendly (no technical jargon)
- Status indicators: `✓` for complete, ` ` (space) for incomplete
