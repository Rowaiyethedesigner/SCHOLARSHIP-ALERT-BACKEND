from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app import models, schemas, crud
from app.database import engine, get_db

# =========================
# INIT
# =========================

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Scholarship Alert API")

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # public API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
# PUBLIC ENDPOINTS
# =========================

@app.get("/calls", response_model=list[schemas.Call])
def get_calls(
    q: str | None = None,
    host_country: str | None = None,
    degree_level: str | None = None,
    field: str | None = None,
    theme: str | None = None,
    sdg: str | None = None,
    limit: int = 20,
    offset: int = 0,
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
        limit=limit,
        offset=offset,
    )

# =========================
# ADMIN ENDPOINTS
# =========================

@app.post("/calls", response_model=schemas.Call)
def create_call(call: schemas.CallCreate, db: Session = Depends(get_db)):
    return crud.create_call(db=db, call=call)


@app.patch("/calls/{call_id}/verify", response_model=schemas.Call)
def verify_call(call_id: int, db: Session = Depends(get_db)):
    call = crud.verify_call(db=db, call_id=call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call


@app.patch("/calls/{call_id}/deactivate", response_model=schemas.Call)
def deactivate_call(call_id: int, db: Session = Depends(get_db)):
    call = crud.deactivate_call(db=db, call_id=call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call

# =========================
# AUTOMATION / INGESTION
# =========================

@app.post("/ingest/calls", response_model=schemas.Call)
def ingest_call(call: schemas.CallIngest, db: Session = Depends(get_db)):
    return crud.ingest_call(db=db, call=call)

# =========================
# RESEARCH DATASET API
# =========================

@app.get("/research/dataset")
def research_dataset(db: Session = Depends(get_db)):
    calls = db.query(models.Call).filter(
        models.Call.verified == True,
        models.Call.active == True
    ).all()

    dataset = []

    for c in calls:
        dataset.append({
            "id": c.id,
            "title": c.title,
            "host_country": c.host_country,
            "field": c.field,
            "theme": c.theme,
            "degree_level": c.degree_level,
            "funding_type": c.funding_type,
            "deadline": str(c.deadline) if c.deadline else None,
            "sdg_tags": c.sdg_tags,
            "source_url": c.source_url,
            "source_name": c.source_name,
            "confidence_score": c.confidence_score,
        })

    return {
        "count": len(dataset),
        "dataset": dataset
    }
