---
id: 0004
title: interactive-menu-driven-todo
stage: implement
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-todo-in-memory
user: null
command: sp.implement
labels: ["interactive","menu-driven","console"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - main.py
tests:
 - None
---

## Prompt

# Research – In-Memory Todo CLI

Phase-I focuses on a stateless, in-memory CLI todo application.

- Tasks exist only during a single execution
- No persistence across commands
- Suitable for validating CLI structure and command behavior

You are building Phase-I of a Todo Application.

Build an INTERACTIVE, MENU-DRIVEN, IN-MEMORY Python Console Application.

STRICT RULES:
- In-memory only (NO files, NO database)
- Data must persist ONLY while the program is running
- Once user exits, all data is lost
- Single Python entry file
- Clean, readable code
- No external libraries

=== APPLICATION BEHAVIOR ===

On start, show this menu repeatedly until Exit is chosen:

--- Todo Application ---
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit
-------------------------
Enter your choice (1–7):

=== TASK RULES ===
- Each task has:
  - ID (incremental starting from 1)
  - Description (string)
  - Completed status (True / False)

=== OUTPUT FORMAT ===

When viewing tasks, display exactly like this:

--- All Tasks ---
1. [ ] Buy milk
2. [x] Learn Python
-----------------

[ ] = incomplete
[x] = completed

=== FEATURE DETAILS ===

1. Add Task
   - Ask for task description
   - Add to in-memory list
   - Confirm with message: "Task added successfully"

2. View All Tasks
   - Show all tasks
   - If no tasks: "No tasks available"

3. Update Task
   - Ask for Task ID
   - Ask for new description
   - Update task
   - Validate ID

4. Delete Task
   - Ask for Task ID
   - Remove task
   - Validate ID

5. Mark Task Complete
   - Ask for Task ID
   - Set completed = True

6. Mark Task Incomplete
   - Ask for Task ID
   - Set completed = False

7. Exit
   - Print "Goodbye!"
   - Stop program

=== ERROR HANDLING ===
- Invalid menu choice → show error and re-show menu
- Invalid Task ID → show error and re-show menu
- Empty input not allowed

=== IMPORTANT ===
- Use a loop so menu appears after every action
- This is Phase-I only
- NO CLI arguments
- NO persistence
- NO advanced features

Deliver:
- Fully working Python code
- Ready to run with: `python main.py`

## Response snapshot

Created `main.py` with complete interactive menu-driven todo application:

**Features Implemented:**
1. **Add Task** - Prompts for description, adds to in-memory list, confirms success
2. **View All Tasks** - Displays tasks with `[ ]` for incomplete, `[x]` for completed
3. **Update Task** - Shows tasks, prompts for ID and new description
4. **Delete Task** - Shows tasks, prompts for ID, removes task
5. **Mark Complete** - Shows tasks, prompts for ID, sets completed=True
6. **Mark Incomplete** - Shows tasks, prompts for ID, sets completed=False
7. **Exit** - Prints "Goodbye!" and exits loop

**Error Handling:**
- Invalid menu choice → "Error: Invalid choice. Please enter a number between 1 and 7"
- Invalid/empty Task ID → "Error: Invalid Task ID" or "Error: Task ID cannot be empty"
- Task not found → "Error: Task {id} not found"
- Empty description → "Error: Description cannot be empty"
- No tasks available → "No tasks available"

**Implementation Details:**
- Single file `main.py` (115 lines)
- Uses `dataclass` for Task model (id, description, completed)
- `TodoApp` class manages `List[Task]` in memory
- Incremental IDs starting from 1
- Menu loop re-displays after every action
- No external libraries (standard library only)
- Type hints with `Task | None` (Python 3.10+)

**Testing Results:**
- Empty task list displays "No tasks available"
- Adding task works: "Task added successfully"
- Viewing shows correct format: "1. [ ] Buy milk"
- Exit prints "Goodbye!"

## Outcome

- ✅ Impact: Created interactive, menu-driven todo application per specifications
- 🧪 Tests: Manual testing completed for empty list, add task, view, exit workflows
- 📁 Files: Created `main.py` (115 lines, clean, readable)
- 🔁 Next prompts: Ready to run with `python main.py`
- 🧠 Reflection: Note - This is a different approach from the existing CLI-based implementation (src/cli/main.py). Both exist in the codebase: this is a menu-driven REPL, while the other is argparse-based CLI with single commands.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Manual testing successful
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None - application complete per requirements
