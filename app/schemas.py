from pydantic import BaseModel
from datetime import date
from typing import Optional


# =========================
# BASE SCHEMA
# =========================

class CallBase(BaseModel):
    title: str
    host_country: Optional[str] = None
    field: Optional[str] = None
    theme: Optional[str] = None
    degree_level: Optional[str] = None
    funding_type: Optional[str] = None
    deadline: Optional[date] = None
    source_url: Optional[str] = None
    sdg_tags: Optional[str] = None
    source_name: Optional[str] = None
    confidence_score: Optional[str] = None


# =========================
# CREATE (ADMIN)
# =========================

class CallCreate(CallBase):
    pass


# =========================
# INGEST (AUTOMATION)
# =========================

class CallIngest(CallBase):
    pass


# =========================
# RESPONSE MODEL
# =========================

class Call(CallBase):
    id: int
    verified: bool
    active: bool

    class Config:
        from_attributes = True   # Pydantic v2 compatible
