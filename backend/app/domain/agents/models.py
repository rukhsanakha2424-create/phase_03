from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel, Field
from typing import List, Optional


class AgentStatusEnum(str, Enum):
    online = "online"
    offline = "offline"
    busy = "busy"


class Agent(SQLModel, table=True):
    __tablename__ = "agents"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=100)
    version: str = Field(max_length=20, default="1.0.0")
    status: AgentStatusEnum = Field(default=AgentStatusEnum.online)
    last_activity: datetime | None = Field(default=None)
    capabilities: str | None = Field(default=None, max_length=1000)  # Store as JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    description: str | None = Field(default=None, max_length=500)