# health_check.py – Network Health Check Automation Script

## Purpose

`health_check.py` is a Python-based network health monitoring script designed to proactively assess the operational status of Cisco IOS devices.

The script connects to routers using SSH, executes standard operational commands, evaluates key health indicators (CPU, memory, uptime, and routing), and generates both console output and a structured JSON report.

This script is **read-only**. It does **not** make any configuration changes on network devices.

---

## What This Script Solves

In production networks, routine health checks are often performed manually by engineers logging into devices and validating multiple parameters. This approach is:

- Time-consuming  
- Inconsistent  
- Error-prone  
- Difficult to scale  

This script automates that process by:

- Connecting to multiple routers automatically  
- Running standardized health checks  
- Applying threshold-based logic  
- Reporting **PASS / WARNING / CRITICAL** states per check  
- Generating a machine-readable health report  

---

## Files Used by the Script

### `network_health_check.py`

The main Python script responsible for:

- Device connectivity
- Health validation logic
- Report generation

### `devices.yaml`

Inventory file containing device connection details:

- Device name  
- Management IP address  
- Device type (Netmiko platform)  
- SSH username and password  

The script reads this file to determine which devices to check.

---

## Health Checks Performed

The script validates the following operational health parameters:

### 1. CPU Utilization

- Command Used: `show processes cpu`
- Metric: 5-second CPU utilization
- Thresholds:
  - **PASS**: < 70%
  - **WARNING**: ≥ 70%
  - **CRITICAL**: ≥ 85%

---

### 2. Memory Utilization

- Command Used: `show processes memory`
- Metric: Processor Pool usage
- Thresholds:
  - **PASS**: < 75%
  - **WARNING**: ≥ 75%
  - **CRITICAL**: ≥ 90%

---

### 3. Device Uptime

- Command Used: `show version`
- Purpose: Detect recent reloads
- Logic:
  - Converts uptime to minutes
  - Flags devices with uptime below minimum threshold

- Threshold:
  - **CRITICAL**: Uptime < 10 minutes

---

### 4. Routing Table Health

- Command Used: `show ip route summary`
- Purpose: Verify presence of usable routes
- Logic:
  - Ignores headers and legend lines
  - Counts valid routing entries

- Result:
  - **PASS**: At least one valid route
  - **CRITICAL**: No usable routes found

---

## Output and Reporting

### Console Output

For each device, the script displays:

- Device name and IP
- Individual check status
- Associated metric values

Example status values:
- PASS
- WARNING
- CRITICAL
- UNKNOWN

---

### JSON Report

A structured report is generated at the end of execution:

**File:** `health_report.json`

The report includes:

- Device metadata
- Per-check results
- Status and metric values
- Error details (if any)

This file can be easily integrated with:
- Dashboards
- Monitoring systems
- CI/CD pipelines
- Future alerting mechanisms

---

## Error Handling

- Connection failures are gracefully handled
- Errors are captured per device
- Script continues execution even if one device fails

---

## Prerequisites

- Python 3.x
- Netmiko
- PyYAML

Install dependencies using:

```bash
pip install netmiko pyyaml
