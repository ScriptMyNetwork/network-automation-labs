import sys

from app.database import SessionLocal
from app.models import Decision
from app.ingestion.yaml_loader import load_decision_yaml, validate_decision


def ingest_decision(file_path: str):
    session = SessionLocal()

    try:
        data = load_decision_yaml(file_path)
        validate_decision(data)

        existing = session.query(Decision).filter(
            Decision.decision_id == data["decision_id"]
        ).first()

        if existing:
            print(f"Decision {data['decision_id']} already exists. Skipping.")
            return

        rationale_text = (
            f"Context:\n{data.get('context', '')}\n\n"
            f"Decision:\n{data.get('decision', '')}"
        )

        risks_text = None
        if "consequences" in data and "negative" in data["consequences"]:
            risks_text = "\n".join(data["consequences"]["negative"])

        source_link = None
        if data.get("references"):
            source_link = data["references"][0]

        decision = Decision(
            decision_id=data["decision_id"],
            summary=data["title"],
            rationale=rationale_text,
            risks=risks_text,
            source=source_link,
            confidence=1.0 if data.get("confidence") == "high" else
                       0.5 if data.get("confidence") == "medium" else
                       0.2
        )

        session.add(decision)
        session.commit()

        print(f"Decision {data['decision_id']} ingested successfully.")

    except Exception as e:
        session.rollback()
        print(f"Ingestion failed: {e}")

    finally:
        session.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ingest_decision.py <decision_yaml_path>")
        sys.exit(1)

    ingest_decision(sys.argv[1])
