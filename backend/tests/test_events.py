import pytest
from httpx import AsyncClient
from main import app  # main.py is at backend/main.py

@pytest.mark.asyncio
async def test_create_and_list_event():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Test creating an event payload
        event_data = {
            "card_id": "CARD-1",
            "reader_id": "reader1",
            "timestamp": "2025-10-01T12:00:00Z",
            "type": "checkin"
        }

        # expect 401 without secret
        r = await ac.post("/api/events", json=event_data)
        assert r.status_code == 401

        # with correct header
        r = await ac.post("/api/events", json=event_data, headers={"x-edge-secret": "supersecret"})
        assert r.status_code == 201

        # list events
        r = await ac.get("/api/events")
        assert r.status_code == 200
        items = r.json()
        assert len(items) == 1
        assert items[0]["card_id"] == "CARD-1"
