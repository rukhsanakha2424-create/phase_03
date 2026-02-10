"""Configuration management for agent service."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Agent service configuration from environment variables."""

    # OpenRouter Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    MCP_TOOL_ENDPOINT = os.getenv("MCP_TOOL_ENDPOINT", "http://localhost:8000")
    USER_ID = os.getenv("USER_ID", "default-user")

    # Project configuration
    PROJECT_ROOT = os.getenv("PROJECT_ROOT", os.getcwd())

    # Agent configuration
    AGENT_MODEL = os.getenv("AGENT_MODEL")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))
    TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "30"))

    # Validation
    @classmethod
    def validate(cls, skip_validation: bool = False) -> bool:
        """Validate required configuration is present.

        Args:
            skip_validation: If True, skip validation (useful for testing)

        Returns:
            True if valid, raises otherwise
        """
        if skip_validation:
            return True

        required = ["OPENROUTER_API_KEY", "MCP_TOOL_ENDPOINT"]
        missing = [key for key in required if not getattr(cls, key, None)]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        return True


def get_config(skip_validation: bool = False) -> Config:
    """Get configuration instance.

    Args:
        skip_validation: If True, skip validation checks (useful for testing)

    Returns:
        Config class with loaded environment variables
    """
    Config.validate(skip_validation=skip_validation)
    return Config()
