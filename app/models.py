from sqlalchemy import Column, Integer, String, Boolean, Date
from app.database import Base

class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)

    # Core data
    title = Column(String, nullable=False)
    host_country = Column(String, nullable=True)
    field = Column(String, nullable=True)
    theme = Column(String, nullable=True)
    degree_level = Column(String, nullable=True)
    funding_type = Column(String, nullable=True)
    deadline = Column(Date, nullable=True)
    source_url = Column(String, nullable=True)
    sdg_tags = Column(String, nullable=True)

    # Moderation & lifecycle
    verified = Column(Boolean, default=False)
    active = Column(Boolean, default=True)

    # Metadata
    source_name = Column(String, nullable=True)
    confidence_score = Column(String, nullable=True)
