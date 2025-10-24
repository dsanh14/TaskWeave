"""WebSocket event models."""
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


class EventType(str, Enum):
    """WebSocket event types."""
    AGENT_LOG = "AGENT_LOG"
    TIMELINE_UPDATE = "TIMELINE_UPDATE"
    ERROR = "ERROR"
    PLAN_COMPLETE = "PLAN_COMPLETE"
    AGENTS_SPAWNED = "AGENTS_SPAWNED"
    AGENTS_COMPLETE = "AGENTS_COMPLETE"


class ServerEvent(BaseModel):
    """Server-to-client WebSocket event."""
    type: EventType = Field(description="Event type")
    payload: Any = Field(description="Event payload")
    trace_id: Optional[str] = Field(default=None, description="Request trace ID")


class AgentLogPayload(BaseModel):
    """Payload for AGENT_LOG events."""
    agent: str = Field(description="Agent name")
    message: str = Field(description="Log message")
    level: str = Field(default="INFO", description="Log level")


class TimelineUpdatePayload(BaseModel):
    """Payload for TIMELINE_UPDATE events."""
    user_id: str = Field(description="User ID")
    blocks: list[Any] = Field(description="Updated event blocks")


class ErrorPayload(BaseModel):
    """Payload for ERROR events."""
    message: str = Field(description="Error message")
    details: Optional[str] = Field(default=None, description="Additional error details")

