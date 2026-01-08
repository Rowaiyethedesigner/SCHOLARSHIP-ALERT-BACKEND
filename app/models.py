from sqlalchemy import Column, Integer, String, Boolean, Date
from app.database import Base

class ScholarshipCall(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    host_country = Column(String)
    field = Column(String)
    theme = Column(String)
    degree_level = Column(String)
    funding_type = Column(String)
    deadline = Column(Date)
    source_url = Column(String)
    sdg_tags = Column(String)
    verified = Column(Boolean, default=False)
    active = Column(Boolean, default=True)


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    country_interest = Column(String)
    field_interest = Column(String)
    degree_interest = Column(String)
    active = Column(Boolean, default=True)
