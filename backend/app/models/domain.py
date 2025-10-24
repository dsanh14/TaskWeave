"""Domain models for core business entities."""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class AgentType(str, Enum):
    """Available agent types."""
    STUDY_AGENT = "study_agent"
    MEAL_AGENT = "meal_agent"
    CALENDAR_AGENT = "calendar_agent"


class EventStatus(str, Enum):
    """Status of an event block."""
    PROPOSED = "proposed"
    APPLIED = "applied"


class Subtask(BaseModel):
    """A subtask assigned to an agent."""
    id: str = Field(description="Unique subtask ID")
    agent: AgentType = Field(description="Agent responsible for this subtask")
    description: str = Field(description="What the agent should do")


class EventBlock(BaseModel):
    """A calendar event block."""
    id: str = Field(description="Unique block ID")
    title: str = Field(description="Event title")
    start_iso: str = Field(description="Start time in ISO 8601 format")
    end_iso: str = Field(description="End time in ISO 8601 format")
    source_agent: str = Field(description="Agent that created this block")
    status: EventStatus = Field(default=EventStatus.PROPOSED)


class MemoryPrefs(BaseModel):
    """User memory and preferences."""
    user_id: str = Field(description="Unique user ID")
    sleep_start: str = Field(default="23:00", description="Sleep start time (HH:MM)")
    sleep_end: str = Field(default="07:00", description="Sleep end time (HH:MM)")
    break_minutes: int = Field(default=15, description="Break duration after study blocks")
    study_block_minutes: int = Field(default=90, description="Standard study block length")
    dietary: Optional[str] = Field(default=None, description="Dietary preferences or restrictions")


class Timeline(BaseModel):
    """A collection of event blocks for a user."""
    user_id: str = Field(description="User ID")
    blocks: list[EventBlock] = Field(default_factory=list, description="Event blocks in chronological order")

