---
name: "refactor-without-fear"
description: "Plan and execute behavior-preserving refactors with explicit invariants, checkpoints, and verification steps. Use when Codex needs to improve maintainability or structure without silently changing externally visible behavior."
---

# Refactor Without Fear

Refactor with declared invariants and proof points. Start by naming what must not change, then stage the work so every step can be verified before moving forward.

## Workflow
1. Declare invariants and user-visible behavior that must remain stable.
2. Split the refactor into small checkpoints with verification after each step.
3. Update or add tests alongside structural changes when the existing suite is not enough to preserve confidence.
4. Return a diff summary, gate results, and a skill log.

## Inputs
- Refactor target
- Motivation
- Constraints such as timebox or no-behavior-change requirements

## Deliverables
- JSON with `invariants`, `plan`, `changes`, `gates`, and `skill_log`
- Explicit no-behavior-change checks unless the prompt allows behavior changes

## Quality Gates
- Must-not-change behaviors are named before edits.
- Each step has a verification checkpoint.
- Tests or other proof points guard the refactor.
- Cleanup work does not silently broaden scope.

## Prompt Scaffold
```text
SYSTEM
You are a refactoring engineer.

USER
Inputs:
- Refactor target
- Motivation
- Constraints such as timebox or no-behavior-change requirements

Task:
Return a behavior-safe refactor plan, staged changes, verification gates, and a skill log in JSON.

Output requirements:
- JSON with `invariants`, `plan`, `changes`, `gates`, and `skill_log`
- Explicit no-behavior-change checks unless the prompt allows behavior changes
```
