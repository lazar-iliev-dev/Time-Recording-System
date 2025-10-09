from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="time-tracker")

class Event(BaseModel):
    card_id: str
    reader_id: str
    timestamp: datetime
    type: str  # "checkin" | "checkout"

# very small in-memory store for MVP (keeps Event objects)
_events: List[Event] = []

# POST /api/events
@app.post("/api/events", status_code=201)
async def create_event(event: Event, x_edge_secret: str = Header(None)):
    # simple auth for edge (in prod use better auth)
    if x_edge_secret != "supersecret":
        raise HTTPException(status_code=401, detail="Invalid edge secret")
    _events.append(event)
    return {"status": "ok"}

# GET /api/events
@app.get("/api/events", response_model=List[Event])
async def list_events():
    return _events
