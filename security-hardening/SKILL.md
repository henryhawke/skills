---
name: "security-hardening"
description: "Generate threat-driven hardening plans with control mapping, header strategy, and CI verification steps. Use when Codex needs a practical security posture for frontend, backend, or full-stack work with explicit assumptions, controls, and validation."
---

# Security Hardening

Separate threats, controls, and verification. Treat security as a checklist of explicit controls and gates rather than generic advice.

## Workflow
1. List the most relevant threats for the declared scope and sensitivity.
2. Map controls to known categories such as auth, session safety, injection, XSS, or dependency hygiene.
3. Define security headers and CSP strategy when web UI is in scope.
4. Return CI-suitable verification steps, including dependency audit expectations.

## Inputs
- System scope
- Data sensitivity
- Auth model

## Deliverables
- JSON with `threats`, `controls`, `headers`, `dependency_audit`, and `skill_log`
- Threat-model assumptions called out separately from verified controls

## Quality Gates
- Threats, controls, and verification are distinct sections.
- Dependency-audit behavior is explicit.
- Header and CSP guidance is concrete when applicable.
- Unknown security inputs are surfaced as assumptions, not fabricated facts.

## Prompt Scaffold
```text
SYSTEM
You are a security-first engineer.

USER
Inputs:
- System scope
- Data sensitivity
- Auth model

Task:
Produce a threat-led hardening plan and verification steps in JSON.

Output requirements:
- JSON with `threats`, `controls`, `headers`, `dependency_audit`, and `skill_log`
- Threat-model assumptions called out separately from verified controls
```
