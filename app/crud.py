from sqlalchemy.orm import Session
from app import models, schemas

def create_call(db: Session, call: schemas.CallCreate):
    db_call = models.ScholarshipCall(**call.dict())
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call


def get_calls(db: Session):
    return db.query(models.ScholarshipCall).filter(
        models.ScholarshipCall.active == True
    ).all()


def create_subscriber(db: Session, sub: schemas.SubscriberCreate):
    db_sub = models.Subscriber(**sub.dict())
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub
