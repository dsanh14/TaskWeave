"""Anthropic Claude client adapter with mock fallback."""
import json
from typing import Optional
import httpx
from app.config import settings
from app.util.logging import log_info, log_warning
from app.util.ids import generate_id
from app.models.domain import AgentType


class AnthropicClient:
    """Client for Anthropic Claude API with mock fallback."""
    
    def __init__(self):
        self.api_key = settings.anthropic_api_key
        self.base_url = "https://api.anthropic.com/v1"
        self.model = "claude-3-5-sonnet-20241022"
        
    async def complete_json(self, prompt: str, system_prompt: str) -> dict:
        """Get a JSON response from Claude.
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            
        Returns:
            dict: Parsed JSON response
        """
        if not self.api_key:
            log_warning("No Anthropic API key found, using mock response")
            return self._mock_response(prompt)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "max_tokens": 1024,
                        "system": system_prompt,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ]
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                content = data["content"][0]["text"]
                
                # Parse JSON from response
                return json.loads(content)
                
        except Exception as e:
            log_warning(f"Anthropic API call failed: {e}, using mock")
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt: str) -> dict:
        """Generate a mock response for demo purposes."""
        log_info("Generating mock Claude response")
        
        # Parse query to make reasonable subtasks
        query_lower = prompt.lower()
        
        if "midterm" in query_lower or "exam" in query_lower or "study" in query_lower:
            rationale = "Breaking down exam preparation into study sessions, meal planning for energy, and calendar blocking for focus time."
            study_desc = "Create 3 focused study blocks per day (90min each) covering CS fundamentals, algorithms, and practice problems"
            meal_desc = "Schedule healthy meals and snacks to maintain energy during study sessions"
            calendar_desc = "Block study time in calendar, ensuring breaks and avoiding conflicts with existing commitments"
        elif "project" in query_lower or "code" in query_lower:
            rationale = "Organizing project work into coding sessions, nutrition planning, and time blocking."
            study_desc = "Allocate dedicated coding blocks for project implementation and testing"
            meal_desc = "Plan meals around deep work sessions to optimize productivity"
            calendar_desc = "Reserve uninterrupted time slots for coding and review"
        else:
            rationale = "Structuring the task into actionable work blocks, nutrition planning, and calendar management."
            study_desc = "Break task into focused work sessions with clear objectives"
            meal_desc = "Ensure proper nutrition and breaks during work periods"
            calendar_desc = "Schedule time blocks and protect focus time from interruptions"
        
        return {
            "rationale": rationale,
            "subtasks": [
                {
                    "id": generate_id(),
                    "agent": AgentType.STUDY_AGENT.value,
                    "description": study_desc
                },
                {
                    "id": generate_id(),
                    "agent": AgentType.MEAL_AGENT.value,
                    "description": meal_desc
                },
                {
                    "id": generate_id(),
                    "agent": AgentType.CALENDAR_AGENT.value,
                    "description": calendar_desc
                }
            ]
        }


# Global client instance
anthropic_client = AnthropicClient()

