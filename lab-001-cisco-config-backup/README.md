# Lab 001 – Automate Cisco 7206 Configuration Backup Using Python

## Objective
Automate the backup of **running configurations** from multiple Cisco 7206 routers using Python.

By completing this lab, you will be able to:
- Connect to real Cisco IOS devices over SSH
- Execute operational CLI commands programmatically
- Store configuration backups in a **repeatable, consistent, and scalable** manner

This lab focuses on **day-to-day network operations automation**, not theory.

---

## Why This Lab Exists
In enterprise and ISP environments, network engineers are expected to:
- Take regular configuration backups
- Perform backups before and after configuration changes
- Recover quickly from misconfigurations or device failures

Performing these tasks manually via SSH does not scale and is error-prone.  
This lab demonstrates how to automate configuration backups using Python in a **safe, controlled, and auditable** way.

---

## Real-World Scenario
This lab simulates a common NOC / operations workflow where multiple network devices must be backed up reliably without manual intervention.

The automation:
- Eliminates repetitive manual logins
- Ensures configuration consistency across devices
- Enables version-controlled storage of configurations
- Forms the foundation for compliance and drift detection workflows

---

## Lab Topology
The lab is built entirely inside EVE-NG and consists of:

- **Ubuntu Server** – Automation host
- **Cisco 7206 Routers** – R1, R2
- **Management Network** – All devices connected to the same management segment

The Ubuntu server acts as the automation controller and initiates SSH connections to all routers.

---

## Automation Workflow
1. Load device inventory
2. Establish SSH connections using Netmiko
3. Execute `show running-config` on each router
4. Capture and store outputs as configuration backup files
5. Handle device connectivity sequentially for reliability

---

## Prerequisites

### Skills
- Basic Cisco IOS CLI
- Basic Python (variables, loops, conditionals)
- Basic Linux command-line usage

### Environment
- EVE-NG (Community or Pro)
- Cisco 7206 router images
- Ubuntu Server VM running inside EVE-NG

### Software
- Python 3
- Netmiko
- PyYAML

---

## Production Considerations
This lab is designed for learning, but mirrors real operational concerns:

- Credential handling can be extended using environment variables or vaults
- Scripts can be scheduled via `cron` for daily backups
- Output files can be version-controlled using Git
- Error handling can be expanded for unreachable devices
- Scalability considerations apply for large device inventories

---

## What Can Be Improved Next
- Encrypt or externalize credentials
- Add logging and execution timestamps
- Compare backups to detect configuration drift
- Integrate with monitoring or alerting systems
- Extend to additional platforms using NAPALM

---

## Outcome
After completing this lab, you will have built a **realistic network automation workflow** that reflects how configuration backups are handled in production environments using Python.

This lab serves as a foundation for more advanced automation, compliance, and monitoring use cases.
