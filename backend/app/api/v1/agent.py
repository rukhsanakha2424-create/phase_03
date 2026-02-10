from fastapi import APIRouter, Depends
from typing import Dict, Any
from datetime import datetime
from sqlmodel import Session

from app.db.session import get_session
from app.domain.agents.service import get_agents as db_get_agents

router = APIRouter(prefix="/agent", tags=["agent"])

@router.get("/status")
async def get_agent_status(session: Session = Depends(get_session)):
    """Get the current status of the AI agent."""
    # Get all agents to determine overall status
    agents = db_get_agents(session)
    
    # Determine status based on agents
    if agents:
        # If any agent is online, return online
        for agent in agents:
            if agent.status.value == "online":
                return {"status": "online", "active_agents": len([a for a in agents if a.status.value == "online"])}
        # If no agents are online but there are agents, return busy/offline depending on first agent
        return {"status": agents[0].status.value, "active_agents": 0}
    else:
        # No agents exist
        return {"status": "offline", "active_agents": 0}