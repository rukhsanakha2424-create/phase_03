from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/agent", tags=["agent"])

@router.get("/status")
def get_agent_status():
    """Get the current status of the AI agent."""
    # For now, return a static status to avoid database issues
    return {"status": "online", "active_agents": 1}