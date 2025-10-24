"""Memory management endpoints."""
from fastapi import APIRouter, Query
from app.models.dto import (
    MemoryUpsertRequest,
    MemoryUpsertResponse,
    MemoryGetResponse
)
from app.adapters.letta_client import letta_client
from app.util.ids import generate_trace_id
from app.util.logging import log_info

router = APIRouter()


@router.get("/api/memory", response_model=MemoryGetResponse)
async def get_memory(user_id: str = Query(..., description="User ID")):
    """Fetch user memory and preferences.
    
    Args:
        user_id: User ID
        
    Returns:
        MemoryGetResponse with preferences
    """
    trace_id = generate_trace_id()
    log_info(f"Getting memory for user {user_id}", trace_id=trace_id)
    
    prefs = await letta_client.get_prefs(user_id)
    
    return MemoryGetResponse(prefs=prefs, trace_id=trace_id)


@router.post("/api/memory/upsert", response_model=MemoryUpsertResponse)
async def upsert_memory(request: MemoryUpsertRequest):
    """Save or update user preferences.
    
    Args:
        request: MemoryUpsertRequest with preferences
        
    Returns:
        MemoryUpsertResponse with saved preferences
    """
    trace_id = generate_trace_id()
    log_info(f"Upserting memory for user {request.prefs.user_id}", trace_id=trace_id)
    
    saved_prefs = await letta_client.upsert_prefs(request.prefs)
    
    return MemoryUpsertResponse(prefs=saved_prefs, trace_id=trace_id)

