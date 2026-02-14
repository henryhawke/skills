---
name: subject-systems-auditor
description: End-to-end audit for one explicit subject (service, feature, workflow, API, system idea, or capability) across every system touchpoint. Use when a user asks to audit/review/assess one subject for bugs, regressions, security gaps, performance or cost issues, architecture risks, missing tests, operational gaps, and concrete optimization or innovation opportunities.
---

# Subject Systems Auditor

## Overview

Run a full, subject-scoped audit that traces how one target area touches the rest of the system. Produce prioritized findings with concrete fixes, optimization opportunities, and high-leverage innovation ideas.

## Inputs

- Capture the exact subject to audit.
- Capture scope constraints: repository roots, excluded directories, target environment, and timeline.
- Capture success criteria: risk reduction, latency, cost, quality, UX outcomes, or delivery speed.

If the subject is ambiguous, ask one focused clarification question, then continue.

## Workflow

### 1) Define Subject Boundary

- Normalize the subject into primary name, aliases, and related identifiers.
- Capture related identifiers such as routes, endpoints, tables, queue names, flags, jobs, and service names.
- Build a compact "audit seed list" of search terms.
- Start with exact terms first; expand to semantic neighbors only after direct matches are mapped.

### 2) Discover Every Touchpoint

- Search direct references and indirect references (callers, dependencies, configuration links).
- Include runtime config and environment variables.
- Include authentication and authorization rules.
- Include CI/CD and release pipelines.
- Include migrations and data model boundaries.
- Include background jobs, webhooks, and third-party integrations.
- Include observability surfaces (logs, metrics, traces, alerts, runbooks).
- Include documentation and operational playbooks.
- Use `scripts/find_touchpoints.sh "<comma-separated-terms>" <root>` for a first-pass map.

### 3) Build the End-to-End Contact Map

- Trace the path from inputs to side effects: inputs -> orchestration -> storage/integrations -> outputs.
- Mark trust boundaries, async edges, and failure points.
- Confirm no dead zones: every stage has validation, ownership, and telemetry.

### 4) Pull Supporting Skills and Context

- Inspect the available skills in the current session.
- Load only skills relevant to discovered touchpoints.
- Read only reference files needed for the current subject to keep context precise.
- If a useful skill is missing or unreadable, continue with direct analysis and note that limitation.

### 5) Audit with Multi-Lens Checks

Apply each lens to each touchpoint:
- Correctness: edge cases, race conditions, idempotency, data invariants.
- Reliability: retries, timeouts, partial failure handling, degradation behavior.
- Security and privacy: authn/authz coverage, secret handling, data exposure risk.
- Performance: latency hotspots, query or I/O inefficiency, unnecessary work.
- Cost: compute/network/storage waste, over-fetching, high-churn workflows.
- Test strategy: unit, integration, e2e, and failure-path coverage.
- Operability: log quality, metrics coverage, traceability, alert usefulness.
- Product and UX: user friction, confusing states, regressions in core flows.
- Maintainability: coupling, duplication, brittle abstractions, unclear ownership.

### 6) Propose Improvements and Innovations

- For each finding, include severity, evidence, recommendation, impact, and estimated effort.
- Add explicit optimization items for performance, cost, and developer velocity.
- Add innovation ideas that go beyond bug fixes: architectural simplifications, automation/tooling upgrades, product experience improvements, and instrumentation/experimentation opportunities.
- Favor high-leverage proposals over long low-value lists.

### 7) Validate and Close

- Run relevant tests, lint checks, and benchmarks where available.
- State exact blockers when validation cannot run.
- Deliver findings in the reporting format below.

## Reporting Format

Use this structure exactly:

1. Subject and Scope
2. End-to-End Contact Map
3. Findings (ordered by severity, each with evidence and fix)
4. Optimizations (performance, cost, operability)
5. Innovation Opportunities
6. Validation Performed and Remaining Gaps
7. Top 3 Next Actions

## Command Patterns

Use these defaults unless project instructions override:

```bash
rg -n -i -S "term1|term2|term3" .
rg --files .
rg -n "function_name|endpoint_path|table_name|event_name" .
```

For large repositories, start with narrowed directories and then expand.

## Resources

- Use `references/audit-checklist.md` for full touchpoint and scoring guidance.
- Use `scripts/find_touchpoints.sh` to bootstrap subject touchpoint discovery.
