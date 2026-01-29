from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database import SessionLocal
from app.models import Decision, DecisionLink
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


class LinkCreate(BaseModel):
    source_decision_id: str
    target_decision_id: str
    relationship_type: str


class QuestionRequest(BaseModel):
    question: str


def decision_to_dict(d):
    return {
        "decision_id": d.decision_id,
        "summary": d.summary,
        "status": d.status,
        "confidence": d.confidence
    }


@app.post("/ask")
def ask_ai(q: QuestionRequest):
    return {"answer": ask_question(q.question)}


@app.post("/decisions")
def create_decision(decision: DecisionCreate):
    session = SessionLocal()
    new_decision = Decision(**decision.dict(), created_at=datetime.utcnow())
    session.add(new_decision)
    session.commit()
    session.close()
    return {"message": "Decision created successfully"}


@app.get("/decisions")
def list_decisions():
    session = SessionLocal()
    decisions = session.query(Decision).all()
    result = [decision_to_dict(d) for d in decisions]
    session.close()
    return result


@app.post("/links")
def create_link(link: LinkCreate):
    session = SessionLocal()
    new_link = DecisionLink(**link.dict())
    session.add(new_link)
    session.commit()
    session.close()
    return {"message": "Link created"}


@app.get("/links")
def list_links():
    session = SessionLocal()
    links = session.query(DecisionLink).all()
    result = [
        {
            "source": l.source_decision_id,
            "target": l.target_decision_id,
            "relationship": l.relationship_type
        }
        for l in links
    ]
    session.close()
    return result