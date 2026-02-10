"""CLI entry point for the Todo application.

Phase I: In-memory only, no persistence.
"""

import argparse
import sys
from src.core.service import TaskService


def main() -> None:
    """Main entry point for the todo CLI."""
    service = TaskService()

    parser = argparse.ArgumentParser(
        prog="todo",
        description="A simple in-memory todo list CLI application",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task description")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("description", help="New task description")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    try:
        if args.command == "add":
            task = service.add(args.description)
            print(f"Added task {task.id}: {task.description}")

        elif args.command == "list":
            tasks = service.list()
            if not tasks:
                print("No tasks yet. Add one with 'todo add \"Your task\"'")
            else:
                for task in tasks:
                    status = "[x]" if task.completed else "[ ]"
                    print(f"{task.id}. {status} {task.description}")

        elif args.command == "update":
            task = service.update(args.id, args.description)
            print(f"Updated task {task.id}: {task.description}")

        elif args.command == "delete":
            if service.delete(args.id):
                print(f"Deleted task {args.id}")
            else:
                print(f"Error: Task {args.id} not found")

        elif args.command == "complete":
            task = service.complete(args.id)
            status = "completed" if task.completed else "uncompleted"
            print(f"Task {task.id} marked as {status}: {task.description}")

    except KeyError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
