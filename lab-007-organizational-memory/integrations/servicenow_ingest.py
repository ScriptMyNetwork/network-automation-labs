import requests

INSTANCE = "https://dev354961.service-now.com"
USER = "admin"
PASS = "rJ/^Gfu9Q0kX"

DECISION_API = "http://127.0.0.1:8000/decisions"

def fetch_changes():
    url = f"{INSTANCE}/api/now/table/change_request"
    r = requests.get(url, auth=(USER, PASS))
    return r.json()["result"]

def fetch_incidents():
    url = f"{INSTANCE}/api/now/table/incident"
    r = requests.get(url, auth=(USER, PASS))
    return r.json()["result"]

def create_decision(ticket, ttype):
    payload = {
        "decision_id": f"DEC-SN-{ticket['number']}",
        "summary": ticket["short_description"],
        "rationale": ticket.get("description", ""),
        "risks": "Operational impact – derived from ServiceNow record",
        "source": ticket["number"],
        "confidence": 0.7,
        "status": "active"
    }
    r = requests.post(DECISION_API, json=payload)
    print(f"Decision created for {ticket['number']}:", r.status_code)

if __name__ == "__main__":
    for chg in fetch_changes():
        create_decision(chg, "change")
    for inc in fetch_incidents():
        create_decision(inc, "incident")