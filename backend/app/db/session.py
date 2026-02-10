import os
from collections.abc import Generator
from sqlmodel import Session, SQLModel
from app.db.database import sync_engine
from app.domain.agents.service import get_agents, create_agent
from app.domain.agents.models import AgentStatusEnum


def init_db() -> None:
    """Initialize the database and create tables"""
    SQLModel.metadata.create_all(sync_engine)
    
    # Create a default agent if none exists
    with Session(sync_engine) as session:
        agents = get_agents(session)
        if not agents:
            # Create a default agent
            create_agent(
                session=session,
                name="Default Taskie AI Agent",
                version="1.0.0",
                status=AgentStatusEnum.online,
                capabilities=["Task management", "File reading", "Code updates", "System monitoring"],
                description="Default AI agent for task automation and management"
            )


def get_session() -> Generator[Session, None, None]:
    """Get a database session"""
    with Session(sync_engine) as session:
        yield session