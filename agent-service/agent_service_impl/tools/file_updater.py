"""File update tool for the AI agent."""

import os
import logging
from pathlib import Path
from typing import Optional
from agent_service_impl.config import Config

logger = logging.getLogger(__name__)


def update_file_content(file_path: str, content: str, config: Config) -> dict:
    """Update the content of a specified file.
    
    Args:
        file_path: Path to the file to update (relative to project root)
        content: New content for the file
        config: Configuration object
        
    Returns:
        Dictionary with keys:
        - status: "success" or "error"
        - message: Success or error message
    """
    try:
        # Sanitize the file path to prevent directory traversal
        sanitized_path = Path(file_path).resolve()
        project_root = Path(config.PROJECT_ROOT if hasattr(config, 'PROJECT_ROOT') else os.getcwd())
        
        # Ensure the file is within the project directory
        if not str(sanitized_path).startswith(str(project_root)):
            return {
                "status": "error",
                "message": "Access denied: File is outside project directory"
            }
        
        # Check if parent directory exists
        parent_dir = sanitized_path.parent
        if not parent_dir.exists():
            return {
                "status": "error",
                "message": f"Parent directory does not exist: {parent_dir}"
            }
        
        # Write the new content to the file
        with open(sanitized_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return {
            "status": "success",
            "message": f"Successfully updated file: {file_path}"
        }
        
    except PermissionError:
        return {
            "status": "error",
            "message": f"Permission denied: Cannot write to file {file_path}"
        }
    except Exception as e:
        logger.error(f"Error updating file {file_path}: {str(e)}")
        return {
            "status": "error",
            "message": f"Error updating file: {str(e)}"
        }


def create_new_file(file_path: str, content: str, config: Config) -> dict:
    """Create a new file with the specified content.
    
    Args:
        file_path: Path for the new file (relative to project root)
        content: Content for the new file
        config: Configuration object
        
    Returns:
        Dictionary with keys:
        - status: "success" or "error"
        - message: Success or error message
    """
    try:
        # Sanitize the file path to prevent directory traversal
        sanitized_path = Path(file_path).resolve()
        project_root = Path(config.PROJECT_ROOT if hasattr(config, 'PROJECT_ROOT') else os.getcwd())
        
        # Ensure the file is within the project directory
        if not str(sanitized_path).startswith(str(project_root)):
            return {
                "status": "error",
                "message": "Access denied: File is outside project directory"
            }
        
        # Check if file already exists
        if sanitized_path.exists():
            return {
                "status": "error",
                "message": f"File already exists: {file_path}"
            }
        
        # Create parent directories if they don't exist
        parent_dir = sanitized_path.parent
        parent_dir.mkdir(parents=True, exist_ok=True)
        
        # Write the content to the new file
        with open(sanitized_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return {
            "status": "success",
            "message": f"Successfully created file: {file_path}"
        }
        
    except PermissionError:
        return {
            "status": "error",
            "message": f"Permission denied: Cannot create file {file_path}"
        }
    except Exception as e:
        logger.error(f"Error creating file {file_path}: {str(e)}")
        return {
            "status": "error",
            "message": f"Error creating file: {str(e)}"
        }