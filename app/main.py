from fastapi import (
    FastAPI,
    Depends,
    Query,
    HTTPException,
)
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import engine, SessionLocal
from app import models, schemas, crud

# ----------------------------------
# DATABASE INITIALIZATION
# ----------------------------------
models.Base.metadata.create_all(bind=engine)

# ----------------------------------
# APP SETUP
# ----------------------------------
app = FastAPI(
    title="Scholarship Alert API",
    description=(
        "Backend API for USA & Canada scholarships focused on "
        "Sustainable Development and SDG-aligned programs"
    ),
    version="1.0.0",
)

# ----------------------------------
# DATABASE SESSION DEPENDENCY
# ----------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------------
# ADMIN API KEY (SECURITY)
# ----------------------------------
API_KEY_NAME = "x-api-key"
ADMIN_API_KEY = "sk_scholarship_admin_2026_live"

api_key_header = APIKeyHeader(
    name=API_KEY_NAME,
    auto_error=False
)

def verify_admin_key(api_key: str = Depends(api_key_header)):
    if api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ----------------------------------
# ROOT
# ----------------------------------
@app.get("/")
def root():
    return {
        "message": "Scholarship Alert API is running",
        "status": "OK"
    }

# ----------------------------------
# SCHOLARSHIP CALLS
# ----------------------------------
@app.post("/calls", response_model=schemas.CallResponse)
def add_call(
    call: schemas.CallCreate,
    db: Session = Depends(get_db),
):
    """
    Add a new scholarship call (unverified by default)
    """
    return crud.create_call(db, call)


@app.get("/calls", response_model=List[schemas.CallResponse])
def list_calls(
    host_country: Optional[str] = Query(default=None),
    degree_level: Optional[str] = Query(default=None),
    field: Optional[str] = Query(default=None),
    theme: Optional[str] = Query(default=None),
    sdg: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    """
    List scholarship calls with optional filters
    """
    return crud.get_calls(
        db,
        host_country=host_country,
        degree_level=degree_level,
        field=field,
        theme=theme,
        sdg=sdg,
    )

# ----------------------------------
# ADMIN ACTIONS (PROTECTED)
# ----------------------------------
@app.patch("/calls/{call_id}/verify", response_model=schemas.CallResponse)
def verify_call(
    call_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin_key),
):
    """
    Verify a scholarship call (admin only)
    """
    call = crud.verify_call(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call


@app.patch("/calls/{call_id}/deactivate", response_model=schemas.CallResponse)
def deactivate_call(
    call_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin_key),
):
    """
    Deactivate (close) a scholarship call (admin only)
    """
    call = crud.deactivate_call(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call

# ----------------------------------
# SUBSCRIBERS
# ----------------------------------
@app.post("/subscribe")
def subscribe(
    subscriber: schemas.SubscriberCreate,
    db: Session = Depends(get_db),
):
    """
    Subscribe an email address for alerts
    """
    return crud.create_subscriber(db, subscriber)
