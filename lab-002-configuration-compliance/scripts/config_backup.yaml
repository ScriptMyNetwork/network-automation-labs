#!/usr/bin/env python3

"""
Lab-002: Configuration Compliance Automation
Author: David John / ScriptMyNetwork

Validates Cisco IOS device configurations against defined standards.
"""

from netmiko import ConnectHandler
from datetime import datetime
import yaml
import json
import os

# ===============================
# COMPLIANCE STANDARDS
# ===============================
STANDARD_NTP_SERVER = "10.0.0.1"
STANDARD_LOGGING_SERVER = "10.0.0.1"
HOSTNAME_PREFIX = "R"

STANDARD_BANNER_TEXT = (
    "Authorized access only\n"
    "All activity is monitored and logged"
)

# ===============================
# UTILITY FUNCTIONS
# ===============================
def load_inventory(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def get_running_config(connection):
    return connection.send_command("show running-config", expect_string=r"#")


def get_actual_hostname(config):
    for line in config.splitlines():
        if line.startswith("hostname"):
            return line.split()[1]
    return "UNKNOWN"


# ===============================
# COMPLIANCE CHECKS
# ===============================
def check_hostname(actual_hostname):
    if actual_hostname.startswith(HOSTNAME_PREFIX):
        return None
    return "Hostname does not follow standard naming convention"


def check_ntp(config):
    if f"ntp server {STANDARD_NTP_SERVER}" in config:
        return None
    return "NTP server configuration missing or incorrect"


def check_logging(config):
    if f"logging {STANDARD_LOGGING_SERVER}" in config:
        return None
    return "Logging server configuration missing"


def check_banner(config):
    if "banner motd" not in config:
        return "Banner MOTD missing"

    if STANDARD_BANNER_TEXT not in config:
        return "Banner MOTD does not match standard"

    return None


# ===============================
# DEVICE COMPLIANCE
# ===============================
def check_device_compliance(device):
    result = {
        "device": device["name"],
        "ip": device["host"],
        "actual_hostname": None,
        "status": "PASS",
        "issues": []
    }

    try:
        netmiko_device = device.copy()
        netmiko_device.pop("name")

        connection = ConnectHandler(
            **netmiko_device,
            port=22,
            fast_cli=False,
            global_delay_factor=2
        )

        connection.enable()

        running_config = get_running_config(connection)
        actual_hostname = get_actual_hostname(running_config)
        result["actual_hostname"] = actual_hostname

        checks = [
            check_hostname(actual_hostname),
            check_ntp(running_config),
            check_logging(running_config),
            check_banner(running_config),
        ]

        for issue in checks:
            if issue:
                result["issues"].append(issue)

        if result["issues"]:
            result["status"] = "FAIL"

        connection.disconnect()

    except Exception as e:
        result["status"] = "FAIL"
        result["issues"].append(f"SSH/enable failure: {str(e)}")

    return result


# ===============================
# REPORTING
# ===============================
def generate_report(results):
    return {
        "timestamp": datetime.now().isoformat(),
        "compliance_results": results
    }


def save_report(report, file_path):
    with open(file_path, "w") as f:
        json.dump(report, f, indent=4)


# ===============================
# MAIN
# ===============================
def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    inventory_file = os.path.join(base_dir, "devices.yaml")
    report_file = os.path.join(
        base_dir,
        f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    devices = load_inventory(inventory_file)
    results = []

    for device in devices:
        results.append(check_device_compliance(device))

    report = generate_report(results)
    save_report(report, report_file)

    print("Configuration compliance check completed.")
    print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    main()
