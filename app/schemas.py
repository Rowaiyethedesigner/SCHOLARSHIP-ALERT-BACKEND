from pydantic import BaseModel
from datetime import date

class CallCreate(BaseModel):
    title: str
    host_country: str
    field: str
    theme: str
    degree_level: str
    funding_type: str
    deadline: date
    source_url: str
    sdg_tags: str


class CallResponse(CallCreate):
    id: int
    verified: bool
    active: bool

    class Config:
        orm_mode = True


class SubscriberCreate(BaseModel):
    email: str
    country_interest: str
    field_interest: str
    degree_interest: str
