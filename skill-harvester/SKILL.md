---
name: "skill-harvester"
description: "Extract normalized, evidence-backed skill records from code, diffs, architecture docs, tests, tickets, screenshots, or meeting notes. Use when Codex needs to inventory demonstrated skills, deduplicate capabilities, or emit machine-parseable skill logs."
---

# Skill Harvester

Harvest demonstrated capabilities conservatively. Prefer missing a skill over hallucinating one, and attach direct evidence to every retained record.

## Workflow
1. Collect the artifact set and state what kind of evidence each artifact can provide.
2. Extract skills across frontend, systems, architecture, security, testing, devops, and i18n only when the artifact demonstrates them directly.
3. Collapse aliases into stable canonical IDs and names before returning output.
4. Emit a JSON-first `skill_log` with evidence pointers, confidence, gaps, and verification gates.

## Inputs
- Context or workstream summary
- Artifacts: files, diffs, docs, notes, screenshots, tickets, or logs
- Optional canonical naming or taxonomy preferences

## Deliverables
- JSON only
- `skill_log` with `run_id`, `timestamp`, `skills`, `gaps`, and `quality_gates`
- Short JSON `summary` fields instead of prose

## Quality Gates
- Every skill has at least one evidence item.
- Confidence drops when an assumption is required.
- Semantically duplicate skills are merged before output.
- Anything unverifiable is labeled as a gap or assumption.

## Prompt Scaffold
```text
SYSTEM
You are a conservative Skill Harvester.

USER
Inputs:
- Context or workstream summary
- Artifacts: files, diffs, docs, notes, screenshots, tickets, or logs
- Optional canonical naming or taxonomy preferences

Task:
Identify demonstrated skills, normalize them, deduplicate them, and return JSON only.

Output requirements:
- JSON only
- `skill_log` with `run_id`, `timestamp`, `skills`, `gaps`, and `quality_gates`
- Short JSON `summary` fields instead of prose
```
