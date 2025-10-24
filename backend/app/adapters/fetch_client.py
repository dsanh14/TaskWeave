"""Fetch AI client adapter with mock fallback."""
from datetime import datetime, timedelta
import httpx
from app.config import settings
from app.util.logging import log_info, log_warning
from app.util.ids import generate_id
from app.models.domain import Subtask, EventBlock, MemoryPrefs, AgentType


class FetchClient:
    """Client for Fetch AI Agentverse/ASI:One with mock fallback."""
    
    def __init__(self):
        self.api_key = settings.fetch_api_key
        self.agentverse_url = settings.fetch_agentverse_url
        self.asi_one_url = settings.fetch_asi_one_url
        
    async def propose_plan(
        self,
        subtask: Subtask,
        memory: MemoryPrefs
    ) -> list[EventBlock]:
        """Have an agent propose event blocks for a subtask.
        
        Args:
            subtask: The subtask to plan
            memory: User memory and preferences
            
        Returns:
            list[EventBlock]: Proposed event blocks
        """
        if not self.api_key:
            log_warning(f"No Fetch API key, using mock for {subtask.agent}")
            return self._mock_propose(subtask, memory)
        
        try:
            # In a real implementation, this would call Fetch AI API
            # For now, we'll use mock even with API key since we're building MVP
            log_warning(f"Fetch AI integration pending, using mock for {subtask.agent}")
            return self._mock_propose(subtask, memory)
            
        except Exception as e:
            log_warning(f"Fetch API call failed: {e}, using mock")
            return self._mock_propose(subtask, memory)
    
    def _mock_propose(self, subtask: Subtask, memory: MemoryPrefs) -> list[EventBlock]:
        """Generate mock event blocks based on agent type."""
        log_info(f"Mock agent {subtask.agent} proposing blocks")
        
        # Start planning from tomorrow at 8 AM
        tomorrow = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1)
        blocks = []
        
        if subtask.agent == AgentType.STUDY_AGENT:
            # Create 3 study blocks across 3 days
            for day in range(3):
                for session in range(3):
                    start = tomorrow + timedelta(days=day, hours=session * 2)
                    end = start + timedelta(minutes=memory.study_block_minutes)
                    
                    blocks.append(EventBlock(
                        id=generate_id("evt_"),
                        title=f"Study Session {session + 1} - Day {day + 1}",
                        start_iso=start.isoformat(),
                        end_iso=end.isoformat(),
                        source_agent=subtask.agent.value
                    ))
        
        elif subtask.agent == AgentType.MEAL_AGENT:
            # Create meal blocks for 3 days
            meal_times = [
                (12, 0, "Lunch"),
                (18, 0, "Dinner")
            ]
            
            for day in range(3):
                for hour, minute, meal_name in meal_times:
                    start = tomorrow.replace(hour=hour, minute=minute) + timedelta(days=day)
                    end = start + timedelta(minutes=45)
                    
                    dietary_note = f" ({memory.dietary})" if memory.dietary else ""
                    blocks.append(EventBlock(
                        id=generate_id("evt_"),
                        title=f"{meal_name}{dietary_note}",
                        start_iso=start.isoformat(),
                        end_iso=end.isoformat(),
                        source_agent=subtask.agent.value
                    ))
        
        elif subtask.agent == AgentType.CALENDAR_AGENT:
            # Create break blocks
            for day in range(3):
                for break_num in range(3):
                    start = tomorrow + timedelta(days=day, hours=break_num * 2 + 1, minutes=30)
                    end = start + timedelta(minutes=memory.break_minutes)
                    
                    blocks.append(EventBlock(
                        id=generate_id("evt_"),
                        title=f"Break",
                        start_iso=start.isoformat(),
                        end_iso=end.isoformat(),
                        source_agent=subtask.agent.value
                    ))
        
        return blocks


# Global client instance
fetch_client = FetchClient()

