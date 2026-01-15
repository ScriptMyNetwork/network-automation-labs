# Lab 002 – Configuration Compliance Automation Using Python

## Overview
This lab demonstrates how to automate **configuration compliance checks** on Cisco IOS routers using Python and Netmiko.

Instead of manually logging into devices to verify standards, the automation validates each router against a **defined configuration baseline** and generates a structured compliance report.

This lab focuses on **governance, audit readiness, and configuration drift detection**, not configuration deployment.

---

## Lab Topology
The lab is built in EVE-NG and consists of:

- Ubuntu Linux VM (Automation Host)
- Cisco IOS Routers: R1, R2, R3
- One L2 switch providing a shared management network

The Ubuntu VM connects to all routers over SSH to retrieve and validate running configurations.

(Topology diagram included in the repository.)

---

## Scope

### In Scope
- Read-only validation of running configuration
- Configuration compliance checks against defined standards
- PASS / FAIL compliance reporting
- Detection of missing or non-compliant configuration elements

### Out of Scope
- Configuration remediation (auto-fix)
- Configuration deployment
- Multi-vendor support
- Monitoring, alerting, or dashboards

These are intentionally excluded to keep the lab focused on **compliance detection and governance**.

---

## Configuration Standards Enforced
The automation validates the following standards:

- Hostname must start with `R`
- NTP server must be configured as `10.0.0.1`
- Logging server must be configured as `10.0.0.1`
- Banner MOTD must match the approved text
- Device must be reachable via SSH and enter enable mode

Each standard is evaluated independently.

---

## Device Configuration States

Routers are intentionally configured with different compliance states to validate detection logic.

### R1 – Fully Compliant
- Correct hostname
- Correct NTP configuration
- Correct logging configuration
- Correct banner

Expected result: **PASS**

---

### R2 – Partially Non-Compliant
- Correct hostname
- Missing NTP configuration
- Missing logging configuration
- Correct banner

Expected result: **FAIL**

---

### R3 – Non-Compliant
- Correct hostname
- Incorrect NTP server
- Missing logging configuration
- Incorrect banner

Expected result: **FAIL**

---

## Inventory vs Device Hostname

The device name defined in `devices.yaml` represents the **expected identity** of the device, not necessarily the configured hostname.

The automation retrieves the **actual hostname** from the running configuration and validates it against the defined standard. This allows detection of hostname drift without relying solely on inventory labels.

This mirrors real-world automation systems where inventory and device state are treated separately.

---

## Compliance Workflow

1. Load device inventory from `devices.yaml`
2. Connect to each router via SSH using Netmiko
3. Enter enable mode
4. Retrieve running configuration
5. Extract actual hostname from configuration
6. Validate configuration against defined standards
7. Record compliance issues per device
8. Generate a timestamped JSON compliance report

---

## Script Execution
The compliance automation is executed from the Ubuntu Linux VM using a Python virtual environment.

- Script: `config_compliance.py`
- Inventory: `devices.yaml`
- Output: JSON compliance report

The script processes devices sequentially and handles SSH or enable-mode failures gracefully.

---

## Output and Reporting
The script generates a structured JSON report containing:

- Execution timestamp
- Device name and management IP
- Actual hostname detected
- Compliance status (PASS / FAIL)
- List of compliance issues per device

This output format is suitable for audits, reviews, and future integration with reporting tools.

(Sample output included in the repository.)

---

## Known Limitations
- Banner validation uses simple string matching and does not handle formatting variations
- Compliance checks rely on CLI output parsing
- Devices are processed sequentially
- No historical compliance tracking is stored

These limitations are acceptable for learning purposes and can be addressed in future enhancements.

---

## Why This Lab Matters
Configuration drift is a common cause of outages and audit failures in enterprise networks.

This lab demonstrates how automation can be used to:
- Consistently validate configuration standards
- Reduce manual verification effort
- Detect drift after changes or incidents
- Improve audit and governance readiness

The same approach can be extended to security baselines, remediation workflows, and CI/CD-style validation.

---

## Lab Status
**Completed**

This lab builds on Lab-001 (Configuration Backup) and provides a foundation for:
- Lab-003: Network Health Checks and Monitoring Automation
