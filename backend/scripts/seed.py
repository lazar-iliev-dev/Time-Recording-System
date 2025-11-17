import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
# /app is the working directory in the container
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.models import Event 

from sqlmodel import SQLModel, Session, create_engine, select

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

def main():
    engine = create_engine(DATABASE_URL, echo=False)
    SQLModel.metadata.create_all(engine)

    demo_events = [
        Event(card_id="CARD-001", reader_id="desk-1", timestamp=datetime.now(timezone.utc) - timedelta(hours=3), type="checkin"),
        Event(card_id="CARD-001", reader_id="desk-1", timestamp=datetime.now(timezone.utc) - timedelta(hours=1), type="checkout"),
        Event(card_id="CARD-002", reader_id="desk-2", timestamp=datetime.now(timezone.utc) - timedelta(hours=2), type="checkin"),
        Event(card_id="CARD-002", reader_id="desk-2", timestamp=datetime.now(timezone.utc) - timedelta(minutes=30), type="checkout"),
    ]

    with Session(engine) as session:
        existing_events = session.exec(select(Event)).all()
        if existing_events:
            print(f"[seed] DB already contains {len(existing_events)} events — skipping.")
            return

        for ev in demo_events:
            session.add(ev)
        session.commit()
        print(f"[seed] Added {len(demo_events)} demo events to {DATABASE_URL}")


if __name__ == "__main__":
    main()
