from yaml_loader import load_decision_yaml, validate_decision

FILE_PATH = "../../decisions/001-use-netmiko-over-napalm.yaml"

data = load_decision_yaml(FILE_PATH)
validate_decision(data)

print("YAML loaded and validated successfully")
print(data)
