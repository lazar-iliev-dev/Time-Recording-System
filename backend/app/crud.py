from typing import List
from sqlmodel import select, Session
from .models import Event

def create_event(session: Session, *, event: Event) -> Event:
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

def list_events(session: Session) -> List[Event]:
    statement = select(Event).order_by(Event.timestamp.desc())
    results = session.exec(statement)
    return results.all()
