"""Tool execution endpoints (calendar, etc.)."""
from fastapi import APIRouter
from app.models.dto import ApplyCalendarRequest, ApplyCalendarResponse
from app.adapters.composio_client import composio_client
from app.util.ids import generate_trace_id
from app.util.logging import log_info

router = APIRouter()


@router.post("/api/tools/calendar/apply", response_model=ApplyCalendarResponse)
async def apply_calendar(request: ApplyCalendarRequest):
    """Apply event blocks to Google Calendar via Composio.
    
    Args:
        request: ApplyCalendarRequest with blocks and dry_run flag
        
    Returns:
        ApplyCalendarResponse with applied count
    """
    trace_id = generate_trace_id()
    log_info(
        f"Applying {len(request.blocks)} blocks to calendar "
        f"(dry_run={request.dry_run})",
        trace_id=trace_id
    )
    
    applied_count = await composio_client.apply_calendar(
        request.blocks,
        request.dry_run
    )
    
    return ApplyCalendarResponse(
        applied_count=applied_count,
        dry_run=request.dry_run,
        trace_id=trace_id
    )

