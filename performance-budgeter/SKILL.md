---
name: "performance-budgeter"
description: "Create measurable performance budgets, Core Web Vitals targets, and verification plans for web surfaces. Use when Codex needs a concrete performance plan with remediation priorities instead of vague optimization advice."
---

# Performance Budgeter

Do not claim wins you cannot measure. Define budgets, explain the measurement method, and tie remediation ideas to explicit verification steps.

## Workflow
1. Set budgets for LCP, INP, CLS, and any additional local constraints.
2. Separate field measurement from lab measurement and state where results should be logged.
3. Prioritize likely causes and remediation ideas such as code splitting, caching, rendering strategy, or asset changes.
4. Return a prioritized action plan with verification steps.

## Inputs
- Page or flow under analysis
- Known bottlenecks
- Perf target overrides if any

## Deliverables
- JSON with `budgets`, `measurement`, `actions`, and `skill_log`
- Each action includes a verification method

## Quality Gates
- Budgets are numeric and testable.
- Measurement distinguishes field and lab data.
- Actions are prioritized by expected impact.
- No unverified improvement claims.

## Prompt Scaffold
```text
SYSTEM
You are a performance engineer.

USER
Inputs:
- Page or flow under analysis
- Known bottlenecks
- Perf target overrides if any

Task:
Define budgets, measurement, actions, and verification steps in JSON.

Output requirements:
- JSON with `budgets`, `measurement`, `actions`, and `skill_log`
- Each action includes a verification method
```
