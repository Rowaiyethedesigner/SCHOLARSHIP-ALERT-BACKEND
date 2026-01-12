from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas, crud
from app.database import engine, SessionLocal

app = FastAPI(title="Scholarship Alert API")

models.Base.metadata.create_all(bind=engine)

# =========================
# DB
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
    return {"status": "OK"}


# =========================
# PUBLIC
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
# AUTOMATION INGESTION
# =========================
@app.post("/ingest/calls", response_model=schemas.CallResponse)
def ingest_call(call: schemas.CallIngest, db: Session = Depends(get_db)):
    return crud.ingest_call(db, call)


# =========================
# ADMIN
# =========================
@app.post("/calls", response_model=schemas.CallResponse, dependencies=[Depends(verify_admin)])
def create_call(call: schemas.CallCreate, db: Session = Depends(get_db)):
    return crud.create_call(db, call)

@app.patch("/calls/{call_id}/verify", response_model=schemas.CallResponse, dependencies=[Depends(verify_admin)])
def verify(call_id: int, db: Session = Depends(get_db)):
    result = crud.verify_call(db, call_id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result
