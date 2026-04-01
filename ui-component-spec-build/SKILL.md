---
name: "ui-component-spec-build"
description: "Produce a compact component spec plus modular implementation guidance for React or TypeScript UI work. Use when Codex needs to design or build a component, page section, or frontend feature with explicit accessibility, responsiveness, state, testing, and maintainability requirements."
---

# UI Component Spec Build

Drive UI work from a compact contract: define props, states, interactions, accessibility, responsive behavior, tests, and implementation seams before code generation.

## Workflow
1. Start with the component API, states, error states, and loading behavior.
2. Write an accessibility plan that prefers semantic HTML and only adds ARIA when needed.
3. Define responsive behavior, state boundaries, and implementation seams.
4. Return code-file outputs together with tests and a skill log sidecar.

## Inputs
- Feature name
- Product context
- Constraints or existing stack conventions

## Deliverables
- Single JSON object
- Keys: `spec`, `a11y`, `responsive`, `state`, `tests`, `code_files`, `skill_log`
- At least two concrete example tests

## Quality Gates
- Semantic-first accessibility plan is explicit.
- Loading, empty, error, and success states are covered.
- Responsive changes are defined rather than implied.
- Implementation stays modular and testable.

## Prompt Scaffold
```text
SYSTEM
You are a senior frontend engineer and UI architect.

USER
Inputs:
- Feature name
- Product context
- Constraints or existing stack conventions

Task:
Build the requested UI surface and return spec, code plan, code files, tests, and a skill log.

Output requirements:
- Single JSON object
- Keys: `spec`, `a11y`, `responsive`, `state`, `tests`, `code_files`, `skill_log`
- At least two concrete example tests
```
