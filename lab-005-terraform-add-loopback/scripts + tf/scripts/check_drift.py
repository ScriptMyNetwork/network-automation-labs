import sys
import yaml
from netmiko import ConnectHandler

inventory_file = sys.argv[1]
drift_found = False

with open(inventory_file) as f:
    data = yaml.safe_load(f)

for router in data["routers"]:
    device = {
        "device_type": "cisco_ios",
        "host": router["ip"],
        "username": router["username"],
        "password": router["password"],
        "secret": router["password"],
    }

    print(f"Checking drift on {router['name']}")

    conn = ConnectHandler(**device)
    conn.enable()

    output = conn.send_command("show running-config interface Loopback0")

    expected_ip = router["loopback"]

    if expected_ip not in output or "Terraform_Managed" not in output:
        print(f"DRIFT DETECTED on {router['name']}")
        drift_found = True
    else:
        print(f"No drift on {router['name']}")

    conn.disconnect()

if drift_found:
    print("Drift detected.")
    sys.exit(0)   # IMPORTANT: do NOT fail Terraform

print("No drift detected on any device.")
