import sys

from app.database import SessionLocal
from app.models import Decision


def list_all_decisions(session):
    decisions = session.query(Decision).all()
    print("\n--- ALL DECISIONS ---")
    for d in decisions:
        print(f"{d.decision_id} | {d.summary} | status={d.status} | confidence={d.confidence}")
    print("---------------------\n")


def get_decision_by_id(session, decision_id):
    d = session.query(Decision).filter(Decision.decision_id == decision_id).first()
    if not d:
        print("Decision not found.")
        return

    print("\n--- DECISION DETAIL ---")
    print(f"ID: {d.decision_id}")
    print(f"Summary: {d.summary}")
    print(f"Status: {d.status}")
    print(f"Rationale:\n{d.rationale}")
    print(f"Risks:\n{d.risks}")
    print(f"Source: {d.source}")
    print(f"Confidence: {d.confidence}")
    print(f"Created At: {d.created_at}")
    print("------------------------\n")


def list_recent_decisions(session, limit=5):
    decisions = (
        session.query(Decision)
        .order_by(Decision.created_at.desc())
        .limit(limit)
        .all()
    )

    print(f"\n--- Last {limit} Decisions ---")
    for d in decisions:
        print(f"{d.created_at} | {d.decision_id} | {d.summary} | status={d.status}")
    print("------------------------------\n")


def decision_timeline(session):
    decisions = session.query(Decision).order_by(Decision.created_at.asc()).all()

    print("\n=== DECISION TIMELINE ===")
    for d in decisions:
        print(f"{d.created_at} → {d.decision_id} → {d.summary} (status={d.status})")
    print("=========================\n")


def deprecate_decision(session, decision_id):
    d = session.query(Decision).filter(Decision.decision_id == decision_id).first()
    if not d:
        print("Decision not found.")
        return

    d.status = "deprecated"
    session.commit()
    print(f"Decision {decision_id} marked as deprecated.")


def decisions_with_risks(session):
    decisions = session.query(Decision).filter(Decision.risks != None).all()
    print("\n--- DECISIONS WITH RISKS ---")
    for d in decisions:
        print(f"{d.decision_id} | {d.summary} | risks={d.risks}")
    print("-----------------------------\n")


def high_confidence_decisions(session, threshold=0.8):
    decisions = session.query(Decision).filter(Decision.confidence >= threshold).all()
    print(f"\n--- DECISIONS WITH CONFIDENCE >= {threshold} ---")
    for d in decisions:
        print(f"{d.decision_id} | {d.summary} | confidence={d.confidence}")
    print("----------------------------------------------\n")


def decisions_by_source(session, source):
    decisions = session.query(Decision).filter(Decision.source == source).all()
    print(f"\n--- DECISIONS FROM SOURCE: {source} ---")
    for d in decisions:
        print(f"{d.decision_id} | {d.summary}")
    print("---------------------------------------\n")


def main():
    session = SessionLocal()

    try:
        if len(sys.argv) < 2:
            print("Usage:")
            print("  list | get <ID> | recent [limit] | timeline")
            print("  deprecate <ID> | risks | highconf [threshold] | source <url>")
            return

        cmd = sys.argv[1]

        if cmd == "list":
            list_all_decisions(session)
        elif cmd == "get":
            get_decision_by_id(session, sys.argv[2])
        elif cmd == "recent":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            list_recent_decisions(session, limit)
        elif cmd == "timeline":
            decision_timeline(session)
        elif cmd == "deprecate":
            deprecate_decision(session, sys.argv[2])
        elif cmd == "risks":
            decisions_with_risks(session)
        elif cmd == "highconf":
            threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
            high_confidence_decisions(session, threshold)
        elif cmd == "source":
            decisions_by_source(session, sys.argv[2])
        else:
            print("Unknown command")

    finally:
        session.close()


if __name__ == "__main__":
    main()
