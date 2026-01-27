from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime

from app.database import Base


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(String, unique=True, index=True, nullable=False)

    summary = Column(String, nullable=False)
    rationale = Column(Text)

    risks = Column(Text)
    source = Column(String)

    confidence = Column(Float)

    # NEW FIELD
    status = Column(String, default="active")

    created_at = Column(DateTime, default=datetime.utcnow)
