from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Event (SQLModel , table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    card_id: str
    reader_id: str
    timestamp: datetime
    type: str  # e.g., "checkin" or "checkout"