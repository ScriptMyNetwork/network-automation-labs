from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database import SessionLocal
from app.models import Decision, DecisionLink
from app.ai_engine import ask_question, impact_analysis

app = FastAPI(title="Organizational Decision Memory API")
templates = Jinja2Templates(directory="templates")


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


class ImpactRequest(BaseModel):
    decision_id: str


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ask")
def ask_ai(q: QuestionRequest):
    return {"answer": ask_question(q.question)}


@app.post("/impact")
def impact(req: ImpactRequest):
    return {"analysis": impact_analysis(req.decision_id)}


@app.post("/decisions")
def create_decision(decision: DecisionCreate):
    session = SessionLocal()
    new_decision = Decision(**decision.dict(), created_at=datetime.utcnow())
    session.add(new_decision)
    session.commit()
    session.close()
    return {"message": "Decision created successfully"}


@app.post("/links")
def create_link(link: LinkCreate):
    session = SessionLocal()
    new_link = DecisionLink(**link.dict())
    session.add(new_link)

    if link.relationship_type == "replaces":
        target = session.query(Decision).filter(
            Decision.decision_id == link.target_decision_id
        ).first()
        if target:
            target.status = "deprecated"

    session.commit()
    session.close()
    return {"message": "Link created and lifecycle updated"}


@app.get("/timeline")
def timeline():
    session = SessionLocal()
    decisions = session.query(Decision).order_by(Decision.created_at.asc()).all()
    result = [
        {
            "decision_id": d.decision_id,
            "summary": d.summary,
            "status": d.status,
            "created_at": d.created_at
        }
        for d in decisions
    ]
    session.close()
    return result


@app.get("/system-overview")
def overview():
    session = SessionLocal()
    total = session.query(Decision).count()
    active = session.query(Decision).filter(Decision.status == "active").count()
    deprecated = session.query(Decision).filter(Decision.status == "deprecated").count()
    links = session.query(DecisionLink).count()
    session.close()

    return {
        "total_decisions": total,
        "active_decisions": active,
        "deprecated_decisions": deprecated,
        "relationship_links": links
    }