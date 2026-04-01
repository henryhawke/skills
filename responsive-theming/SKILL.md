---
name: "responsive-theming"
description: "Design responsive layouts, breakpoints, tokens, and preference-aware styling strategies for UI surfaces. Use when Codex needs a responsive or themed UI plan with explicit layout shifts, media-query behavior, and viewport test coverage."
---

# Responsive Theming

Prefer fluid layout first, introduce breakpoints only when the content demands it, and make preference-aware styling part of the contract rather than an afterthought.

## Workflow
1. Define the layout strategy with grid or flex decisions, width constraints, and content priorities.
2. Specify what changes at each breakpoint and why.
3. Include user-preference handling such as reduced motion, contrast, or color scheme when relevant.
4. Return a minimal styling strategy and a viewport test matrix.

## Inputs
- UI surface
- Content types
- Device targets or performance constraints

## Deliverables
- JSON with `layout_spec`, `breakpoints`, `styles`, `test_matrix`, and `skill_log`
- A mobile-first default unless the prompt overrides it

## Quality Gates
- Breakpoints explain their behavioral changes.
- At least one preference-aware consideration is evaluated when relevant.
- Viewport tests cover both layout and interaction regressions.
- Styling strategy matches the requested stack.

## Prompt Scaffold
```text
SYSTEM
You are a responsive UI engineer.

USER
Inputs:
- UI surface
- Content types
- Device targets or performance constraints

Task:
Produce a responsive layout plan, styling approach, test matrix, and a skill log in JSON.

Output requirements:
- JSON with `layout_spec`, `breakpoints`, `styles`, `test_matrix`, and `skill_log`
- A mobile-first default unless the prompt overrides it
```
