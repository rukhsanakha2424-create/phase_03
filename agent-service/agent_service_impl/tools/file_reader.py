"""File reading tool for the AI agent."""

import os
import logging
from pathlib import Path
from typing import Optional
from agent_service_impl.config import Config

logger = logging.getLogger(__name__)


def read_file_content(file_path: str, config: Config) -> dict:
    """Read the content of a specified file.
    
    Args:
        file_path: Path to the file to read (relative to project root)
        config: Configuration object
        
    Returns:
        Dictionary with keys:
        - status: "success" or "error"
        - content: File content (if successful)
        - error: Error message (if failed)
    """
    try:
        # Sanitize the file path to prevent directory traversal
        sanitized_path = Path(file_path).resolve()
        project_root = Path(config.PROJECT_ROOT if hasattr(config, 'PROJECT_ROOT') else os.getcwd())
        
        # Ensure the file is within the project directory
        if not str(sanitized_path).startswith(str(project_root)):
            return {
                "status": "error",
                "error": "Access denied: File is outside project directory"
            }
        
        # Check if file exists
        if not sanitized_path.exists():
            return {
                "status": "error",
                "error": f"File does not exist: {file_path}"
            }
        
        # Check if it's a file (not a directory)
        if not sanitized_path.is_file():
            return {
                "status": "error",
                "error": f"Path is not a file: {file_path}"
            }
        
        # Read file content
        with open(sanitized_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return {
            "status": "success",
            "content": content
        }
        
    except UnicodeDecodeError:
        return {
            "status": "error",
            "error": f"Cannot read file: {file_path} (binary file or unsupported encoding)"
        }
    except PermissionError:
        return {
            "status": "error",
            "error": f"Permission denied: Cannot read file {file_path}"
        }
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return {
            "status": "error",
            "error": f"Error reading file: {str(e)}"
        }


def list_directory_contents(dir_path: str, config: Config) -> dict:
    """List the contents of a specified directory.
    
    Args:
        dir_path: Path to the directory to list (relative to project root)
        config: Configuration object
        
    Returns:
        Dictionary with keys:
        - status: "success" or "error"
        - contents: List of directory contents (if successful)
        - error: Error message (if failed)
    """
    try:
        # Sanitize the directory path to prevent directory traversal
        sanitized_path = Path(dir_path).resolve()
        project_root = Path(config.PROJECT_ROOT if hasattr(config, 'PROJECT_ROOT') else os.getcwd())
        
        # Ensure the directory is within the project directory
        if not str(sanitized_path).startswith(str(project_root)):
            return {
                "status": "error",
                "error": "Access denied: Directory is outside project directory"
            }
        
        # Check if directory exists
        if not sanitized_path.exists():
            return {
                "status": "error",
                "error": f"Directory does not exist: {dir_path}"
            }
        
        # Check if it's a directory (not a file)
        if not sanitized_path.is_dir():
            return {
                "status": "error",
                "error": f"Path is not a directory: {dir_path}"
            }
        
        # List directory contents
        contents = []
        for item in sanitized_path.iterdir():
            contents.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "path": str(item.relative_to(project_root))
            })
            
        return {
            "status": "success",
            "contents": contents
        }
        
    except PermissionError:
        return {
            "status": "error",
            "error": f"Permission denied: Cannot access directory {dir_path}"
        }
    except Exception as e:
        logger.error(f"Error listing directory {dir_path}: {str(e)}")
        return {
            "status": "error",
            "error": f"Error listing directory: {str(e)}"
        }