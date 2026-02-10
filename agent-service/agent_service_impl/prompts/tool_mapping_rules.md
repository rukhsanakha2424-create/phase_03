# Tool Mapping Rules: Natural Language to MCP Tools

Maps natural language patterns to MCP tool invocations.

## add_task Tool Mapping

**Intent Patterns** (high confidence):
- "add task", "add a task", "create task", "create a task"
- "new task", "i need to", "remind me to", "don't forget to"
- "add [title]", "create [title]", "new [title]"

**Example Variations**:
- "Add task: Buy groceries"
- "Create: Fix bug in login form"
- "New task - Review PR for backend"
- "I need to call the dentist"
- "Remind me to pay the bills"
- "Don't forget to water the plants"

**Parameter Extraction**:
- Title: Everything after "task:", "create:", or the main noun phrase
- Description: Any additional context or notes (optional)

## list_tasks Tool Mapping

**Intent Patterns** (high confidence):
- "list tasks", "list my tasks", "show tasks", "show my tasks"
- "what are my tasks", "task list", "view tasks"
- "pending tasks", "completed tasks", "show pending", "show completed"
- "what do i have to do", "what's left to do", "what's done"

**Example Variations**:
- "List my tasks"
- "Show pending tasks"
- "What are my tasks?"
- "Show me what's not done yet"
- "List completed tasks"
- "What's left to do?"

**Parameter Extraction**:
- Status: Infer from context
  - "pending", "not done", "remaining", "to do" → status="pending"
  - "completed", "done", "finished" → status="completed"
  - No status mentioned or "all" → status="all"

## complete_task Tool Mapping

**Intent Patterns** (high confidence):
- "complete [task]", "mark [task] done", "finish [task]"
- "check off [task]", "done with [task]", "i finished [task]"

**Example Variations**:
- "Mark task 5 as done"
- "Complete task: Buy groceries"
- "Check off the dentist appointment"
- "I finished reviewing the PR"
- "Done with the bug fix"
- "Mark 'Call mom' as complete"

**Parameter Extraction**:
- Task ID: Numeric ID or task title/partial match
- If title provided: May need to search/confirm which task

## update_task Tool Mapping

**Intent Patterns** (high confidence):
- "update [task]", "change [task]", "edit [task]"
- "update [task] to [new_value]", "rename [task]"
- "make [task] [attribute]" (e.g., "make it urgent")

**Example Variations**:
- "Update task 3: change to 'Buy milk'"
- "Change task 5 to 'Call dentist on Friday'"
- "Edit task 1 description to add more details"
- "Rename 'Go to store' to 'Go to grocery store'"
- "Make task 2 high priority"

**Parameter Extraction**:
- Task ID: Numeric ID or task reference
- Title: If updating name/title
- Description: If updating description
- Require at least one of title or description

## delete_task Tool Mapping

**Intent Patterns** (high confidence):
- "delete [task]", "remove [task]", "get rid of [task]"
- "delete task [id]", "remove task [title]"

**Example Variations**:
- "Delete task 2"
- "Remove the old task"
- "Get rid of task: 'Buy old cereal'"
- "Delete 'Meeting at 3pm'"

**Parameter Extraction**:
- Task ID: Numeric ID or task reference
- Always confirm before deletion (built into delete workflow)

## Ambiguous/Clarification Cases

### Case 1: Ambiguous Intent
**Input**: "Task 5"
**Clarification**: Ask "Do you want to complete task 5, update it, or delete it?"

### Case 2: Multiple Tasks Mentioned
**Input**: "Complete tasks 1, 3, and 5"
**Action**: Invoke complete_task three times (multi-step workflow)

### Case 3: Missing Identifiers
**Input**: "Mark the first one done"
**Action**: list_tasks → identify first task → complete_task

### Case 4: Implicit Context
**Input**: "Add to the list"
**Clarification**: Ask "What would you like to add?"

## Confidence Scoring

High Confidence (≥95%):
- Direct keywords present (add, create, list, complete, delete)
- Clear parameters provided
- Single unambiguous interpretation

Medium Confidence (80-94%):
- Indirect language but clear intent
- Parameters need inference from context
- Requires parameter validation before tool call

Low Confidence (<80%):
- Ambiguous language
- Multiple possible interpretations
- Ask for clarification before proceeding

## Tool Selection Decision Tree

```
User Message
├─ "add" OR "create" OR "new" OR "remind me" → add_task
├─ "list" OR "show" OR "view" OR "what are" → list_tasks
├─ "complete" OR "done" OR "finish" OR "mark" → complete_task
├─ "update" OR "change" OR "edit" → update_task
├─ "delete" OR "remove" OR "get rid" → delete_task
└─ None match → Ask for clarification
```
