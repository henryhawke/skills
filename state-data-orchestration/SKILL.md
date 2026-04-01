---
name: "state-data-orchestration"
description: "Design state boundaries, reducers, failure modes, and error-boundary placement for complex UI features. Use when Codex needs to reason about local state, shared state, server data, URL state, optimistic updates, or resilience before implementation."
---

# State Data Orchestration

Classify state deliberately, define invariants, and make failure handling first-class. Prefer the simplest state model that still scales under the feature’s complexity.

## Workflow
1. Partition state into local UI, shared UI, server or cache, and URL state.
2. Choose the simplest viable ownership model, escalating to reducers only when complexity warrants it.
3. Document transitions, invariants, retries, partial rendering, and rollback behavior.
4. Specify error-boundary placement and return tests together with the orchestration model.

## Inputs
- Feature name
- Data sources
- Concurrency or optimistic update concerns

## Deliverables
- JSON with `state_model`, `reducer`, `error_handling`, `tests`, and `skill_log`
- Text state diagram or transition table

## Quality Gates
- All major state classes are accounted for.
- Failure modes have user-facing handling paths.
- Reducer actions and transitions are explicit when reducers are used.
- Error-boundary placement is justified.

## Prompt Scaffold
```text
SYSTEM
You are a state management architect.

USER
Inputs:
- Feature name
- Data sources
- Concurrency or optimistic update concerns

Task:
Define state boundaries, transitions, resilience patterns, and tests, then return JSON.

Output requirements:
- JSON with `state_model`, `reducer`, `error_handling`, `tests`, and `skill_log`
- Text state diagram or transition table
```
