---
name: "architecture-adr-pack"
description: "Produce durable architecture artifacts such as ADRs, C4-style diagrams, API semantics notes, and implementation roadmaps. Use when Codex needs to formalize system design decisions instead of only describing architecture informally."
---

# Architecture ADR Pack

Turn architectural intent into durable artifacts. Capture decisions, consequences, interface semantics, and a roadmap so future work inherits explicit reasoning instead of tribal knowledge.

## Workflow
1. Write ADRs with context, decision, and consequences.
2. Provide context and container-level diagrams in Mermaid.
3. Spell out API semantics, retries, idempotency, and error-model notes.
4. Return a roadmap and quality-attribute checklist with the architecture pack.

## Inputs
- System goal
- Key constraints
- Important integrations

## Deliverables
- JSON with `adrs`, `c4_mermaid`, `api_semantics`, `roadmap`, and `skill_log`
- At least two ADRs unless the prompt narrows the scope

## Quality Gates
- ADRs include consequences rather than only decisions.
- Diagrams are consistent with the written interfaces.
- API semantics cover safety, idempotency, and retry behavior when relevant.
- Roadmap calls out quality attributes, not only features.

## Prompt Scaffold
```text
SYSTEM
You are a software architect.

USER
Inputs:
- System goal
- Key constraints
- Important integrations

Task:
Return ADRs, diagrams, interface semantics, roadmap, and a skill log as JSON.

Output requirements:
- JSON with `adrs`, `c4_mermaid`, `api_semantics`, `roadmap`, and `skill_log`
- At least two ADRs unless the prompt narrows the scope
```
