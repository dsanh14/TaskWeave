"""In-process event bus for pub/sub messaging."""
from typing import Callable, Awaitable
from collections import defaultdict
from app.models.events import ServerEvent, EventType
from app.util.logging import log_info


EventHandler = Callable[[ServerEvent], Awaitable[None]]


class EventBus:
    """Simple in-process event bus for WebSocket integration."""
    
    def __init__(self):
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
        
    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Subscribe a handler to an event type.
        
        Args:
            event_type: Type of event to listen for
            handler: Async function to call when event is published
        """
        self._handlers[event_type.value].append(handler)
        log_info(f"Subscribed handler to {event_type.value}")
        
    def unsubscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Unsubscribe a handler from an event type.
        
        Args:
            event_type: Type of event
            handler: Handler to remove
        """
        if handler in self._handlers[event_type.value]:
            self._handlers[event_type.value].remove(handler)
            log_info(f"Unsubscribed handler from {event_type.value}")
    
    async def publish(self, event: ServerEvent) -> None:
        """Publish an event to all subscribers.
        
        Args:
            event: Event to publish
        """
        handlers = self._handlers.get(event.type.value, [])
        
        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                log_info(f"Error in event handler: {e}")


# Global event bus instance
event_bus = EventBus()

