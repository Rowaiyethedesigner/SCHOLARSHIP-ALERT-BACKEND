from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas, crud
from app.database import engine, SessionLocal

# =========================
# APP INIT
# =========================
app = FastAPI(
    title="Scholarship Alert API",
    description="API for verified USA & Canada scholarship opportunities",
    version="1.0.0",
)

models.Base.metadata.create_all(bind=engine)

# =========================
# DB DEPENDENCY
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
        raise HTTPException(status_code=401, detail="Unauthorized admin access")

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {
        "status": "OK",
        "message": "Scholarship Alert API is running"
    }

# =========================
# PUBLIC: LIST SCHOLARSHIPS (SEARCH + FILTER)
# =========================
@app.get("/calls", response_model=List[schemas.CallResponse])
def list_calls(
    q: Optional[str] = None,
    host_country: Optional[str] = None,
    degree_level: Optional[str] = None,
    field: Optional[str] = None,
    theme: Optional[str] = None,
    sdg: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_calls(
        db=db,
        q=q,
        host_country=host_country,
        degree_level=degree_level,
        field=field,
        theme=theme,
        sdg=sdg,
    )

# =========================
# PUBLIC: GET SINGLE SCHOLARSHIP
# =========================
@app.get("/calls/{call_id}", response_model=schemas.CallResponse)
def get_call(call_id: int, db: Session = Depends(get_db)):
    call = crud.get_call_by_id(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return call

# =========================
# ADMIN: CREATE SCHOLARSHIP
# =========================
@app.post(
    "/calls",
    response_model=schemas.CallResponse,
    dependencies=[Depends(verify_admin)],
)
def create_call(call: schemas.CallCreate, db: Session = Depends(get_db)):
    return crud.create_call(db, call)

# =========================
# ADMIN: VERIFY SCHOLARSHIP
# =========================
@app.patch(
    "/calls/{call_id}/verify",
    response_model=schemas.CallResponse,
    dependencies=[Depends(verify_admin)],
)
def verify_call(call_id: int, db: Session = Depends(get_db)):
    call = crud.verify_call(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return call

# =========================
# ADMIN: DEACTIVATE SCHOLARSHIP
# =========================
@app.patch(
    "/calls/{call_id}/deactivate",
    response_model=schemas.CallResponse,
    dependencies=[Depends(verify_admin)],
)
def deactivate_call(call_id: int, db: Session = Depends(get_db)):
    call = crud.deactivate_call(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return call
