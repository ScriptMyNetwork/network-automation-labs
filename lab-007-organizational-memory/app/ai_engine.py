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

    context_text = "Organizational Decision Memory:\n\n"

    for d in decisions:
        context_text += f"""
Decision ID: {d.decision_id}
Summary: {d.summary}
Status: {d.status}
Rationale: {d.rationale}
Risks: {d.risks}
Confidence: {d.confidence}
Source: {d.source}
---
"""

    context_text += "\nDecision Relationships:\n"

    for l in links:
        context_text += f"{l.source_decision_id} {l.relationship_type} {l.target_decision_id}\n"

    return context_text


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