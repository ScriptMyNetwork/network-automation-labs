# LAB005 – Terraform Network Automation with Drift Detection & Auto-Remediation

## Overview

LAB005 demonstrates how Infrastructure as Code (IaC) principles can be applied to traditional network devices using Terraform as the orchestration layer and Python-based automation as the execution and inspection engine.

This lab moves beyond simple configuration push and introduces enterprise-grade concepts such as desired state enforcement, configuration drift detection, optional auto-remediation, and idempotent network changes. The overall design mirrors how real network automation platforms are built in production environments.

---

## Lab Objectives

By completing this lab, you will learn how to:

- Use Terraform to orchestrate network changes
- Maintain a single source of truth for network intent
- Detect configuration drift on live network devices
- Automatically remediate drift in a controlled manner
- Design automation workflows that scale toward enterprise platforms

---

## Topology

The lab uses a simple management-only topology.

Management Subnet: 10.0.0.0/24

| Device | Role | IP Address |
|------|------|------------|
| Linux Automation Host | Terraform and automation execution | 10.0.0.1 |
| R1 | Cisco IOS Router | 10.0.0.2 |
| R2 | Cisco IOS Router | 10.0.0.3 |
| R3 | Cisco IOS Router | 10.0.0.4 |

All devices are connected to the same Layer-2 switch in EVE-NG.

---

## Desired State (Intent)

Each router must have a Loopback interface configured as part of the desired state.

| Router | Loopback Interface |
|------|--------------------|
| R1 | Loopback0 with a unique /32 IP |
| R2 | Loopback0 with a unique /32 IP |
| R3 | Loopback0 with a unique /32 IP |

The loopback interface is treated as a managed resource and is used to demonstrate deterministic, low-risk network intent.

---

## Project Structure

The project follows a clean, enterprise-style repository structure.

lab005-terraform  
├── Terraform configuration files  
├── Inventory directory (source of truth)  
└── Automation scripts directory  

Design principles:

- Terraform is responsible for orchestration and control flow
- Automation scripts are responsible for device interaction
- Inventory defines intent and device-specific attributes
- No generic “push configuration” script is used

---

## How the Lab Works

### Drift Detection

Before making any changes, Terraform triggers a drift detection process. The automation logic connects to each router and validates the live configuration against the desired state defined in the inventory.

If the loopback interface is missing, modified, or removed, the system flags this as configuration drift.

### Auto-Remediation

When auto-remediation is enabled, Terraform proceeds to enforce the desired state after drift is detected. Missing or incorrect loopback configurations are automatically restored, and the network converges back to the defined intent.

Auto-remediation can be enabled or disabled via Terraform variables, allowing this lab to demonstrate both detect-only and self-healing workflows.

---

## Terraform Execution Flow

1. Terraform initializes and prepares state
2. Drift detection runs against live network devices
3. Drift is reported but does not block execution
4. Optional auto-remediation is triggered
5. The network converges back to the desired state

This execution model reflects how enterprise automation guardrails are implemented.

---

## Drift Simulation (Recommended)

To validate the lab:

1. Manually remove or modify the loopback configuration on any router
2. Re-run the Terraform apply workflow
3. Observe drift detection and automatic remediation

This confirms that the lab enforces intent rather than blindly pushing configuration.

---

## Key Learning Outcomes

- Terraform can be used as a control plane for network automation
- Drift detection must be logically separated from remediation
- Exit-code behavior directly impacts automation workflows
- Desired-state networking is achievable without SDN or controllers
- Enterprise-style automation relies on orchestration, not scripts

---

## Why This Lab Matters

Most network automation examples stop at pushing configuration to devices.

LAB005 demonstrates a fundamentally different approach:

- Guardrails are applied before changes
- Configuration drift is detected proactively
- Remediation is controlled and optional
- Changes are repeatable and idempotent
- The design aligns with real enterprise automation platforms

This lab forms the foundation for advanced topics such as GitOps pipelines, risk-based change approvals, and AI-assisted network operations.
