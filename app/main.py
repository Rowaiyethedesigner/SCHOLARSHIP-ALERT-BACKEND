from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app import models, schemas, crud

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Scholarship Alert API",
    description="Backend API for USA & Canada scholarships focused on Sustainable Development",
    version="1.0.0"
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# ROOT
# -------------------------
@app.get("/")
def root():
    return {
        "message": "Scholarship Alert API is running",
        "status": "OK"
    }


# -------------------------
# SCHOLARSHIP CALLS
# -------------------------
@app.post("/calls", response_model=schemas.CallResponse)
def add_call(
    call: schemas.CallCreate,
    db: Session = Depends(get_db)
):
    return crud.create_call(db, call)


@app.get("/calls", response_model=list[schemas.CallResponse])
def list_calls(db: Session = Depends(get_db)):
    return crud.get_calls(db)


# -------------------------
# SUBSCRIBERS
# -------------------------
@app.post("/subscribe")
def subscribe(
    subscriber: schemas.SubscriberCreate,
    db: Session = Depends(get_db)
):
    return crud.create_subscriber(db, subscriber)

