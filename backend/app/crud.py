from sqlmodel import Select, Session
from .models import Event

def create_event(db: Session, event: Event) -> Event:
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

def list_sessions(session: Session) -> list[Event]:
    statement = Select(Event).order_by(Event.timestamp.desc())
    results = session.exec(statement)
    return results.all()
