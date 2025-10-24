"""LLM planning endpoints."""
from fastapi import APIRouter
from app.models.dto import PlanRequest, PlanResponse
from app.services.planner import planner_service
from app.services.event_bus import event_bus
from app.models.events import ServerEvent, EventType
from app.util.ids import generate_trace_id
from app.util.logging import log_info

router = APIRouter()


@router.post("/api/plan", response_model=PlanResponse)
async def plan_task(request: PlanRequest):
    """Parse user query into subtasks using Claude.
    
    Args:
        request: PlanRequest with user_id, query, dry_run
        
    Returns:
        PlanResponse with subtasks and rationale
    """
    trace_id = generate_trace_id()
    log_info(f"Plan request from user {request.user_id}", trace_id=trace_id)
    
    # Parse query with planner
    subtasks, rationale = await planner_service.parse_query(
        request.query,
        request.user_id
    )
    
    # Emit plan complete event
    await event_bus.publish(ServerEvent(
        type=EventType.PLAN_COMPLETE,
        payload={
            "subtasks": [s.model_dump() for s in subtasks],
            "rationale": rationale
        },
        trace_id=trace_id
    ))
    
    return PlanResponse(
        subtasks=subtasks,
        rationale=rationale,
        trace_id=trace_id
    )

