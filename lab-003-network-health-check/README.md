# Lab 002 – Network Health Check Automation Using Python

## Objective
Automate daily network health checks for Cisco IOS devices using Python.

By completing this lab, you will be able to:
- Perform operational health checks across multiple network devices
- Detect common issues before they cause incidents
- Generate structured health reports suitable for NOC workflows

This lab focuses on **network operations and reliability**, not configuration changes.

---

## Why This Lab Exists
In real-world NOC and Managed Services environments, engineers perform daily checks such as:
- Verifying device reachability
- Identifying interfaces that are down unexpectedly
- Monitoring CPU utilization
- Ensuring time synchronization (NTP)

These checks are often done manually and inconsistently.  
This lab demonstrates how to **automate daily health validation** in a repeatable and scalable way.

---

## Real-World Scenario
This lab simulates the responsibilities of a NOC or Managed Services engineer responsible for maintaining network stability across multiple routers.

The automation:
- Reduces manual CLI checks
- Detects early warning signs of failure
- Produces clear pass/fail health summaries
- Creates a foundation for alerting and monitoring integration

---

## Lab Topology
The lab is built using EVE-NG and consists of:

- **Ubuntu Server** – Automation host
- **Cisco IOS Routers** – Multiple devices
- **Management Network** – Shared management connectivity

The Ubuntu server connects to each router over SSH to perform health checks.

---

## Health Checks Performed
The automation performs the following checks:

1. Device reachability over SSH
2. Interfaces that are down but not administratively shut
3. CPU utilization threshold validation
4. NTP configuration presence

Each check is designed to reflect real operational monitoring tasks.

---

## Automation Workflow
1. Load device inventory
2. Establish SSH connection using Netmiko
3. Execute health check commands
4. Parse command outputs
5. Evaluate results against thresholds
6. Generate per-device health status
7. Write summary reports to disk

---

## Output and Reporting
The script generates structured reports that include:
- Execution timestamp
- Per-device status (PASS / FAIL)
- Identified issues per device

Reports are stored in the `reports/` directory for auditing and review.

---

## Prerequisites

### Skills
- Cisco IOS CLI fundamentals
- Basic Python scripting
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
This lab mirrors production concerns such as:
- Threshold-based alerting
- Failure isolation per device
- Report-driven operations
- Scalability across device inventories

Future enhancements may include scheduling, alerting, and monitoring integration.

---

## What Can Be Improved Next
- Integrate results with Zabbix or Grafana
- Add alerting via email or messaging platforms
- Store health data in a database
- Replace CLI parsing with structured APIs
- Extend support to additional vendors

---

## Outcome
After completing this lab, you will have built a **NOC-style network health check automation** that reflects real-world operational practices.

This lab builds directly on Lab-001 and moves from task automation to **operational intelligence**.
