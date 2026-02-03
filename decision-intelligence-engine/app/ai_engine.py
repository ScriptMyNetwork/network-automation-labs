import os
from openai import OpenAI
from app.database import SessionLocal
from app.models import Decision, DecisionLink

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_context():
    session = SessionLocal()
    decisions = session.query(Decision).all()
    links = session.query(DecisionLink).all()
    session.close()

    context = "Organizational Decisions:\n\n"

    for d in decisions:
        context += f"""
Decision ID: {d.decision_id}
Summary: {d.summary}
Status: {d.status}
Rationale: {d.rationale}
Risks: {d.risks}
Confidence: {d.confidence}
Source: {d.source}
---
"""

    context += "\nDecision Relationships:\n"
    for l in links:
        context += f"{l.source_decision_id} {l.relationship_type} {l.target_decision_id}\n"

    return context


def analyze_impact(decision_id: str):
    session = SessionLocal()
    links = session.query(DecisionLink).filter(
        (DecisionLink.source_decision_id == decision_id) |
        (DecisionLink.target_decision_id == decision_id)
    ).all()
    session.close()

    related = []
    for l in links:
        related.append(f"{l.source_decision_id} {l.relationship_type} {l.target_decision_id}")

    return "\n".join(related)


def ask_question(question: str) -> str:
    context = build_context()

    prompt = f"""
You are an AI organizational memory assistant.

Use the decisions and relationships below to answer questions accurately.

{context}

Question: {question}

Explain clearly:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def impact_analysis(decision_id: str) -> str:
    context = build_context()
    related = analyze_impact(decision_id)

    prompt = f"""
You are an AI architecture risk assistant.

A change is being considered to decision: {decision_id}

Related decision links:
{related}

Full organizational context:
{context}

Explain:
- What decisions may be impacted
- What risks could propagate
- What should engineers evaluate
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()