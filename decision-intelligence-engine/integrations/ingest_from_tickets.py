import json
import requests

API_URL = "http://127.0.0.1:8000/decisions"

with open("integrations/mock_tickets.json") as f:
    tickets = json.load(f)

for t in tickets:
    decision_payload = {
        "decision_id": f"DEC-TICKET-{t['ticket_id']}",
        "summary": t["title"],
        "rationale": t["description"],
        "risks": t["risk"],
        "source": t["ticket_id"],
        "confidence": 0.6,
        "status": "active"
    }

    r = requests.post(API_URL, json=decision_payload)

    if r.status_code == 200:
        print(f"Created decision from ticket {t['ticket_id']}")
    else:
        print(f"Failed for {t['ticket_id']}:", r.text)