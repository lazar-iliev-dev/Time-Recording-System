# edge/edge_sim.py
import os
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from datetime import datetime

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")
EDGE_SECRET = os.environ.get("EDGE_SECRET", "supersecret")

app = FastAPI(title="edge-simulator")

class SimEvent(BaseModel):
    card_id: str
    reader_id: str
    type: str = "checkin"

@app.post("/simulate")
async def simulate(evt: SimEvent):
    payload = {
        "card_id": evt.card_id,
        "reader_id": evt.reader_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": evt.type
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BACKEND_URL}/api/events",
                              json=payload,
                              headers={"x-edge-secret": EDGE_SECRET})
        return {"backend_status": r.status_code, "backend_text": r.text}
