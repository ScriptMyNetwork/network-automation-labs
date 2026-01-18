from netmiko import ConnectHandler
import yaml
import sys

ACL_NAME = "SSH_MANAGEMENT_ONLY"
INTERFACE = "Ethernet1/0"
EXPECTED_RULES = [
    "permit tcp host 10.0.0.1 any eq 22",
    "deny ip any any"
]

with open("devices.yaml") as f:
    devices = yaml.safe_load(f)["routers"]

failed_devices = []

for device in devices:
    device_name = device["name"]    # keep for logging
    device.pop("name")              # remove before Netmiko

    print(f"\nValidating {device_name}")

    conn = ConnectHandler(**device)

    acl_output = conn.send_command(f"show ip access-lists {ACL_NAME}")
    intf_output = conn.send_command(f"show run interface {INTERFACE}")

    # ACL existence
    if ACL_NAME not in acl_output:
        print("FAIL: ACL not found")
        failed_devices.append(device_name)
        conn.disconnect()
        continue

    # Rule validation
    for rule in EXPECTED_RULES:
        if rule not in acl_output:
            print(f"FAIL: Missing rule -> {rule}")
            failed_devices.append(device_name)
            break

    # Interface binding validation
    if f"ip access-group {ACL_NAME} in" not in intf_output:
        print("FAIL: ACL not applied inbound on interface")
        failed_devices.append(device_name)

    conn.disconnect()
    print("PASS")

print("\n===== VALIDATION RESULT =====")

if failed_devices:
    print("Validation FAILED on:")
    for d in failed_devices:
        print(f" - {d}")
    sys.exit(1)
else:
    print("Validation PASSED on all routers")
    sys.exit(0)
