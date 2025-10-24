"""Tests for API routes."""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


@pytest.mark.asyncio
async def test_plan_endpoint():
    """Test planning endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/plan",
            json={
                "user_id": "test_user",
                "query": "Plan my CS midterms",
                "dry_run": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "subtasks" in data
        assert len(data["subtasks"]) == 3
        assert "rationale" in data
        assert "trace_id" in data


@pytest.mark.asyncio
async def test_memory_get_endpoint():
    """Test memory retrieval endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/memory?user_id=test_user")
        
        assert response.status_code == 200
        data = response.json()
        assert "prefs" in data
        assert data["prefs"]["user_id"] == "test_user"


@pytest.mark.asyncio
async def test_memory_upsert_endpoint():
    """Test memory upsert endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/memory/upsert",
            json={
                "prefs": {
                    "user_id": "test_user",
                    "sleep_start": "23:00",
                    "sleep_end": "07:00",
                    "break_minutes": 15,
                    "study_block_minutes": 90,
                    "dietary": "vegetarian"
                }
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "prefs" in data
        assert data["prefs"]["dietary"] == "vegetarian"


@pytest.mark.asyncio
async def test_agents_run_endpoint():
    """Test agents run endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/agents/run",
            json={
                "user_id": "test_user",
                "subtasks": [
                    {
                        "id": "test_id_1",
                        "agent": "study_agent",
                        "description": "Create study blocks"
                    }
                ],
                "trace_id": "test_trace"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "timeline" in data
        assert isinstance(data["timeline"], list)


@pytest.mark.asyncio
async def test_calendar_apply_endpoint():
    """Test calendar apply endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/tools/calendar/apply",
            json={
                "user_id": "test_user",
                "blocks": [],
                "dry_run": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "applied_count" in data
        assert data["dry_run"] is True

