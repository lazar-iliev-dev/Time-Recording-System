import pytest
from sqlmodel import sqlmodel, Session, create_engine
from backend.app.models import Event
from backend.app.crud import create_event, list_events

@pytest.fixture
def in_memuri_engine():
    engine = create_engine("sqlite:///:memory:", echo=False, connect_args={"check_same_thread": False})
    sqlmodel.SQLModel.metadata.create_all(engine)
    return engine

def test_create_and_list_event(in_memory_engine):
    with Session(in_memory_engine) as session:
        # create a model instance
        ev = Event(card_id="CARD-UNIT", reader_id="desk-1", timestamp="2025-10-17T09:00:00Z", type="checkin")
        created = create_event(session=session, event=ev)

        # created should have an id (SQLModel sets after flush/refresh)
        assert getattr(created, "id", None) is not None

        items = list_events(session=session)
        assert len(items) == 1
        assert items[0].card_id == "CARD-UNIT"