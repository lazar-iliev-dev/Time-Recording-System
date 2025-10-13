from fastapi import FastAPI
from .db import create_db_and_tables
from .api.events import router as events_router

app = FastAPI(title="time-tracker")
app.include_router(events_router)

# For dev convenience only: create tables at startup (migrations preferred)
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
