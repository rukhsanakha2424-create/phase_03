"""Sample natural language commands for testing.

Provides 50+ test input variations for each tool to validate
NL interpretation accuracy and parameter extraction.
"""

from typing import Any


class SampleCommands:
    """Sample NL commands organized by tool/intent."""

    # Add task command variations
    ADD_TASK_COMMANDS = [
        ("Add task: Buy groceries", {"title": "Buy groceries"}),
        ("Create task: Review PR #42", {"title": "Review PR #42"}),
        ("New task - Fix login bug", {"title": "Fix login bug"}),
        ("Add: Call the dentist", {"title": "Call the dentist"}),
        ("Create a task called 'Water plants'", {"title": "Water plants"}),
        ("I need to pay the bills", {"title": "pay the bills"}),
        ("Remind me to check email", {"title": "check email"}),
        ("Don't forget to buy milk", {"title": "buy milk"}),
        ("Add 'Schedule meeting'", {"title": "Schedule meeting"}),
        ("Create: Update documentation", {"title": "Update documentation"}),
        ("New task: Deploy to production", {"title": "Deploy to production"}),
        ("Add task - Clean the office", {"title": "Clean the office"}),
        ("I should call mom", {"title": "call mom"}),
        ("Remind me to submit the report", {"title": "submit the report"}),
        ("Create 'Book vacation'", {"title": "Book vacation"}),
    ]

    # List tasks command variations
    LIST_TASKS_COMMANDS = [
        ("List my tasks", {"status": "all"}),
        ("List tasks", {"status": "all"}),
        ("Show my tasks", {"status": "all"}),
        ("What are my tasks?", {"status": "all"}),
        ("Show my task list", {"status": "all"}),
        ("View all tasks", {"status": "all"}),
        ("What do I have to do?", {"status": "all"}),
        ("List pending tasks", {"status": "pending"}),
        ("Show pending tasks", {"status": "pending"}),
        ("What tasks are pending?", {"status": "pending"}),
        ("What's left to do?", {"status": "pending"}),
        ("Show incomplete tasks", {"status": "pending"}),
        ("List completed tasks", {"status": "completed"}),
        ("Show done tasks", {"status": "completed"}),
        ("What tasks are done?", {"status": "completed"}),
        ("Show finished tasks", {"status": "completed"}),
        ("List my completed tasks", {"status": "completed"}),
        ("What have I finished?", {"status": "completed"}),
    ]

    # Complete task command variations
    COMPLETE_TASK_COMMANDS = [
        ("Mark task 1 as done", {"task_id": "1"}),
        ("Complete task 2", {"task_id": "2"}),
        ("Mark task #3 complete", {"task_id": "3"}),
        ("Finish task 5", {"task_id": "5"}),
        ("Check off task 4", {"task_id": "4"}),
        ("Done with task 1", {"task_id": "1"}),
        ("I finished task 2", {"task_id": "2"}),
        ("Complete the groceries task", {"task_id": "Buy groceries"}),
        ("Mark 'Call mom' as done", {"task_id": "Call mom"}),
        ("Finish 'Review PR'", {"task_id": "Review PR"}),
        ("Complete task #10", {"task_id": "10"}),
        ("Done! Mark task 5 complete", {"task_id": "5"}),
        ("Mark the first one done", {"task_id": "first"}),
        ("Complete task 'Buy groceries'", {"task_id": "Buy groceries"}),
        ("I'm done with task 3", {"task_id": "3"}),
    ]

    # Update task command variations
    UPDATE_TASK_COMMANDS = [
        ("Update task 1 to 'Buy milk'", {"task_id": "1", "title": "Buy milk"}),
        ("Change task 2 to 'Review PR #50'", {"task_id": "2", "title": "Review PR #50"}),
        ("Edit task 3: Make it high priority", {"task_id": "3"}),
        ("Update task #5 to 'Call dentist Friday'", {"task_id": "5", "title": "Call dentist Friday"}),
        ("Rename task 1 to 'Go to store'", {"task_id": "1", "title": "Go to store"}),
        ("Change task 2", {"task_id": "2"}),
        ("Update task 'Buy groceries' to 'Buy organic groceries'", {"task_id": "Buy groceries", "title": "Buy organic groceries"}),
        ("Edit task #1 description", {"task_id": "1"}),
        ("Modify task 3 to add urgency", {"task_id": "3"}),
        ("Update task 4: 'New description here'", {"task_id": "4"}),
    ]

    # Delete task command variations
    DELETE_TASK_COMMANDS = [
        ("Delete task 1", {"task_id": "1"}),
        ("Remove task 2", {"task_id": "2"}),
        ("Delete task #5", {"task_id": "5"}),
        ("Remove task #3", {"task_id": "3"}),
        ("Get rid of task 4", {"task_id": "4"}),
        ("Delete the old task", {"task_id": "old"}),
        ("Remove 'Buy groceries'", {"task_id": "Buy groceries"}),
        ("Delete 'Meeting at 3pm'", {"task_id": "Meeting at 3pm"}),
        ("Get rid of task 'Call mom'", {"task_id": "Call mom"}),
        ("Delete task 1", {"task_id": "1"}),
    ]

    # Edge cases and special scenarios
    EDGE_CASE_COMMANDS = [
        # Ambiguous
        ("Task 5", {}),
        ("It", {}),
        ("That one", {}),
        # Multi-step
        ("List my tasks and mark the first one done", {}),
        ("Show completed tasks and create a new task", {}),
        # Malformed
        ("   add   task   :   buy milk   ", {"title": "buy milk"}),
        ("ADD TASK: BUY MILK", {"title": "BUY MILK"}),
        ("AdD tAsK: Mix Case", {"title": "Mix Case"}),
        # Empty/minimal
        ("Add", {}),
        ("List", {"status": "all"}),
        # Very long title
        ("Add task: " + "x" * 300, {}),  # Should be truncated
    ]

    @staticmethod
    def get_all_add_task_commands() -> list[tuple[str, dict[str, Any]]]:
        """Get all add_task test commands."""
        return SampleCommands.ADD_TASK_COMMANDS

    @staticmethod
    def get_all_list_tasks_commands() -> list[tuple[str, dict[str, Any]]]:
        """Get all list_tasks test commands."""
        return SampleCommands.LIST_TASKS_COMMANDS

    @staticmethod
    def get_all_complete_task_commands() -> list[tuple[str, dict[str, Any]]]:
        """Get all complete_task test commands."""
        return SampleCommands.COMPLETE_TASK_COMMANDS

    @staticmethod
    def get_all_update_task_commands() -> list[tuple[str, dict[str, Any]]]:
        """Get all update_task test commands."""
        return SampleCommands.UPDATE_TASK_COMMANDS

    @staticmethod
    def get_all_delete_task_commands() -> list[tuple[str, dict[str, Any]]]:
        """Get all delete_task test commands."""
        return SampleCommands.DELETE_TASK_COMMANDS

    @staticmethod
    def get_all_commands() -> dict[str, list[tuple[str, dict[str, Any]]]]:
        """Get all test commands organized by intent."""
        return {
            "add_task": SampleCommands.ADD_TASK_COMMANDS,
            "list_tasks": SampleCommands.LIST_TASKS_COMMANDS,
            "complete_task": SampleCommands.COMPLETE_TASK_COMMANDS,
            "update_task": SampleCommands.UPDATE_TASK_COMMANDS,
            "delete_task": SampleCommands.DELETE_TASK_COMMANDS,
            "edge_cases": SampleCommands.EDGE_CASE_COMMANDS,
        }
