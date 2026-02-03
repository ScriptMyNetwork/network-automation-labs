from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
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
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)


class DecisionLink(Base):
    __tablename__ = "decision_links"

    id = Column(Integer, primary_key=True)
    source_decision_id = Column(String, ForeignKey("decisions.decision_id"))
    target_decision_id = Column(String, ForeignKey("decisions.decision_id"))
    relationship_type = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)