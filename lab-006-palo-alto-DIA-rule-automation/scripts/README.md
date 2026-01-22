# LAB006 – Palo Alto DIA Automation (Python)

## Purpose of This Lab

This lab demonstrates **programmatic automation of outbound (DIA) security policy** on a standalone Palo Alto firewall using **Python and the PAN-OS API**.

The automation focuses on enforcing **least-privilege internet access**, allowing traffic only to an approved external destination and service, while denying all other outbound traffic by default.

---

## Files in This Lab

This lab intentionally uses a **small, explicit file set** to keep the automation understandable, auditable, and easy to extend.

pa_dia.py
config.yaml

---

## `pa_dia.py`

### Description

`pa_dia.py` is the **main automation script** responsible for interacting with the Palo Alto firewall using the **PAN-OS XML API**.

It performs the following high-level actions:

- Authenticates to the firewall
- Creates required address and service objects
- Creates security policies enforcing DIA restrictions
- Commits configuration changes
- Fails fast on API or validation errors

The script is written to reflect **how firewalls actually operate**, rather than abstracting behavior behind tooling layers.

---

### Key Responsibilities

- **Firewall Authentication**  
  Generates an API key using supplied credentials.

- **Object Management**  
  Ensures required objects (source subnet, FQDN destination, service) exist before policy creation.

- **Security Policy Enforcement**  
  Creates explicit rules allowing:
  - Required supporting services (e.g., DNS)
  - Approved internet access to a specific destination and port

- **Configuration Commit**  
  Commits changes only after all objects and policies are defined successfully.

---

### Design Principles

- **Deterministic behavior**  
  Explicit API calls instead of inferred state.

- **Minimal abstraction**  
  API calls map directly to firewall configuration paths.

- **Fail-fast error handling**  
  Script exits immediately if the firewall rejects any configuration.

- **Production realism**  
  Reflects how many enterprise teams automate Palo Alto policy today.

---

## `config.yaml`

### Description

`config.yaml` is the **external configuration file** used by the Python script to separate **logic from environment-specific data**.

This allows the same script to be reused across environments without modification.

---

### What It Defines

- Firewall connection details
- Virtual system context
- Zone names
- Address object definitions
- FQDN destination definitions
- Service definitions
- Security policy naming

---

### Why YAML Is Used

- Human-readable
- Easy to audit and review
- Safer than hardcoding values in code
- Enables future expansion (multiple sites, environments, policies)

---

### Security Considerations

- Credentials are intentionally **not embedded in the Python code**
- Sensitive values are isolated in a single file
- The file is expected to be excluded from version control or populated locally

---

## Workflow Summary

1. Configuration values are read from `config.yaml`
2. The Python script authenticates to the firewall
3. Required objects are created or validated
4. Security rules enforcing DIA restrictions are created
5. The firewall configuration is committed
6. Traffic behavior is validated externally

---

## Key Learnings from This Lab

- Firewall automation requires strict alignment between zones, virtual systems, and policies
- Supporting services such as DNS must be explicitly allowed for higher-level policies to function
- Programmatic interfaces expose dependencies that are often hidden in GUI workflows
- Choosing the correct automation interface is critical for reliability

---

## Outcome

This lab results in a **repeatable, auditable, and least-privilege DIA security policy** implemented through code rather than manual configuration.

It demonstrates **real-world firewall automation practices** suitable for enterprise network and security engineering environments.

---

## Future Enhancements

Potential extensions include:

- Idempotency checks (GET-before-SET)
- Policy rollback and deletion support
- Multi-destination allow lists
- CI/CD pipeline integration
- Pre- and post-change validation checks

---

## Summary

This lab emphasizes **correctness, clarity, and operational relevance** over tooling complexity.

The `.py` and `.yaml` file separation reflects best practices for maintainable and scalable network security automation.
