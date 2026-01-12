from pydantic import BaseModel, HttpUrl
from datetime import date
from typing import Optional


# =========================
# BASE SCHOLARSHIP SCHEMA
# =========================
class CallBase(BaseModel):
    title: str
    host_country: str
    field: str
    theme: str
    degree_level: str
    funding_type: str
    deadline: date
    source_url: HttpUrl
    sdg_tags: str


# =========================
# ADMIN CREATE
# =========================
class CallCreate(CallBase):
    verified: Optional[bool] = False


# =========================
# AUTOMATION INGESTION
# =========================
class CallIngest(CallBase):
    source_name: Optional[str] = "automation"
    confidence_score: Optional[float] = 0.0


# =========================
# RESPONSE MODEL
# =========================
class CallResponse(CallBase):
    id: int
    verified: bool
    active: bool

    class Config:
        orm_mode = True
