# Lab-004 – Push ACL Configuration Automation (Scripts & YAML Reference)

This README documents the **three Python automation scripts** and the **YAML files** used in Lab-004.  
Together, these components implement an **enterprise-style workflow** for safely deploying, validating, and committing ACL configurations across multiple Cisco IOS routers.

---

## Overview of the Automation Workflow

The lab is intentionally split into **three distinct stages**, each handled by a separate script:

1. **Configuration Deployment** – Push ACL configuration to all devices
2. **Validation** – Verify that the correct configuration is in place on every device
3. **Commit** – Persist the validated configuration using `write memory`

YAML files are used to define **inventory** and **policy**, ensuring separation of data from logic.

---

## Python Scripts

### 1. `acl_config.py` – Push ACL Configuration

**Purpose**  
Deploys the ACL configuration to all routers and applies it to the specified interface.

**What the Script Does**
- Reads device inventory from `devices.yaml`
- Reads ACL policy from `acl_policy.yaml`
- Connects to each router using Netmiko
- Creates or updates the extended ACL
- Applies the ACL inbound on the specified interface
- Leaves the configuration in **running-config only**
- Does **not** perform validation logic
- Does **not** assume success implies correctness

**Key Characteristics**
- Multi-device execution
- Idempotent ACL creation
- No persistence to startup-config

**When to Run**
- First step in the workflow

---

### 2. `validate_config.py` – Validate Configuration State

**Purpose**  
Confirms that the intended ACL configuration is correctly applied on **all routers** before committing.

**What the Script Validates**
- ACL exists on the device
- ACL name matches the expected policy
- ACL rules are present and correct
- ACL is applied inbound on the correct interface

**What the Script Does Not Do**
- Does not modify configuration
- Does not write memory
- Does not rely on manual inspection

**Output Behavior**
- Prints PASS or FAIL per device
- Returns a non-zero exit code if any device fails
- Prevents unsafe commits

**When to Run**
- Immediately after `acl_config.py`
- Required gate before committing configuration

---

### 3. `commit_config.py` – Commit Configuration (Write Memory)

**Purpose**  
Persists the already-validated running configuration to startup-config.

**What the Script Does**
- Connects to all routers
- Executes `write memory`
- Confirms success per device
- Fails clearly if any device cannot save

**Important Notes**
- This script assumes validation has already passed
- No configuration logic is present
- No validation logic is present

**When to Run**
- Only after successful validation on all routers

---

## YAML Files

### `devices.yaml` – Device Inventory

**Purpose**  
Defines router connection parameters and metadata.

**Typical Contents**
- Device name (used for logging)
- Management IP address
- Username and password
- Device type (Cisco IOS)

**Design Considerations**
- Metadata such as `name` is used for reporting
- Only supported connection parameters are passed to Netmiko
- Inventory-driven automation allows easy scaling

**Why YAML**
- Human-readable
- Easy to extend with roles, sites, or environments
- Standard format in enterprise automation

---

### `acl_policy.yaml` – ACL Policy Definition

**Purpose**  
Defines the security policy independently from the Python code.

**What It Contains**
- ACL name
- Interface name
- Direction (inbound)
- Ordered list of ACL rules

**Policy Implemented in This Lab**
- Permit SSH (TCP/22) only from 10.0.0.1
- Deny all other traffic

**Why This Matters**
- Separates intent from implementation
- Enables policy reuse and modification without code changes
- Aligns with policy-as-code principles

---

## Recommended Execution Order

The scripts must be executed in the following order:

1. Push configuration  
python acl_config.py

pgsql
Copy code

2. Validate configuration  
python validate_config.py

pgsql
Copy code

3. Commit configuration  
python commit_config.py

yaml
Copy code

Skipping or reordering steps breaks the safety model.

---

## Enterprise Design Principles Demonstrated

- Separation of concerns (push, validate, commit)
- Inventory-driven automation
- Policy-as-code using YAML
- Deterministic, repeatable validation
- Safe multi-device configuration management
- CI/CD-compatible scripting model

---

## Summary

This lab intentionally avoids “single-script automation” in favor of a **controlled, enterprise-grade workflow**.  
Each script has a single responsibility, and YAML files provide a clean abstraction for inventory and policy.

This structure mirrors how real production networks implement automation at scale.
