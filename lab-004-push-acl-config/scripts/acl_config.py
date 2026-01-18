from netmiko import ConnectHandler
import yaml

with open("devices.yaml") as f:
    devices = yaml.safe_load(f)["routers"]

with open("acl_policy.yaml") as f:
    acl = yaml.safe_load(f)

for device in devices:
    device_name = device["name"]          # Keep for logging
    device.pop("name")                     # Remove before Netmiko

    print(f"\nConnecting to {device_name}")

    conn = ConnectHandler(**device)

    config_commands = [
        f"ip access-list extended {acl['acl_name']}"
    ]

    for rule in acl["rules"]:
        config_commands.append(rule)

    config_commands.extend([
        "exit",
        f"interface {acl['interface']}",
        f"ip access-group {acl['acl_name']} {acl['direction']}",
        "exit"
    ])

    output = conn.send_config_set(config_commands)
    conn.save_config()

    print(output)
    conn.disconnect()
