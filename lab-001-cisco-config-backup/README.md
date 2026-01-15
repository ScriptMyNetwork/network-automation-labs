# Lab 001 – Automate Cisco 7206 Configuration Backup Using Python

## Objective
Automate the backup of running configurations from multiple Cisco 7206 routers using Python.  
By the end of this lab, you will be able to connect to real Cisco IOS devices via SSH, execute operational commands, and store configuration backups in a repeatable and scalable way.

This lab focuses on **day-to-day network operations automation**, not theory.

---

## Real-World Scenario
In enterprise and ISP environments, network engineers are expected to:
- Take regular configuration backups
- Perform backups before and after changes
- Recover quickly from misconfigurations

Doing this manually via SSH does not scale and is error-prone.  
This lab demonstrates how to automate this task using Python in a safe and controlled way.

---

## Lab Topology

- Ubuntu Server (Automation Host)
- Cisco 7206 Routers (R1, R2)
- All devices connected to the same management network

The Ubuntu server acts as the automation controller and initiates SSH connections to all routers.

---

## Prerequisites

### Skills
- Basic Cisco IOS CLI
- Basic Python (variables, loops)
- Basic Linux command line

### Environment
- EVE-NG (Community or Pro)
- Cisco 7206 router images
- Ubuntu Server VM inside EVE-NG

### Software
- Python 3
- Netmiko
- PyYAML
