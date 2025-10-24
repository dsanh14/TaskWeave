"""Data Transfer Objects for API requests and responses."""
from typing import Optional
from pydantic import BaseModel, Field
from app.models.domain import Subtask, EventBlock, MemoryPrefs


class PlanRequest(BaseModel):
    """Request to plan a task."""
    user_id: str = Field(description="User ID")
    query: str = Field(description="Natural language query")
    dry_run: bool = Field(default=True, description="Dry-run mode")


class PlanResponse(BaseModel):
    """Response from planning."""
    subtasks: list[Subtask] = Field(description="Subtasks to execute")
    rationale: str = Field(description="Reasoning behind the plan")
    trace_id: str = Field(description="Request trace ID")


class AgentSpawnRequest(BaseModel):
    """Request to spawn agents."""
    user_id: str = Field(description="User ID")
    subtasks: list[Subtask] = Field(description="Subtasks for agents")
    trace_id: str = Field(description="Request trace ID")


class AgentSpawnResponse(BaseModel):
    """Response from spawning agents."""
    agent_ids: list[str] = Field(description="IDs of spawned agents")
    trace_id: str = Field(description="Request trace ID")


class AgentRunRequest(BaseModel):
    """Request to run agents."""
    user_id: str = Field(description="User ID")
    subtasks: list[Subtask] = Field(description="Subtasks to execute")
    trace_id: str = Field(description="Request trace ID")


class AgentRunResponse(BaseModel):
    """Response from running agents."""
    timeline: list[EventBlock] = Field(description="Merged timeline")
    trace_id: str = Field(description="Request trace ID")


class MemoryUpsertRequest(BaseModel):
    """Request to update memory."""
    prefs: MemoryPrefs = Field(description="User preferences")


class MemoryUpsertResponse(BaseModel):
    """Response from memory upsert."""
    prefs: MemoryPrefs = Field(description="Saved preferences")
    trace_id: str = Field(description="Request trace ID")


class MemoryGetResponse(BaseModel):
    """Response from memory get."""
    prefs: MemoryPrefs = Field(description="Current preferences")
    trace_id: str = Field(description="Request trace ID")


class ApplyCalendarRequest(BaseModel):
    """Request to apply blocks to calendar."""
    user_id: str = Field(description="User ID")
    blocks: list[EventBlock] = Field(description="Blocks to apply")
    dry_run: bool = Field(default=True, description="Dry-run mode")


class ApplyCalendarResponse(BaseModel):
    """Response from calendar apply."""
    applied_count: int = Field(description="Number of blocks applied")
    dry_run: bool = Field(description="Whether this was a dry-run")
    trace_id: str = Field(description="Request trace ID")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(description="Service status")
    version: str = Field(default="0.1.0", description="API version")

