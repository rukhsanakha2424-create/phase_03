from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from app.domain.agents.models import Agent, AgentStatusEnum
import json


def get_agents(session: Session) -> List[Agent]:
    """Get all agents from the database"""
    statement = select(Agent).order_by(Agent.created_at.desc())
    agents = session.exec(statement).all()
    return agents


def get_agent_by_id(session: Session, agent_id: int) -> Optional[Agent]:
    """Get a specific agent by ID"""
    statement = select(Agent).where(Agent.id == agent_id)
    agent = session.exec(statement).first()
    return agent


def create_agent(
    session: Session,
    name: str,
    version: str = "1.0.0",
    status: AgentStatusEnum = AgentStatusEnum.online,
    capabilities: Optional[List[str]] = None,
    description: Optional[str] = None
) -> Agent:
    """Create a new agent in the database"""
    capabilities_str = json.dumps(capabilities) if capabilities else None
    
    agent = Agent(
        name=name,
        version=version,
        status=status,
        last_activity=datetime.utcnow(),
        capabilities=capabilities_str,
        description=description,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(agent)
    session.commit()
    session.refresh(agent)
    return agent


def update_agent(
    session: Session,
    agent_id: int,
    name: Optional[str] = None,
    version: Optional[str] = None,
    status: Optional[AgentStatusEnum] = None,
    capabilities: Optional[List[str]] = None,
    description: Optional[str] = None
) -> Optional[Agent]:
    """Update an existing agent in the database"""
    agent = get_agent_by_id(session, agent_id)
    if not agent:
        return None
    
    # Update fields if provided
    if name is not None:
        agent.name = name
    if version is not None:
        agent.version = version
    if status is not None:
        agent.status = status
    if capabilities is not None:
        agent.capabilities = json.dumps(capabilities)
    if description is not None:
        agent.description = description
    
    agent.updated_at = datetime.utcnow()
    if status == AgentStatusEnum.online:
        agent.last_activity = datetime.utcnow()
    
    session.add(agent)
    session.commit()
    session.refresh(agent)
    return agent


def delete_agent(session: Session, agent_id: int) -> bool:
    """Delete an agent from the database"""
    agent = get_agent_by_id(session, agent_id)
    if not agent:
        return False
    
    session.delete(agent)
    session.commit()
    return True