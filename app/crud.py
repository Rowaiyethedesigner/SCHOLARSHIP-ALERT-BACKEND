from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas


# =========================
# CREATE SCHOLARSHIP CALL
# =========================
def create_call(db: Session, call: schemas.CallCreate):
    db_call = models.Call(
        title=call.title,
        host_country=call.host_country,
        field=call.field,
        theme=call.theme,
        degree_level=call.degree_level,
        funding_type=call.funding_type,
        deadline=call.deadline,
        source_url=call.source_url,
        sdg_tags=call.sdg_tags,
        verified=call.verified if call.verified is not None else False,
        active=True,
    )
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call


# =========================
# GET SCHOLARSHIPS (SEARCH + FILTER)
# =========================
def get_calls(
    db: Session,
    q: str | None = None,
    host_country: str | None = None,
    degree_level: str | None = None,
    field: str | None = None,
    theme: str | None = None,
    sdg: str | None = None,
):
    query = db.query(models.Call)

    # 🔍 KEYWORD SEARCH
    if q:
        search = f"%{q}%"
        query = query.filter(
            or_(
                models.Call.title.ilike(search),
                models.Call.field.ilike(search),
                models.Call.theme.ilike(search),
                models.Call.sdg_tags.ilike(search),
                models.Call.host_country.ilike(search),
            )
        )

    # 🎯 FILTERS
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

    # ✅ PUBLIC VISIBILITY RULES
    query = query.filter(
        models.Call.active == True,
        models.Call.verified == True
    )

    return query.order_by(models.Call.deadline.asc()).all()


# =========================
# GET SINGLE SCHOLARSHIP
# =========================
def get_call_by_id(db: Session, call_id: int):
    return (
        db.query(models.Call)
        .filter(
            models.Call.id == call_id,
            models.Call.active == True
        )
        .first()
    )


# =========================
# VERIFY SCHOLARSHIP (ADMIN)
# =========================
def verify_call(db: Session, call_id: int):
    call = db.query(models.Call).filter(models.Call.id == call_id).first()
    if not call:
        return None

    call.verified = True
    db.commit()
    db.refresh(call)
    return call


# =========================
# DEACTIVATE SCHOLARSHIP
# =========================
def deactivate_call(db: Session, call_id: int):
    call = db.query(models.Call).filter(models.Call.id == call_id).first()
    if not call:
        return None

    call.active = False
    db.commit()
    db.refresh(call)
    return call
