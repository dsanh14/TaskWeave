"""Planning service using Claude to parse user intent."""
from app.adapters.anthropic_client import anthropic_client
from app.models.domain import Subtask
from app.util.logging import log_info
from app.util.errors import PlannerError


SYSTEM_PROMPT = """You are a planner that converts a user's task into exactly three subtasks, each mapped to one of: 'study_agent', 'meal_agent', 'calendar_agent'. Return strict JSON only with keys: 'rationale' and 'subtasks'. 'subtasks' must contain exactly three items. Keep descriptions imperative and specific. Respect quiet hours from memory if provided.

STRICT OUTPUT SCHEMA:
{
  "rationale": "...",
  "subtasks": [
    {"id":"<uuid>", "agent":"study_agent", "description":"..."},
    {"id":"<uuid>", "agent":"meal_agent", "description":"..."},
    {"id":"<uuid>", "agent":"calendar_agent", "description":"..."}
  ]
}

Rules:
- No extra keys, no prose outside JSON.
- Assume university student schedule.
- Prefer 3×90m study blocks/day with 15m breaks, adjust to memory sleep window.
- If memory missing, use defaults: sleep 23:00–07:00; study_block_minutes 90; break_minutes 15."""


class PlannerService:
    """Service for parsing user queries into actionable subtasks."""
    
    async def parse_query(self, query: str, user_id: str) -> tuple[list[Subtask], str]:
        """Parse a user query into subtasks.
        
        Args:
            query: Natural language query
            user_id: User ID for context
            
        Returns:
            tuple: (list of Subtask, rationale string)
            
        Raises:
            PlannerError: If parsing fails
        """
        log_info(f"Planning query for user {user_id}: {query[:50]}...")
        
        try:
            # Call Claude (or mock)
            result = await anthropic_client.complete_json(
                prompt=query,
                system_prompt=SYSTEM_PROMPT
            )
            
            # Validate response
            if "subtasks" not in result or "rationale" not in result:
                raise PlannerError("Invalid response structure from planner")
            
            if len(result["subtasks"]) != 3:
                raise PlannerError(f"Expected 3 subtasks, got {len(result['subtasks'])}")
            
            # Convert to Subtask objects
            subtasks = [Subtask(**task) for task in result["subtasks"]]
            rationale = result["rationale"]
            
            log_info(f"Plan created with {len(subtasks)} subtasks")
            return subtasks, rationale
            
        except Exception as e:
            log_info(f"Planning error: {e}")
            raise PlannerError(f"Failed to parse query: {e}")


# Global planner instance
planner_service = PlannerService()

