import paramiko
from netmiko import ConnectHandler
import yaml
import time

paramiko.Transport._preffered_kex = (
    'diffie-hellman-group14-sha1',
    'diffie-hellman-group1-sha1'
)
paramiko.Transport._preffered_ciphers = (
    'aes128-cbc',
    '3des-cbc'
)

with open("devices.yaml") as f:
    inventory = yaml.safe_load(f)

for device in inventory["devices"]:
    print(f"\nConnecting to {device['name']}")

    conn = ConnectHandler(
        device_type=device["device_type"],
        host=device["host"],
        username=device["username"],
        password=device["password"],
        secret="cisco",
        use_keys=False,
        allow_agent=False,
        fast_cli=False,
        global_delay_factor=2,
    )

    conn.enable()
    time.sleep(1)

    output = conn.send_command_timing(
        "show running-config",
        strip_prompt=False,
        strip_command=False
    )

    hostname = conn.find_prompt().replace("#","").strip()
    filename = f"{hostname}_running_config.txt"
    
    with open(filename, "w") as f:
        f.write(output)

    print(f"Backup completed for {hostname}")
    conn.disconnect()

print("\nAll device backups completed.")
