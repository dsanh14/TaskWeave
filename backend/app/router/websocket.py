"""WebSocket endpoint for real-time events."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Set
import json
from app.services.event_bus import event_bus
from app.models.events import ServerEvent, EventType
from app.util.logging import log_info

router = APIRouter()

# Active WebSocket connections
active_connections: Set[WebSocket] = set()


@router.websocket("/ws/events")
async def websocket_events(websocket: WebSocket):
    """WebSocket endpoint for streaming server events to clients.
    
    Clients receive JSON messages in ServerEvent format:
    {
        "type": "AGENT_LOG" | "TIMELINE_UPDATE" | "ERROR" | ...,
        "payload": {...},
        "trace_id": "..."
    }
    """
    await websocket.accept()
    active_connections.add(websocket)
    log_info("WebSocket client connected")
    
    # Define event handler for this connection
    async def send_event(event: ServerEvent) -> None:
        """Send event to this WebSocket client."""
        try:
            if websocket in active_connections:
                await websocket.send_text(event.model_dump_json())
        except Exception as e:
            log_info(f"Error sending WebSocket event: {e}")
            if websocket in active_connections:
                active_connections.remove(websocket)
    
    # Subscribe to all event types
    for event_type in EventType:
        event_bus.subscribe(event_type, send_event)
    
    try:
        # Keep connection alive and wait for disconnect
        while True:
            # Receive messages (clients may send pings to keep alive)
            data = await websocket.receive_text()
            # Echo back or ignore
            
    except WebSocketDisconnect:
        log_info("WebSocket client disconnected")
    finally:
        # Cleanup
        if websocket in active_connections:
            active_connections.remove(websocket)
        
        # Unsubscribe from all events
        for event_type in EventType:
            event_bus.unsubscribe(event_type, send_event)


async def broadcast_event(event: ServerEvent) -> None:
    """Broadcast an event to all connected WebSocket clients.
    
    Args:
        event: Event to broadcast
    """
    disconnected = set()
    
    for connection in active_connections:
        try:
            await connection.send_text(event.model_dump_json())
        except Exception:
            disconnected.add(connection)
    
    # Remove disconnected clients
    active_connections.difference_update(disconnected)

