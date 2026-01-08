from sqlalchemy.orm import Session
from typing import Optional

from app import models, schemas
from app.email_utils import send_email_alert


# ----------------------------------
# SCHOLARSHIP CALLS
# ----------------------------------

def create_call(db: Session, call: schemas.CallCreate):
    """
    Create a new scholarship call (unverified by default)
    """
    db_call = models.ScholarshipCall(
        title=call.title,
        host_country=call.host_country,
        field=call.field,
        theme=call.theme,
        degree_level=call.degree_level,
        funding_type=call.funding_type,
        deadline=call.deadline,
        source_url=call.source_url,
        sdg_tags=call.sdg_tags,
        verified=False,
        active=True,
    )
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call


def get_calls(
    db: Session,
    host_country: Optional[str] = None,
    degree_level: Optional[str] = None,
    field: Optional[str] = None,
    theme: Optional[str] = None,
    sdg: Optional[str] = None,
):
    """
    Fetch scholarship calls with optional filters
    """
    query = db.query(models.ScholarshipCall).filter(
        models.ScholarshipCall.active == True
    )

    if host_country:
        query = query.filter(
            models.ScholarshipCall.host_country == host_country
        )

    if degree_level:
        query = query.filter(
            models.ScholarshipCall.degree_level == degree_level
        )

    if field:
        query = query.filter(
            models.ScholarshipCall.field == field
        )

    if theme:
        query = query.filter(
            models.ScholarshipCall.theme == theme
        )

    if sdg:
        # sdg_tags stored like: "SDG2,SDG9,SDG13"
        query = query.filter(
            models.ScholarshipCall.sdg_tags.contains(sdg)
        )

    return query.all()


def verify_call(db: Session, call_id: int):
    """
    Mark a scholarship call as verified
    """
    call = db.query(models.ScholarshipCall).filter(
        models.ScholarshipCall.id == call_id
    ).first()

    if not call:
        return None

    call.verified = True
    db.commit()
    db.refresh(call)

    # Notify subscribers AFTER verification
    notify_subscribers(db, call)

    return call


def deactivate_call(db: Session, call_id: int):
    """
    Deactivate (close) a scholarship call
    """
    call = db.query(models.ScholarshipCall).filter(
        models.ScholarshipCall.id == call_id
    ).first()

    if not call:
        return None

    call.active = False
    db.commit()
    db.refresh(call)
    return call


# ----------------------------------
# SUBSCRIBERS
# ----------------------------------

def create_subscriber(db: Session, sub: schemas.SubscriberCreate):
    """
    Add a new email subscriber
    """
    existing = db.query(models.Subscriber).filter(
        models.Subscriber.email == sub.email
    ).first()

    if existing:
        return existing

    db_sub = models.Subscriber(
        email=sub.email,
        country_interest=sub.country_interest,
        field_interest=sub.field_interest,
        degree_interest=sub.degree_interest,
        active=True,
    )
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub


def get_active_subscribers(db: Session):
    """
    Get all active subscribers
    """
    return db.query(models.Subscriber).filter(
        models.Subscriber.active == True
    ).all()


# -------
