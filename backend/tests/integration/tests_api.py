import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_post_and_get_events():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # create payload
        event_data = {
            "card_id": "INT-123",
            "reader_id": "reader1",
            "timestamp": "2025-10-17T09:00:00Z",
            "type": "checkin"
        }

        # expect 401 without secret header
        r = await ac.post("/api/events", json=event_data)
        assert r.status_code == 401

        # with edge secret header
        r = await ac.post("/api/events", json=event_data, headers={"x-edge-secret": "supersecret"})
        assert r.status_code == 201

        # list events
        r = await ac.get("/api/events")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        # at least one event
        assert any(item.get("card_id") == "INT-123" for item in data)
