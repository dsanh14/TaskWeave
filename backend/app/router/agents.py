"""Agent coordination endpoints."""
from fastapi import APIRouter
from app.models.dto import (
    AgentSpawnRequest,
    AgentSpawnResponse,
    AgentRunRequest,
    AgentRunResponse
)
from app.services.orchestrator import orchestrator_service
from app.services.event_bus import event_bus
from app.models.events import ServerEvent, EventType, TimelineUpdatePayload
from app.util.ids import generate_trace_id
from app.util.logging import log_info

router = APIRouter()


@router.post("/api/agents/spawn", response_model=AgentSpawnResponse)
async def spawn_agents(request: AgentSpawnRequest):
    """Create agent tasks in Fetch AI.
    
    Args:
        request: AgentSpawnRequest with subtasks
        
    Returns:
        AgentSpawnResponse with agent IDs
    """
    trace_id = request.trace_id or generate_trace_id()
    log_info(f"Spawning {len(request.subtasks)} agents", trace_id=trace_id)
    
    # In MVP, we don't actually spawn separate agents
    # Just return mock agent IDs
    agent_ids = [f"agent_{subtask.agent.value}_{subtask.id[:8]}" 
                 for subtask in request.subtasks]
    
    # Emit event
    await event_bus.publish(ServerEvent(
        type=EventType.AGENTS_SPAWNED,
        payload={"agent_ids": agent_ids},
        trace_id=trace_id
    ))
    
    return AgentSpawnResponse(agent_ids=agent_ids, trace_id=trace_id)


@router.post("/api/agents/run", response_model=AgentRunResponse)
async def run_agents(request: AgentRunRequest):
    """Coordinate agents to produce a merged timeline.
    
    Args:
        request: AgentRunRequest with subtasks
        
    Returns:
        AgentRunResponse with merged timeline
    """
    trace_id = request.trace_id or generate_trace_id()
    log_info(f"Running {len(request.subtasks)} agents", trace_id=trace_id)
    
    # Execute subtasks and get merged timeline
    timeline = await orchestrator_service.execute_subtasks(
        request.user_id,
        request.subtasks,
        trace_id
    )
    
    # Emit timeline update event
    await event_bus.publish(ServerEvent(
        type=EventType.TIMELINE_UPDATE,
        payload=TimelineUpdatePayload(
            user_id=request.user_id,
            blocks=[block.model_dump() for block in timeline]
        ).model_dump(),
        trace_id=trace_id
    ))
    
    # Emit agents complete event
    await event_bus.publish(ServerEvent(
        type=EventType.AGENTS_COMPLETE,
        payload={"block_count": len(timeline)},
        trace_id=trace_id
    ))
    
    return AgentRunResponse(timeline=timeline, trace_id=trace_id)

