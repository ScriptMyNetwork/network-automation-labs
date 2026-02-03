# LAB-007 — AI Organizational Decision Memory & Change Risk Intelligence

## Overview

LAB-007 implements an **AI-powered Organizational Decision Memory and Change Risk Intelligence system**.

The platform captures infrastructure and operational decisions, understands how they relate, and uses AI to explain reasoning and predict the impact of change.

This project demonstrates how AI can function as **organizational memory** and support **risk-aware change management** for IT and Network teams.

---

## The Problem

In most environments:

- Teams forget why decisions were made
- Knowledge lives in tickets, emails, or people
- Architecture evolves without clear traceability
- Changes introduce hidden risks

When incidents occur, teams ask:

> “Why was this done?”  
> “What else depends on this?”  
> “What breaks if we change it?”

---

## The Solution

This system acts as a **decision intelligence platform**:

---

## Example Scenario (EVE-NG Lab)

A dual-ISP topology is used between sites in a lab environment.

A static route workaround is added during a failover issue.

The system stores:

- The architectural design decision
- The operational workaround decision
- The dependency relationship between them

The AI can then explain:

- Why the workaround was needed
- Risks such as routing asymmetry and blackholing
- What might be impacted if the design changes

This demonstrates how the platform supports **architecture reasoning and change risk awareness**.

---

## Use Cases

- IT & Network change governance  
- Post-incident knowledge retention  
- Architecture decision traceability  
- Risk-aware change planning  
- Operational memory for complex environments  

---

# Project Context

This lab is part of ScriptMyNetwork and represents an evolution from network automation into AI-assisted decision governance and change intelligence.

## EVE-NG Impact Demonstration

This scenario shows how an operational workaround decision can introduce architectural risk.

**Scenario**

- Dual ISP topology between sites  
- Primary link failure simulated  
- Static route added to restore traffic  

**Outcome**

The AI system explains how this tactical decision depends on the architecture and introduces risks such as routing asymmetry and troubleshooting complexity.

### Evidence

| Stage | Screenshot |
|------|------------|
| Primary path | ![](docs/lab13-primary-path.png) |
| Failover | ![](docs/lab13-failover-path.png) |
| Static workaround | ![](docs/lab13-static-route.png) |
| AI impact reasoning | ![](docs/lab13-ai-impact.png) |
