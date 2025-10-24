"""Tests for planner service."""
import pytest
from app.services.planner import planner_service
from app.models.domain import AgentType


@pytest.mark.asyncio
async def test_parse_query_returns_three_subtasks():
    """Test that planner returns exactly 3 subtasks."""
    query = "Plan my Stanford CS midterms week"
    user_id = "test_user_1"
    
    subtasks, rationale = await planner_service.parse_query(query, user_id)
    
    assert len(subtasks) == 3
    assert rationale is not None
    assert len(rationale) > 0


@pytest.mark.asyncio
async def test_parse_query_assigns_correct_agents():
    """Test that subtasks are assigned to valid agents."""
    query = "Organize my study schedule"
    user_id = "test_user_2"
    
    subtasks, _ = await planner_service.parse_query(query, user_id)
    
    # Check all agents are valid
    agent_types = [s.agent for s in subtasks]
    assert AgentType.STUDY_AGENT in agent_types
    assert AgentType.MEAL_AGENT in agent_types
    assert AgentType.CALENDAR_AGENT in agent_types


@pytest.mark.asyncio
async def test_parse_query_provides_descriptions():
    """Test that all subtasks have descriptions."""
    query = "Help me prepare for exams"
    user_id = "test_user_3"
    
    subtasks, _ = await planner_service.parse_query(query, user_id)
    
    for subtask in subtasks:
        assert subtask.description is not None
        assert len(subtask.description) > 10
        assert subtask.id is not None

