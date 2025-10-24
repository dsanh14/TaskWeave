"""Orchestrator service for coordinating agents."""
from app.adapters.fetch_client import fetch_client
from app.adapters.letta_client import letta_client
from app.models.domain import Subtask, EventBlock
from app.services.timeline import timeline_service
from app.services.event_bus import event_bus
from app.models.events import ServerEvent, EventType, AgentLogPayload
from app.util.logging import log_info
from app.util.errors import OrchestratorError


class OrchestratorService:
    """Service for coordinating multi-agent execution."""
    
    async def execute_subtasks(
        self,
        user_id: str,
        subtasks: list[Subtask],
        trace_id: str
    ) -> list[EventBlock]:
        """Execute subtasks across agents and merge results.
        
        Args:
            user_id: User ID
            subtasks: List of subtasks to execute
            trace_id: Request trace ID
            
        Returns:
            list[EventBlock]: Merged timeline
            
        Raises:
            OrchestratorError: If orchestration fails
        """
        log_info(f"Orchestrating {len(subtasks)} subtasks", trace_id=trace_id)
        
        try:
            # Get user memory
            memory = await letta_client.get_prefs(user_id)
            
            # Collect all proposed blocks from agents
            all_blocks: list[EventBlock] = []
            
            for subtask in subtasks:
                # Log agent start
                await self._emit_agent_log(
                    subtask.agent.value,
                    f"Starting: {subtask.description[:80]}...",
                    trace_id
                )
                
                # Get agent's proposed blocks
                blocks = await fetch_client.propose_plan(subtask, memory)
                
                all_blocks.extend(blocks)
                
                # Log agent completion
                await self._emit_agent_log(
                    subtask.agent.value,
                    f"Proposed {len(blocks)} blocks",
                    trace_id
                )
            
            # Merge timeline with conflict resolution
            merged_timeline = timeline_service.merge_blocks(all_blocks, memory)
            
            log_info(
                f"Orchestration complete: {len(all_blocks)} raw → "
                f"{len(merged_timeline)} merged blocks",
                trace_id=trace_id
            )
            
            return merged_timeline
            
        except Exception as e:
            log_info(f"Orchestration error: {e}", trace_id=trace_id)
            raise OrchestratorError(f"Failed to execute subtasks: {e}", trace_id)
    
    async def _emit_agent_log(
        self,
        agent: str,
        message: str,
        trace_id: str
    ) -> None:
        """Emit an agent log event to the event bus."""
        event = ServerEvent(
            type=EventType.AGENT_LOG,
            payload=AgentLogPayload(
                agent=agent,
                message=message,
                level="INFO"
            ).model_dump(),
            trace_id=trace_id
        )
        await event_bus.publish(event)


# Global orchestrator instance
orchestrator_service = OrchestratorService()

