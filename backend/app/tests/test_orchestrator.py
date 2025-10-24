"""Tests for orchestrator service."""
import pytest
from app.services.orchestrator import orchestrator_service
from app.models.domain import Subtask, AgentType
from app.util.ids import generate_id


@pytest.mark.asyncio
async def test_execute_subtasks_returns_timeline():
    """Test that orchestrator returns a valid timeline."""
    subtasks = [
        Subtask(
            id=generate_id(),
            agent=AgentType.STUDY_AGENT,
            description="Create study blocks"
        ),
        Subtask(
            id=generate_id(),
            agent=AgentType.MEAL_AGENT,
            description="Plan meals"
        ),
        Subtask(
            id=generate_id(),
            agent=AgentType.CALENDAR_AGENT,
            description="Block calendar time"
        )
    ]
    
    timeline = await orchestrator_service.execute_subtasks(
        "test_user",
        subtasks,
        "test_trace"
    )
    
    assert isinstance(timeline, list)
    assert len(timeline) > 0


@pytest.mark.asyncio
async def test_execute_subtasks_produces_no_overlaps():
    """Test that merged timeline has no overlapping blocks."""
    subtasks = [
        Subtask(
            id=generate_id(),
            agent=AgentType.STUDY_AGENT,
            description="Study sessions"
        )
    ]
    
    timeline = await orchestrator_service.execute_subtasks(
        "test_user",
        subtasks,
        "test_trace"
    )
    
    # Check for overlaps
    for i in range(len(timeline) - 1):
        current_end = timeline[i].end_iso
        next_start = timeline[i + 1].start_iso
        assert current_end <= next_start, "Found overlapping blocks"

