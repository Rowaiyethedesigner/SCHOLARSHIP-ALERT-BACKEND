from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas, crud
from app.database import engine, SessionLocal

app = FastAPI(
    title="Scholarship Alert API",
    version="1.1.0",
)

models.Base.metadata.create_all(bind=engine)

# =========================
# DATABASE
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# ADMIN AUTH
# =========================
ADMIN_API_KEY = "sk_scholarship_admin_2026_live"

def verify_admin(x_api_key: Optional[str] = Header(None)):
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


# =========================
# HEALTH
# =========================
@app.get("/")
def root():
    return {
        "status": "OK",
        "message": "Scholarship Alert API is running"
    }


# =========================
# PUBLIC: SEARCH + PAGINATION
# =========================
@app.get("/calls", response_model=List[schemas.CallResponse])
def list_calls(
    q: Optional[str] = None,
    host_country: Optional[str] = None,
    degree_level: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    return crud.get_calls(
        db=db,
        q=q,
        host_country=host_country,
        degree_level=degree_level,
        limit=limit,
        offset=offset,
    )


# =========================
# AUTOMATION INGESTION (NEW)
# =========================
@app.post("/ingest/calls", response_model=schemas.CallResponse)
def ingest_call(call: schemas.CallIngest, db: Session = Depends(get_db)):
    """
    Endpoint for automation, scrapers, and AI agents.
    Ingested calls are NOT public until verified by admin.
    """
    return crud.ingest_call(db, call)


# =========================
# ADMIN: MANUAL CREATE
# =========================
@app.post(
    "/calls",
    response_model=schemas.CallResponse,
    dependencies=[Depends(verify_admin)],
)
def create_call(call: schemas.CallCreate, db: Session = Depends(get_db)):
    return crud.create_call(db, call)


# =========================
# ADMIN: VERIFY
# =========================
@app.patch(
    "/calls/{call_id}/verify",
    response_model=schemas.CallResponse,
    dependencies=[Depends(verify_admin)],
)
def verify_call(call_id: int, db: Session = Depends(get_db)):
    call = crud.verify_call(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Not found")
    return call
