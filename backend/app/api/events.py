from fastapi import APIRouter, Depends, Header, HTTPException
from sqlmodel import Session
from ..db import get_session
from ..models import Event
from ..crud import create_event

router = APIRouter()

@router.post("/api/events", status_code=201)
def post_event(
    event: Event,
    x_edge_secret: str = Header(...),
    session: Session = Depends(get_session)
):
    if x_edge_secret != "supersecret": 
        raise HTTPException(status_code=401, detail="Failed edge secret validation")
        cv = create_event(session, event=event)
        return {"status": "ok", "id": ev.id}

@router.get("/api/events")
def get_events(session: Session = Depends(get_session)):
    events = session.exec(select(Event).order_by(Event.timestamp.desc())).all()
    return events