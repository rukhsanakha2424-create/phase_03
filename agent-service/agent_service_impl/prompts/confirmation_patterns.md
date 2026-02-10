# Confirmation & Response Templates

User-friendly response templates for different scenarios.

## Success Responses

### add_task Success
```
Got it! I've added '{title}' to your tasks.
```

Variations:
- "Added! '{title}' is now on your list."
- "Perfect! I've created the task '{title}'."
- "Done! '{title}' has been added to your tasks."

### list_tasks Success (with tasks)
```
You have {count} {status} task(s):

{numbered_list}
```

Example:
```
You have 3 pending tasks:

1. Buy groceries
2. Fix login bug
3. Review PR #42
```

### list_tasks Success (no tasks)
```
You have no {status} tasks. Great job!
```

Example:
```
You have no pending tasks. Great job!
```

### complete_task Success
```
Great! I've marked '{title}' as done.
```

Variations:
- "Done! '{title}' is now complete."
- "Excellent! '{title}' is marked as finished."

### update_task Success
```
Updated! I've changed {field} to '{new_value}'.
```

Example:
```
Updated! I've changed the title to 'Buy milk instead'.
```

### delete_task Confirmation Request
```
Are you sure you want to delete '{title}'? This can't be undone.
Please reply "yes" or "confirm" to delete, or "no"/"cancel" to keep it.
```

### delete_task Confirmed
```
Done! I've deleted '{title}' from your tasks.
```

## Error Responses

### Validation Error: Title Too Long
```
I couldn't create the task because the title is too long (currently {length}, max 255 characters).
Could you make it shorter? For example: '{suggested_shorter_title}'
```

### Validation Error: Missing Title
```
I need a task title to create it. What should the task be?
```

### Not Found Error
```
I couldn't find that task. Would you like me to show your tasks so you can pick the right one?
```

### Tool Connection Error
```
I'm having trouble connecting to the task service. Could you try again in a moment?
```

### Ambiguous Task Reference
```
I found multiple tasks that could match. Which one did you mean?

1. '{task1_title}'
2. '{task2_title}'
3. '{task3_title}'

(You can say the number or the full task name)
```

## Clarification Requests

### Clarify Intent
```
I'm not quite sure what you'd like to do. Did you mean:
- Create a new task
- Look at your task list
- Mark a task complete

Let me know!
```

### Clarify Task Reference
```
I found a few tasks that could match '{input}':

1. '{task1}' (created yesterday)
2. '{task2}' (from last week)

Which one did you mean?
```

### Clarify Update Field
```
For '{task_title}', what would you like to change?
- The title
- The description

Let me know!
```

## Multi-Step Workflow Responses

### Step 1 Complete, Step 2 In Progress
```
Got it! I've added '{title}' to your tasks. Now showing your task list...
```

### Multi-Step Summary
```
All done! Here's what I did:
1. Added 'Buy groceries' ✓
2. Listed your pending tasks (3 total) ✓
```

### Partial Failure
```
I added 'Buy groceries' successfully, but I had trouble listing your tasks.
Would you like me to try again?
```

## Response Format Rules

1. **Keep it brief**: 1-2 sentences for simple operations
2. **Use task names**: Reference the exact task title for clarity
3. **Be friendly**: Use warm, conversational tone
4. **Suggest fixes**: When there's an error, offer a solution
5. **Show context**: For list operations, show the results clearly
6. **Confirm destructive actions**: Always confirm before delete

## Dynamic Fields

```
{title}                  - The task title/name
{description}            - The task description
{count}                  - Number of tasks
{status}                 - "pending" or "completed"
{field}                  - Field being updated ("title" or "description")
{new_value}              - New value for field
{length}                 - Current length (for validation errors)
{numbered_list}          - Formatted list of tasks (1. Task 1, 2. Task 2, ...)
{task1_title}            - First matching task title
{task2_title}            - Second matching task title
{suggested_shorter_title} - Suggested shorter version of title
{error_code}             - Machine-readable error code
```

## Error Code Mapping

| Error Code | User Message |
|-----------|--------------|
| validation_error | "I couldn't create that task because..." |
| not_found | "I couldn't find that task..." |
| invocation_error | "I'm having trouble connecting..." |
| timeout | "That took too long. Let me try again..." |
| unauthorized | "I don't have permission to do that." |
| unknown_error | "Something unexpected happened..." |
