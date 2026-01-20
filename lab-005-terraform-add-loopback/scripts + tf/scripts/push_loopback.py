import sys
import yaml
from netmiko import ConnectHandler

inventory_file = sys.argv[1]

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

    print(f"Applying loopback config on {router['name']}")

    conn = ConnectHandler(**device)
    conn.enable()

    commands = [
        "interface Loopback0",
        f"ip address {router['loopback']} 255.255.255.255",
        "description Terraform_Managed",
        "no shutdown"
    ]

    conn.send_config_set(commands)
    conn.save_config()
    conn.disconnect()
