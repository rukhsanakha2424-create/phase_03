"""Integration tests for the add command CLI interface.

Phase I: In-memory only, no persistence, no priority.
Each CLI invocation is stateless - creates fresh TaskService.
"""
import pytest
import sys
import os

# Get project root directory (parent of tests/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add src to path for imports
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))


class TestAddCommand:
    """Integration tests for 'todo add' command."""

    def test_add_basic_task(self, capsys):
        """Test adding a basic task."""
        from cli.main import main

        original_argv = sys.argv
        sys.argv = ["todo", "add", "Buy milk"]
        try:
            main()
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        assert "Added task 1: Buy milk" in captured.out
        assert captured.err == ""

    def test_add_empty_description_fails(self, capsys):
        """Test that adding a task with empty description fails."""
        from cli.main import main

        original_argv = sys.argv
        sys.argv = ["todo", "add", ""]
        try:
            with pytest.raises(SystemExit):
                main()
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        assert "Description cannot be empty" in captured.out

    def test_add_whitespace_description_fails(self, capsys):
        """Test that adding a task with whitespace-only description fails."""
        from cli.main import main

        original_argv = sys.argv
        sys.argv = ["todo", "add", "   "]
        try:
            with pytest.raises(SystemExit):
                main()
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        assert "Description cannot be empty" in captured.out

    def test_add_task_with_spaces_in_description(self, capsys):
        """Test adding a task with spaces in description."""
        from cli.main import main

        original_argv = sys.argv
        sys.argv = ["todo", "add", "Buy groceries and milk"]
        try:
            main()
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        assert "Added task 1: Buy groceries and milk" in captured.out

    def test_add_long_description(self, capsys):
        """Test adding a task with a long description."""
        from cli.main import main

        long_desc = "A" * 500  # 500 character description

        original_argv = sys.argv
        sys.argv = ["todo", "add", long_desc]
        try:
            main()
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        assert f"Added task 1: {long_desc}" in captured.out

    def test_add_special_characters(self, capsys):
        """Test adding a task with special characters."""
        from cli.main import main

        original_argv = sys.argv
        sys.argv = ["todo", "add", "Task with $pecial ch@racters!"]
        try:
            main()
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        assert "Added task 1: Task with $pecial ch@racters!" in captured.out
