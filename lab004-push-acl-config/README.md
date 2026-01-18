# Lab-004 – Push ACL Configuration Automation Using Python

## Overview
This lab demonstrates how to automate the deployment, validation, and persistence of security Access Control Lists (ACLs) across multiple Cisco IOS routers using Python and Netmiko.

The lab is intentionally designed to mirror real enterprise change-management workflows by strictly separating:
- Configuration deployment
- Post-change validation
- Configuration commit (write memory)

Configuration is persisted only after validation confirms that the intended state is correctly applied on all devices.

---

## Objective
Automate the following tasks across all routers:
- Create an extended ACL permitting SSH access only from a specific management IP
- Explicitly deny all other traffic
- Apply the ACL inbound on a defined interface
- Validate the configuration consistently on all routers
- Persist configuration only after successful validation

---

## Lab Environment

### Devices
- 3 x Cisco 7206 Routers
  - R1
  - R2
  - R3

### Management Network
- 10.0.0.0/24

### Credentials
- Username: admin
- Password: cisco

### Interface Used
- Ethernet1/0 (ACL applied inbound)

---

## ACL Policy Implemented

### Security Requirement
- Allow SSH (TCP/22) only from 10.0.0.1
- Deny all other traffic

### Logical ACL Configuration

ip access-list extended SSH_MANAGEMENT_ONLY
permit tcp host 10.0.0.1 any eq 22
deny ip any any
!
interface Ethernet1/0
ip access-group SSH_MANAGEMENT_ONLY in


---

## Automation Components

### Inventory
Devices are defined in a YAML inventory file with connection parameters and metadata.  
Metadata such as device name is used for logging and reporting, while only supported parameters are passed to Netmiko.

### Policy Definition
The ACL policy is defined in YAML to separate security intent from automation logic.  
This approach aligns with policy-as-code principles used in enterprise environments.

### Configuration Deployment
The ACL is pushed to all routers and applied to the specified interface.  
At this stage, configuration exists only in running-config.

### Validation
Post-change validation checks are executed on every router to confirm:
- ACL existence
- Correct ACL rules
- Correct interface binding and direction

Validation is deterministic and produces a clear pass/fail result per device.

### Commit
Only after all routers pass validation is the configuration persisted using write memory.  
No configuration changes are made during the commit phase.

---

## Execution Workflow

### Step 1 – Push ACL Configuration

python acl_config.py


This step:
- Creates the ACL
- Applies it inbound on Ethernet1/0
- Leaves the configuration in running-config only

---

### Step 2 – Validate Configuration


python validate_config.py


Expected output:


Validation PASSED on all routers


If any router fails validation, the workflow stops and the configuration is not committed.

---

### Step 3 – Commit Configuration


python commit_config.py


Expected output:


Write memory SUCCESSFUL on all routers


---

## Manual Validation Commands (Optional)

show ip access-lists SSH_MANAGEMENT_ONLY
show run interface Ethernet1/0
show users


SSH behavior verification:
- SSH from 10.0.0.1 → Allowed
- SSH from any other IP → Denied

---

## Enterprise Best Practices Demonstrated
- Separation of configuration, validation, and commit phases
- Fleet-wide configuration consistency enforcement
- YAML-driven inventory and policy definition
- Deterministic, repeatable validation logic
- Safe automation that minimizes risk of lockout
- CI/CD-compatible automation with clear exit codes

---

## Skills Demonstrated
- Network automation using Python
- Multi-device orchestration with Netmiko
- Security policy enforcement through automation
- Enterprise-style change management workflows
- Configuration validation and persistence control

---

## Notes
This lab is designed as a foundational enterprise automation pattern.  
It can be extended to include rollback automation, compliance drift detection, functional testing, and integration into CI/CD pipelines.

This lab builds directly on earlier automation labs and prepares the groundwork for advanced topics such as policy compliance, templating, and automated remediation.
