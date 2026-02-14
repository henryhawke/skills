# End-to-End Subject Audit Checklist

Use this checklist to ensure the audit is complete and consistent.

## 1) Subject Definition

- Confirm exact subject name.
- Confirm aliases, abbreviations, and old names.
- Confirm related identifiers (routes, APIs, events, tables, jobs, flags).
- Confirm in-scope and out-of-scope boundaries.
- Confirm target environments (local, staging, production).

## 2) Contact Surface Inventory

- User entry points: UI screens, API endpoints, webhooks, scheduled jobs, internal service triggers.
- Orchestration layer: controllers, handlers, services, queues, feature flags, rollout logic.
- Storage and state: database tables, migrations, caches, blob/object storage.
- External integrations: third-party APIs, notification providers, payment/auth providers.
- Telemetry and operations: logs, metrics, traces, alerts, escalation paths, runbooks, ownership metadata.
- Delivery path: CI checks, deployment and rollback flow, environment config, and secrets handling.

## 3) Multi-Lens Risk Scan

For each touchpoint, score:

- Correctness: edge-case handling, input validation, concurrency, idempotency.
- Data integrity: migration safety, consistency invariants, backfill and recovery behavior.
- Security and privacy: authentication/authorization coverage, secret handling, data exposure risk.
- Reliability: retries, timeout policy, circuit breaking, fallback behavior, partial failures.
- Performance: hot paths, query and I/O efficiency, payload size, network usage.
- Cost: over-compute, over-fetch, high-frequency expensive operations, unbounded growth.
- Test coverage: unit, integration, end-to-end, failure-path, regression coverage.
- Operability: debuggability from logs, actionable alerts, trace continuity.
- Maintainability: coupling, duplication, ownership clarity, refactor friction.
- Product and UX: confusing paths, failure-state recovery UX, friction in critical journeys.

## 4) Scoring Rubric

Use this simple scoring model:

- Impact: 4 = system-wide outage/data loss/security breach, 3 = major user/business impact, 2 = moderate degradation, 1 = minor annoyance.
- Likelihood: 4 = already happening or very probable, 3 = plausible with normal usage, 2 = uncommon but realistic, 1 = rare edge.
- Confidence: 4 = reproduced or strongly evidenced, 3 = high confidence from code and context, 2 = plausible inference, 1 = weak signal.

Priority score = Impact x Likelihood.
Use Confidence to label certainty, not severity.

## 5) Evidence Standard

Each finding must include:

- Exact file reference or runtime artifact.
- Reproduction steps or reasoned failure path.
- Scope of effect (who/what is impacted).
- Recommended fix with expected impact.

## 6) Improvement and Innovation Prompts

Use these prompts to push beyond basic bug finding:

- Which repeated manual steps can be automated safely?
- Which boundaries can be simplified to reduce coupling?
- Which expensive operations can be cached, batched, or deferred?
- Which test gaps allow high-risk regressions?
- Which metrics are missing for faster incident triage?
- Which product frictions can be converted into clearer flows?
- Which one architectural change would remove multiple classes of issues?

## 7) Report Completion Gate

Mark the audit complete only when all are true:

- End-to-end contact map is documented.
- Findings are prioritized with evidence and fixes.
- At least one optimization and one innovation are proposed.
- Validation status is explicit (what ran, what did not, and why).
- Next three actions are specific and executable.
