from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database import SessionLocal
from app.models import Decision
from app.ai_engine import ask_question

app = FastAPI(title="Organizational Decision Memory API")


class DecisionCreate(BaseModel):
    decision_id: str
    summary: str
    rationale: Optional[str] = None
    risks: Optional[str] = None
    source: Optional[str] = None
    confidence: float = 0.5
    status: str = "active"


class QuestionRequest(BaseModel):
    question: str


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


@app.post("/ask")
def ask_ai(q: QuestionRequest):
    answer = ask_question(q.question)
    return {"answer": answer}


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