from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database import SessionLocal
from app.models import Decision

app = FastAPI(title="Organizational Decision Memory API")


# ---------- Pydantic Schema (API input model) ----------
class DecisionCreate(BaseModel):
    decision_id: str
    summary: str
    rationale: Optional[str] = None
    risks: Optional[str] = None
    source: Optional[str] = None
    confidence: float = 0.5
    status: str = "active"


def decision_to_dict(d):
    return {
        "decision_id": d.decision_id,
        "summary": d.summary,
        "rationale": d.rationale,
        "risks": d.risks,
        "source": d.source,
        "confidence": d.confidence,
        "status": d.status,
        "created_at": d.created_at
    }


@app.get("/")
def root():
    return {"message": "Decision Memory Engine Running"}


@app.get("/decisions")
def list_decisions():
    session = SessionLocal()
    decisions = session.query(Decision).all()
    result = [decision_to_dict(d) for d in decisions]
    session.close()
    return result


@app.get("/decisions/{decision_id}")
def get_decision(decision_id: str):
    session = SessionLocal()
    d = session.query(Decision).filter(Decision.decision_id == decision_id).first()
    session.close()

    if not d:
        raise HTTPException(status_code=404, detail="Decision not found")

    return decision_to_dict(d)


@app.post("/decisions")
def create_decision(decision: DecisionCreate):
    session = SessionLocal()

    existing = session.query(Decision).filter(Decision.decision_id == decision.decision_id).first()
    if existing:
        session.close()
        raise HTTPException(status_code=400, detail="Decision already exists")

    new_decision = Decision(
        decision_id=decision.decision_id,
        summary=decision.summary,
        rationale=decision.rationale,
        risks=decision.risks,
        source=decision.source,
        confidence=decision.confidence,
        status=decision.status,
        created_at=datetime.utcnow()
    )

    session.add(new_decision)
    session.commit()
    session.close()

    return {"message": "Decision created successfully"}


@app.get("/decisions/risks")
def decisions_with_risks():
    session = SessionLocal()
    decisions = session.query(Decision).filter(Decision.risks != None).all()
    result = [decision_to_dict(d) for d in decisions]
    session.close()
    return result


@app.get("/decisions/high-confidence")
def high_confidence(threshold: float = 0.8):
    session = SessionLocal()
    decisions = session.query(Decision).filter(Decision.confidence >= threshold).all()
    result = [decision_to_dict(d) for d in decisions]
    session.close()
    return result


@app.get("/decisions/timeline")
def timeline():
    session = SessionLocal()
    decisions = session.query(Decision).order_by(Decision.created_at.asc()).all()
    result = [decision_to_dict(d) for d in decisions]
    session.close()
    return result