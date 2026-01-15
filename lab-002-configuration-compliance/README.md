# Lab 002 – Configuration Compliance Automation Using Python

## Objective
Automate configuration compliance checks for Cisco IOS devices using Python.

By completing this lab, you will be able to:
- Validate device configurations against a defined standard
- Detect missing or non-compliant configuration elements
- Generate clear compliance reports suitable for audits and operations teams

This lab focuses on **configuration standards, governance, and drift detection**, not device health or monitoring.

---

## Why This Lab Exists
In enterprise and ISP environments, network devices are expected to follow strict configuration standards, such as:
- Mandatory NTP servers
- Centralized logging configuration
- Standardized banners
- Consistent hostname formats

Over time, manual changes, rushed fixes, or misconfigurations lead to **configuration drift**.

This lab demonstrates how to automatically verify that devices comply with a **baseline configuration standard**, reducing audit risk and operational errors.

---

## Real-World Scenario
This lab simulates a scenario where a network engineer or automation engineer must:
- Verify device compliance during audits
- Validate configurations after change windows
- Ensure all devices meet organizational standards

Instead of manually checking configurations on each device, automation performs these checks **consistently and repeatably**.

---

## Lab Topology
The lab is built using EVE-NG and consists of:

- **Ubuntu Server** – Automation host
- **Cisco IOS Routers** – R1, R2, R3
- **Management Network** – Shared management connectivity

The Ubuntu server connects to each router over SSH to retrieve and validate configurations.

---

## Compliance Checks Performed
The automation validates device configurations against predefined standards, including:

- Hostname format validation
- NTP server configuration presence
- Logging configuration presence
- Banner MOTD compliance against a standard template

Each check is evaluated independently to identify **missing or non-compliant settings**.

---

## Automation Workflow
1. Load device inventory
2. Load standard configuration template
3. Establish SSH connection using Netmiko
4. Retrieve running configuration
5. Compare device configuration against the standard
6. Identify missing or non-compliant configuration items
7. Assign compliance status per device
8. Generate a structured compliance report

---

## Output and Reporting
The script generates compliance reports that include:
- Execution timestamp
- Per-device compliance status (PASS / FAIL)
- List of missing configuration elements
- List of non-compliant configuration elements

Reports are stored in the `reports/` directory for audit and review purposes.

---

## Prerequisites

### Skills
- Cisco IOS CLI fundamentals
- Basic Python scripting
- Understanding of standard network configurations
- Linux command-line usage

### Environment
- EVE-NG (Community or Pro)
- Cisco IOS router images
- Ubuntu Server VM inside EVE-NG

### Software
- Python 3
- Netmiko
- PyYAML

---

## Production Considerations
This lab mirrors real-world configuration governance concerns such as:
- Configuration drift detection
- Audit readiness
- Repeatable compliance validation
- Separation of standards and device-specific configuration

Future enhancements may include role-based standards, multi-vendor support, and integration with CI/CD pipelines.

---

## What Can Be Improved Next
- Support multiple configuration templates
- Add configuration remediation (auto-fix)
- Integrate with version control for standards
- Generate HTML or dashboard-based reports
- Extend compliance checks to security configurations

---

## Outcome
After completing this lab, you will have built a **configuration compliance automation workflow** that reflects real-world enterprise practices.

This lab builds on Lab-001 and moves beyond backups into **standards enforcement and configuration governance**.
