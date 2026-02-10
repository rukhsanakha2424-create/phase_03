from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime
from sqlmodel import Session
import json

from app.db.session import get_session
from app.domain.agents.service import (
    get_agents as db_get_agents,
    create_agent as db_create_agent,
    update_agent as db_update_agent,
    delete_agent as db_delete_agent
)
from app.domain.agents.models import Agent as AgentModel, AgentStatusEnum

router = APIRouter(prefix="/agents", tags=["agents"])


class Agent(BaseModel):
    id: int
    name: str
    version: str
    status: str
    last_activity: str | None
    capabilities: List[str] | None = []
    created_at: str
    updated_at: str
    description: str | None = None

    class Config:
        from_attributes = True


class AgentStatus(BaseModel):
    is_active: bool
    name: str
    capabilities: List[str]
    last_activity: str
    version: str = "1.0.0"
    uptime: str = None


class CreateAgentRequest(BaseModel):
    name: str
    version: str = "1.0.0"
    status: str = "online"
    capabilities: List[str] | None = []
    description: str | None = None


class UpdateAgentRequest(BaseModel):
    name: str | None = None
    version: str | None = None
    status: str | None = None
    capabilities: List[str] | None = None
    description: str | None = None


def format_datetime(dt):
    """Format datetime for API response"""
    if dt is None:
        return None
    if isinstance(dt, str):
        return dt
    return dt.isoformat()


def parse_capabilities(capabilities_str):
    """Parse capabilities from JSON string to list"""
    if not capabilities_str:
        return []
    try:
        return json.loads(capabilities_str)
    except:
        return []


def map_agent_to_response(agent: AgentModel) -> Agent:
    """Convert Agent model to API response format"""
    return Agent(
        id=agent.id,
        name=agent.name,
        version=agent.version,
        status=agent.status.value,
        last_activity=format_datetime(agent.last_activity),
        capabilities=parse_capabilities(agent.capabilities),
        created_at=format_datetime(agent.created_at),
        updated_at=format_datetime(agent.updated_at),
        description=agent.description
    )


@router.get("", response_model=List[Agent])
async def get_agents(session: Session = Depends(get_session)):
    """Get list of all agents from database"""
    agents = db_get_agents(session)
    return [map_agent_to_response(agent) for agent in agents]


@router.post("", response_model=Agent)
async def create_agent(
    agent: CreateAgentRequest,
    session: Session = Depends(get_session)
):
    """Create a new agent in the database"""
    try:
        # Validate status
        try:
            status = AgentStatusEnum(agent.status)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {agent.status}. Valid values are: online, offline, busy")
        
        new_agent = db_create_agent(
            session=session,
            name=agent.name,
            version=agent.version,
            status=status,
            capabilities=agent.capabilities,
            description=agent.description
        )
        return map_agent_to_response(new_agent)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create agent: {str(e)}")


@router.put("/{agent_id}", response_model=Agent)
async def update_agent(
    agent_id: int,
    agent_update: UpdateAgentRequest,
    session: Session = Depends(get_session)
):
    """Update an existing agent in the database"""
    try:
        # Convert status if provided
        status = None
        if agent_update.status is not None:
            try:
                status = AgentStatusEnum(agent_update.status)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid status: {agent_update.status}. Valid values are: online, offline, busy")
        
        updated_agent = db_update_agent(
            session=session,
            agent_id=agent_id,
            name=agent_update.name,
            version=agent_update.version,
            status=status,
            capabilities=agent_update.capabilities,
            description=agent_update.description
        )
        
        if not updated_agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        return map_agent_to_response(updated_agent)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update agent: {str(e)}")


@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: int,
    session: Session = Depends(get_session)
):
    """Delete an agent from the database"""
    try:
        success = db_delete_agent(session, agent_id)
        if not success:
            raise HTTPException(status_code=404, detail="Agent not found")
        return {"message": "Agent deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete agent: {str(e)}")


@router.get("/status", response_model=AgentStatus)
async def get_agent_status():
    """Get the current status of the main AI agent."""
    # Return a default status response
    return AgentStatus(
        is_active=True,
        name="Taskie AI Agent",
        capabilities=[
            "Task management",
            "File reading",
            "Code updates",
            "System monitoring"
        ],
        last_activity=datetime.now().isoformat(),
        version="1.2.0"
    )