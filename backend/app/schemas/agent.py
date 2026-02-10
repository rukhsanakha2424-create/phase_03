from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class AgentStatusResponse(BaseModel):
    """Response model for agent status."""
    is_active: bool
    name: str
    capabilities: List[str]
    last_activity: str
    version: Optional[str] = "1.0.0"
    uptime: Optional[str] = None