"""Tools for interacting with frontend and backend systems."""

import os
import logging
from typing import Dict, Any
from pathlib import Path

from agent_service_impl.config import Config
from agent_service_impl.tools.file_reader import read_file_content, list_directory_contents
from agent_service_impl.tools.file_updater import update_file_content, create_new_file

logger = logging.getLogger(__name__)


def read_frontend_file(file_path: str, config: Config) -> dict:
    """Read a file from the frontend directory.
    
    Args:
        file_path: Path to the file relative to frontend directory
        config: Configuration object
        
    Returns:
        Dictionary with file content or error
    """
    frontend_path = os.path.join(config.PROJECT_ROOT, "frontend", file_path)
    return read_file_content(frontend_path, config)


def read_backend_file(file_path: str, config: Config) -> dict:
    """Read a file from the backend directory.
    
    Args:
        file_path: Path to the file relative to backend directory
        config: Configuration object
        
    Returns:
        Dictionary with file content or error
    """
    backend_path = os.path.join(config.PROJECT_ROOT, "backend", file_path)
    return read_file_content(backend_path, config)


def update_frontend_file(file_path: str, content: str, config: Config) -> dict:
    """Update a file in the frontend directory.
    
    Args:
        file_path: Path to the file relative to frontend directory
        content: New content for the file
        config: Configuration object
        
    Returns:
        Dictionary with success/error message
    """
    frontend_path = os.path.join(config.PROJECT_ROOT, "frontend", file_path)
    return update_file_content(frontend_path, content, config)


def update_backend_file(file_path: str, content: str, config: Config) -> dict:
    """Update a file in the backend directory.
    
    Args:
        file_path: Path to the file relative to backend directory
        content: New content for the file
        config: Configuration object
        
    Returns:
        Dictionary with success/error message
    """
    backend_path = os.path.join(config.PROJECT_ROOT, "backend", file_path)
    return update_file_content(backend_path, content, config)


def list_frontend_directory(dir_path: str, config: Config) -> dict:
    """List contents of a directory in the frontend.
    
    Args:
        dir_path: Path to the directory relative to frontend directory
        config: Configuration object
        
    Returns:
        Dictionary with directory contents or error
    """
    frontend_path = os.path.join(config.PROJECT_ROOT, "frontend", dir_path)
    return list_directory_contents(frontend_path, config)


def list_backend_directory(dir_path: str, config: Config) -> dict:
    """List contents of a directory in the backend.
    
    Args:
        dir_path: Path to the directory relative to backend directory
        config: Configuration object
        
    Returns:
        Dictionary with directory contents or error
    """
    backend_path = os.path.join(config.PROJECT_ROOT, "backend", dir_path)
    return list_directory_contents(backend_path, config)


def restart_services(config: Config) -> dict:
    """Restart frontend and backend services if needed.
    
    Args:
        config: Configuration object
        
    Returns:
        Dictionary with restart status
    """
    try:
        # In a real implementation, this would restart services
        # For now, we'll just return a success message
        return {
            "status": "success",
            "message": "Services would be restarted in a production environment"
        }
    except Exception as e:
        logger.error(f"Error restarting services: {str(e)}")
        return {
            "status": "error",
            "message": f"Error restarting services: {str(e)}"
        }