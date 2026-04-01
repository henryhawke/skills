---
name: "accessibility-gate"
description: "Run a testable accessibility review with WCAG mapping, keyboard and focus analysis, and semantic or ARIA remediation guidance. Use when Codex needs to audit a page or component and produce a formal accessibility gate instead of generic UX feedback."
---

# Accessibility Gate

Gate UI work against WCAG 2.2 AA and semantic correctness. Treat ARIA as a sharp tool, justify every usage, and map issues to explicit success criteria when possible.

## Workflow
1. Model keyboard interaction, focus order, and focus visibility.
2. Inspect semantic structure, names, roles, values, and announcement behavior.
3. Only recommend ARIA when semantic HTML cannot express the behavior, and list misuse risks when ARIA is necessary.
4. Return findings, WCAG mapping, remediations, tests, and a skill log.

## Inputs
- Artifact under review
- Primary user flows
- Target conformance level if not WCAG 2.2 AA

## Deliverables
- JSON with `findings`, `wcag_map`, `remediations`, `tests`, and `skill_log`
- Severity for each finding
- Explicit keyboard and screen-reader verification plan

## Quality Gates
- Every issue is tied to a behavior, criterion, or stated assumption.
- No blanket ARIA recommendations.
- Test plan covers keyboard, focus, and assistive technology impact.
- Remediation steps are concrete enough to implement.

## Prompt Scaffold
```text
SYSTEM
You are an accessibility gatekeeper.

USER
Inputs:
- Artifact under review
- Primary user flows
- Target conformance level if not WCAG 2.2 AA

Task:
Audit the artifact, map issues to WCAG where possible, and return a JSON remediation plan.

Output requirements:
- JSON with `findings`, `wcag_map`, `remediations`, `tests`, and `skill_log`
- Severity for each finding
- Explicit keyboard and screen-reader verification plan
```
