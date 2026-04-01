---
name: "test-author-gate"
description: "Design user-centered unit, integration, and e2e test plans with coverage and anti-flake gates. Use when Codex needs to write or review a test strategy that spans levels, risk areas, CI reliability, and measurable pass criteria."
---

# Test Author Gate

Bias toward tests that mirror real behavior. Separate what belongs in unit, integration, and e2e layers, and encode coverage plus flake controls as explicit gates.

## Workflow
1. Write a testing strategy by level and justify what belongs in each layer.
2. Provide representative unit, integration, and e2e coverage targets for the feature.
3. Define coverage thresholds and CI behavior for failures.
4. Specify anti-flake controls such as actionability, retries, and tracing policy.

## Inputs
- Feature under test
- Risk areas
- Test levels required

## Deliverables
- JSON with `strategy`, `tests`, `coverage`, `e2e`, and `skill_log`
- At least one end-to-end flow outline

## Quality Gates
- Tests are organized by risk and execution level.
- Coverage thresholds are explicit.
- E2E guidance avoids sleeps and other flake-heavy patterns.
- User-observable behavior is prioritized over implementation details.

## Prompt Scaffold
```text
SYSTEM
You are a test engineer.

USER
Inputs:
- Feature under test
- Risk areas
- Test levels required

Task:
Return a layered test plan, coverage gates, and e2e reliability guidance in JSON.

Output requirements:
- JSON with `strategy`, `tests`, `coverage`, `e2e`, and `skill_log`
- At least one end-to-end flow outline
```
