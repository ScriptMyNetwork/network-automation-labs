# LAB005 – Automation Scripts and Terraform Configuration

This document explains the purpose, behavior, and interaction of the **Python automation scripts** and **Terraform configuration files** used in LAB005.

The goal is to clearly separate **orchestration**, **inspection**, and **enforcement**, following enterprise network automation design principles.

---

## Design Overview

LAB005 follows a strict separation of responsibilities:

- **Terraform** acts as the orchestration and policy layer
- **Python scripts** handle device-level interaction
- **Inventory files** define the desired state (intent)

Terraform never connects directly to network devices.  
All device communication is delegated to Python automation.

---

## Python Scripts

The `scripts/` directory contains the execution and inspection logic.

### 1. check_drift.py

**Purpose:**  
Detect configuration drift without making any changes.

**Role in the workflow:**
- Connects to each router
- Reads the live Loopback interface configuration
- Compares live state with intended state
- Reports drift clearly in the Terraform output
- Does not block Terraform execution

**Key Characteristics:**
- Read-only
- Safe to run repeatedly
- Designed to surface drift, not enforce policy
- Exit behavior allows Terraform to continue

This script represents the **inspection layer** of the automation workflow.

---

### 2. push_loopback.py

**Purpose:**  
Enforce the desired Loopback configuration on all routers.

**Role in the workflow:**
- Connects to each router
- Creates or corrects the Loopback interface
- Applies the intended IP address
- Ensures the interface is enabled
- Saves the running configuration

**Key Characteristics:**
- Deterministic and idempotent
- Can be safely re-run multiple times
- Only enforces a single, well-defined intent
- Used exclusively for auto-remediation

This script represents the **enforcement layer** of the automation workflow.

---

## Terraform Configuration Files

Terraform is used to orchestrate *when* scripts run and *under what conditions*.

---

### providers.tf

**Purpose:**  
Defines Terraform version constraints.

**Why it exists:**
- Ensures consistent Terraform behavior
- Prevents version-related incompatibilities
- Aligns with enterprise Terraform standards

---

### variables.tf

**Purpose:**  
Defines configurable inputs for the automation workflow.

**Key variables:**
- Inventory file location
- Auto-remediation toggle

**Why it matters:**
- Enables policy-based behavior
- Allows the same code to support detect-only or self-healing modes
- Keeps logic out of scripts and inside Terraform

---

### terraform.tfvars

**Purpose:**  
Supplies runtime values for Terraform variables.

**Why it matters:**
- Separates configuration from logic
- Makes behavior changes explicit and auditable
- Allows quick enable/disable of auto-remediation

This file represents **policy selection**, not implementation.

---

### main.tf

**Purpose:**  
Defines the orchestration flow between drift detection and remediation.

**Execution logic:**
1. Drift detection runs first
2. Drift is reported but does not halt execution
3. Auto-remediation runs only if enabled
4. Desired state is enforced consistently

**Why null_resource is used:**
- Network devices are not Terraform-native resources
- local-exec allows Terraform to orchestrate external automation safely
- This pattern mirrors real-world network automation platforms

---

## Execution Model

Terraform is always executed from the root directory:

- Drift detection is triggered on every apply
- Auto-remediation is conditional
- Repeated applies are safe and idempotent

This ensures:
- No blind configuration pushes
- Clear visibility into drift
- Controlled enforcement of intent

---

## Why This Design Matters

This structure avoids common network automation anti-patterns:

- No monolithic scripts
- No hidden logic inside Python
- No uncontrolled configuration pushes
- No device-specific logic inside Terraform

Instead, it demonstrates:

- Clear separation of concerns
- Policy-driven automation
- Enterprise-aligned workflows
- A foundation for GitOps and CI/CD integration

---

## Summary

LAB005 uses a deliberately simple configuration example to demonstrate complex, real-world automation concepts.

The combination of:
- Terraform orchestration
- Read-only drift detection
- Optional auto-remediation
- Inventory-driven intent

creates a pattern that scales naturally toward enterprise network automation platforms and future MVP development.
