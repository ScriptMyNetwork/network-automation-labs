import yaml

REQUIRED_FIELDS = [
    "decision_id",
    "title",
    "status",
    "decision_date",
    "owner",
    "context",
    "decision",
    "alternatives_considered",
    "consequences",
    "scope",
    "reversibility",
    "confidence",
]

VALID_STATUS = {"proposed", "approved", "rejected", "deprecated"}
VALID_REVERSIBILITY = {"easy", "medium", "hard"}
VALID_CONFIDENCE = {"low", "medium", "high"}


def load_decision_yaml(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def validate_decision(data: dict):
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "status" in data and data["status"] not in VALID_STATUS:
        errors.append(f"Invalid status: {data['status']}")

    if "reversibility" in data and data["reversibility"] not in VALID_REVERSIBILITY:
        errors.append(f"Invalid reversibility: {data['reversibility']}")

    if "confidence" in data and data["confidence"] not in VALID_CONFIDENCE:
        errors.append(f"Invalid confidence: {data['confidence']}")

    if errors:
        raise ValueError("Validation failed:\n" + "\n".join(errors))

    return True
