# config_compliance.py – Configuration Compliance Script

## Purpose
`config_compliance.py` is a Python script that checks whether Cisco IOS routers comply with a defined configuration standard.

The script connects to routers using SSH, reads their running configuration, validates specific configuration items, and generates a structured compliance report.

This script is **read-only**. It does not make any configuration changes on devices.

---

## What This Script Solves
In real networks, configuration standards are often verified manually by logging into devices and checking settings one by one. This does not scale and is error-prone.

This script automates that process by:
- Connecting to multiple routers automatically
- Validating configuration against defined rules
- Reporting PASS / FAIL results per device

---

## Files Used by the Script

### `config_compliance.py`
The main Python script that performs all compliance checks.

### `devices.yaml`
Inventory file containing device connection details:
- Device name
- Management IP address
- SSH username and password
- Enable secret

The script reads this file to know **which devices to check**.

---

## Compliance Standards Checked

The script validates the following configuration items:

1. **Hostname**
   - Hostname must start with `R`

2. **NTP Configuration**
   - NTP server must be configured as `10.0.0.1`

3. **Logging Configuration**
   - Logging server must be configured as `10.0.0.1`

4. **Banner MOTD**
   - Banner must match the approved standard text

Each check is independent. A device can fail one or multiple checks.

---

## How the Script Works (Step-by-Step)

1. Load device inventory from `devices.yaml`
2. Loop through each device in the inventory
3. Establish SSH connection using Netmiko
4. Enter enable mode using the enable secret
5. Retrieve the running configuration
6. Extract the actual hostname from the configuration
7. Run compliance checks:
   - Hostname validation
   - NTP server validation
   - Logging server validation
   - Banner validation
8. Collect all compliance issues for the device
9. Mark device as:
   - `PASS` → no issues found
   - `FAIL` → one or more issues found
10. Generate a timestamped JSON report

---

## Script Output

The script generates a JSON compliance report in the same directory.

### Example Output Structure

```json
{
  "timestamp": "2026-01-15T14:12:10",
  "compliance_results": [
    {
      "device": "R1",
      "ip": "10.0.0.2",
      "actual_hostname": "R1",
      "status": "PASS",
      "issues": []
    },
    {
      "device": "R2",
      "ip": "10.0.0.3",
      "actual_hostname": "R2",
      "status": "FAIL",
      "issues": [
        "NTP server configuration missing or incorrect",
        "Logging server configuration missing"
      ]
    }
  ]
}
