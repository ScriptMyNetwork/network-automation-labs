import os
from openai import OpenAI
from app.database import SessionLocal
from app.models import Decision

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_context():
    session = SessionLocal()
    decisions = session.query(Decision).all()
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
    return context_text


def ask_question(question: str) -> str:
    context = build_context()

    prompt = f"""
You are an AI organizational memory assistant.

Use the decisions below to answer questions accurately.

{context}

Question: {question}

Answer clearly and concisely:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
