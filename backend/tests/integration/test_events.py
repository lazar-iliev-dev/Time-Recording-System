import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app  # main.py is at backend/main.py

@pytest.mark.asyncio
async def test_create_event_requires_secret():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "card_id": "12345",
            "reader_id": "reader1",
            "timestamp": "2025-10-01T12:00:00Z",
            "type": "checkin",
        }
        r = await ac.post("/api/events", json=payload)
        assert r.status_code == 401

@pytest.mark.asyncio
async def test_create_and_list_event():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "card_id": "12345",
            "reader_id": "reader1",
            "timestamp": "2025-10-01T12:00:00Z",
            "type": "checkin",
        }
        # with correct header
        r = await ac.post("/api/events", json=payload, headers={"x-edge-secret": "supersecret"})
        assert r.status_code == 201

        # list events
        r = await ac.get("/api/events")
        assert r.status_code == 200
        items = r.json()
        assert any(i["card_id"] == "12345" for i in items)
