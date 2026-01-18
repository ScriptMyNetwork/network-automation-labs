from netmiko import ConnectHandler
import yaml
import sys

with open("devices.yaml") as f:
    devices = yaml.safe_load(f)["routers"]

failed_devices = []

for device in devices:
    device_name = device["name"]    # keep for logging
    device.pop("name")              # remove before Netmiko

    print(f"\nCommitting configuration on {device_name}")

    try:
        conn = ConnectHandler(**device)
        output = conn.save_config()
        print(output)
        conn.disconnect()
        print("PASS: Configuration saved")

    except Exception as e:
        print(f"FAIL: Could not save config -> {e}")
        failed_devices.append(device_name)

print("\n===== COMMIT RESULT =====")

if failed_devices:
    print("Write memory FAILED on:")
    for d in failed_devices:
        print(f" - {d}")
    sys.exit(1)
else:
    print("Write memory SUCCESSFUL on all routers")
    sys.exit(0)
