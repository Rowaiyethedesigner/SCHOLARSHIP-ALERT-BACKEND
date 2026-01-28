from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas
from app.ai_ranker import relevance_score


def create_call(db: Session, call: schemas.CallCreate):
    db_call = models.Call(**call.dict(), active=True)
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call


def ingest_call(db: Session, call: schemas.CallIngest):
    existing = db.query(models.Call).filter(
        models.Call.title == call.title,
        models.Call.source_url == str(call.source_url),
    ).first()

    if existing:
        return existing

    db_call = models.Call(
        **call.dict(exclude={"source_name", "confidence_score"}),
        verified=False,
        active=False,
    )

    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call


def get_calls(
    db: Session,
    q=None,
    host_country=None,
    degree_level=None,
    field=None,
    theme=None,
    sdg=None,
    limit=20,
    offset=0,
):
    query = db.query(models.Call)

    # BASE FILTERS
    query = query.filter(
        models.Call.active == True,
        models.Call.verified == True
    )

    # BASIC DB FILTERS
    if host_country:
        query = query.filter(models.Call.host_country == host_country)

    if degree_level:
        query = query.filter(models.Call.degree_level == degree_level)

    if field:
        query = query.filter(models.Call.field.ilike(f"%{field}%"))

    if theme:
        query = query.filter(models.Call.theme.ilike(f"%{theme}%"))

    if sdg:
        query = query.filter(models.Call.sdg_tags.ilike(f"%{sdg}%"))

    results = query.all()

    # =========================
    # AI RELEVANCE RANKING
    # =========================
    query_params = {
        "q": q,
        "host_country": host_country,
        "degree_level": degree_level,
    }

    ranked = sorted(
        results,
        key=lambda call: relevance_score(call, query_params),
        reverse=True
    )

    # PAGINATION AFTER RANKING
    return ranked[offset: offset + limit]


def verify_call(db: Session, call_id: int):
    call = db.query(models.Call).filter(models.Call.id == call_id).first()
    if not call:
        return None
    call.verified = True
    call.active = True
    db.commit()
    db.refresh(call)
    return call


def deactivate_call(db: Session, call_id: int):
    call = db.query(models.Call).filter(models.Call.id == call_id).first()
    if not call:
        return None
    call.active = False
    db.commit()
    db.refresh(call)
    return call
