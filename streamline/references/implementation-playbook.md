# Repo-agnostic implementation playbook

Use this reference only when implementation is authorized. It converts a workflow recommendation into the smallest coherent, reversible product change while preserving contracts, permissions, data integrity, accessibility, observability, and unrelated behavior.

The goal is not to minimize changed files. The goal is to change the full vertical slice required for the named task—and nothing outside it.

## Contents

- [Authorization and scope](#authorization-and-scope)
- [Repository orientation](#repository-orientation)
- [Vertical workflow trace](#vertical-workflow-trace)
- [Change classification](#change-classification)
- [Implementation plan](#implementation-plan)
- [Contract and state preservation](#contract-and-state-preservation)
- [Side-effect and concurrency safety](#side-effect-and-concurrency-safety)
- [Interaction-state implementation](#interaction-state-implementation)
- [Accessibility gates](#accessibility-gates)
- [Performance and responsiveness](#performance-and-responsiveness)
- [Content, localization, and design-system fit](#content-localization-and-design-system-fit)
- [Instrumentation](#instrumentation)
- [Test strategy](#test-strategy)
- [Release, rollout, and rollback](#release-rollout-and-rollback)
- [Proof and reporting](#proof-and-reporting)
- [Definition of done](#definition-of-done)

# Authorization and scope

Before editing, record:

```markdown
## Authorized implementation scope

**Requested outcome:**
**Task episode:**
**Actors/roles:**
**Surfaces allowed to change:**
**Behavior allowed to change:**
**Data/API/permission changes authorized:**
**Out of scope:**
**Required compatibility:**
**Risk tier:**
**Release constraints:**
**Unknowns capable of changing policy or safety:**
```

Rules:

- Do not cross from audit/design into implementation without authorization.
- Do not broaden a UX change into an architectural rewrite, dependency migration, design-system replacement, or cleanup campaign unless required for the episode and authorized.
- Preserve unrelated work, local modifications, generated artifacts, and conventions.
- Ask only when the missing answer changes authorization, policy, source of truth, material risk, or an irreversible data/permission effect. Otherwise, use a reversible labeled assumption.

# Repository orientation

Discover how this repository works before assuming a framework, command, or ownership boundary.

## Read first

Inspect the available equivalents of:

- root and package-level README files;
- contribution and architecture guidance;
- dependency/build manifests and lockfiles;
- task runners and repository-native scripts;
- CI definitions and quality gates;
- application entry points and route/navigation definitions;
- component library, design tokens, themes, and content conventions;
- API/schema/client generation sources;
- state management and persistence layers;
- authorization/permission policy;
- analytics/telemetry wrappers and event taxonomy;
- localization/message catalogs;
- unit, component, contract, integration, end-to-end, accessibility, and performance tests;
- feature-flag, deployment, migration, and rollback mechanisms;
- monitoring, alerting, and operational runbooks.

Use repository-native commands discovered in these sources. Do not invent build, test, formatting, or generation commands from framework assumptions.

## Repository map

Create a compact map before editing:

| Concern | Owning path/module | Source of truth | Generated? | Relevant tests | Notes |
|---|---|---|---|---|---|
| Entry/navigation | | | | | |
| Workflow surface | | | | | |
| Shared components/tokens | | | | | |
| State/persistence | | | | | |
| API/service boundary | | | | | |
| Permission policy | | | | | |
| Analytics | | | | | |
| Localization/content | | | | | |
| Feature flags/release | | | | | |
| Monitoring/support | | | | | |

## Generated-source rule

When a file is generated:

1. identify the owning source and generator;
2. edit the source, not the output;
3. run the owning generator;
4. verify the generated diff is limited and deterministic;
5. keep source and generated artifacts in sync.

Never hand-edit generated output to make a test pass.

# Vertical workflow trace

Trace the current task from trigger to durable outcome. Follow behavior, not file names alone.

```text
entry/trigger
-> route/navigation resolution
-> surface/component
-> local/shared state
-> validation
-> client/service request
-> authorization
-> domain operation
-> persistence/external side effect
-> asynchronous work
-> response/event/update
-> user-visible status
-> durable verification
-> analytics/audit
-> recovery/re-entry
```

## Trace table

| Stage | Owning code/path | Input | State transition | Side effect | Permission | User feedback | Failure/retry | Test/telemetry |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## Questions the trace must answer

- What is the authoritative object and source of truth?
- Which layer decides whether the actor may act?
- Which layer validates business rules?
- Which state is local, cached, derived, optimistic, queued, or durable?
- What external or cross-user side effects occur?
- Can a request be repeated safely?
- How are stale writes and concurrent edits handled?
- How does the interface learn that long-running work completed?
- What constitutes partial success?
- What is recorded for audit/support?
- Which deep links and return paths must keep working?
- What happens after refresh, browser/app back, session loss, or device change?

Do not move a control or combine screens before understanding the state and permission boundaries it crosses.

# Change classification

Classify every proposed change. Higher classes require wider validation and often staged release.

| Class | Examples | Typical risk | Minimum validation |
|---|---|---|---|
| **Presentation** | Hierarchy, spacing, copy, visual grouping using existing behavior | Misinterpretation, accessibility regression | Component/task inspection, responsive and accessibility checks |
| **Local interaction** | Disclosure, inline edit, filter persistence, focus/recovery behavior | State loss, keyboard/error regression | Component/integration tests plus scenario replay |
| **Navigation/route** | Deep link, object workspace, moved setting, return path | Broken links, history/context loss, discoverability | Route/deep-link tests, migration cues, task replay |
| **Client/shared state** | Draft retention, optimistic state, cross-surface context | Stale data, silent overwrite, inconsistent UI | State-transition and interruption tests |
| **API/contract** | Request/response, validation, new operation state | Compatibility, partial deployment, client breakage | Contract tests, backward/forward compatibility, staged rollout |
| **Data/schema** | New field, migration, source-of-truth change | Data loss, mixed-version behavior | Migration rehearsal, expand/contract plan, rollback/repair |
| **Permission/policy** | Eligibility, approval, ownership, scope | Unauthorized action or blocked legitimate work | Domain/security review, negative authorization tests, audit verification |
| **External side effect** | Money, email, publication, deletion, provisioning | Duplicate or irreversible effect | Idempotency, preview/review, fault tests, audit, staged release |
| **Automation/AI** | Tool execution, recommendations, bounded autonomous action | Wrong action, overreliance, hidden partial failure | Quality/safety evaluation, authority gates, stop/override, monitored rollout |

A “small UI change” that alters state, permission, or side-effect semantics belongs to the higher class.

# Implementation plan

Use one plan row per coherent behavior change, not per file.

| Change | Episode step | Root cause | Owning layers | Contract/state impact | Safeguards | Tests | Instrumentation | Rollout/rollback |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## Slice design

A coherent vertical slice should include, as applicable:

- entry point and route;
- visible control and content;
- state ownership and persistence;
- validation and permissions;
- service/domain operation;
- async and failure behavior;
- success/partial/failure feedback;
- accessibility semantics and focus;
- analytics/audit;
- tests;
- migration and release control.

Do not ship a new happy path while leaving the old error, permission, or verification path contradictory.

## Change order

Prefer this implementation sequence:

1. Add missing observability and characterize current behavior when needed.
2. Establish or preserve a stable domain/state contract.
3. Add compatibility paths for route/API/data changes.
4. Implement prevention, retained context, and recovery foundations.
5. Implement the lean interaction and all relevant states.
6. Add focused tests and instrumentation.
7. Validate scenario matrix locally/in an appropriate environment.
8. Release behind a reversible control when uncertainty or blast radius warrants it.
9. Monitor primary and guardrail outcomes.
10. Remove obsolete compatibility paths and flags only after evidence and rollback windows permit.

# Contract and state preservation

## Route and deep-link contract

For moved or consolidated workflows:

- preserve existing deep links where practical through redirect or compatibility routing;
- carry object identity and intent, never authorization;
- re-check current permissions and object state at destination;
- preserve list/filter return context without making deep links depend on prior history;
- provide a useful expired/missing/unauthorized state;
- update internal links, notifications, search results, documentation, and tests;
- define how browser/app back and refresh behave;
- avoid redirect loops and hidden context loss.

## API and message contract

Before changing a contract, record:

```markdown
**Consumers:**
**Current request/response or event:**
**Current error semantics:**
**Current idempotency/retry behavior:**
**Candidate change:**
**Backward-compatible path:**
**Forward-compatible path:**
**Mixed-version behavior:**
**Deprecation/removal plan:**
**Contract tests:**
```

Prefer additive, tolerant changes before removal. Do not couple a client and server deployment so tightly that either order creates a broken workflow unless deployment guarantees make that safe and explicit.

## Data/source-of-truth contract

- Identify the authoritative field/object before adding a duplicate UI copy.
- Avoid multiple writable sources for the same setting or status.
- Define derived values and their refresh/invalidation rules.
- Preserve provenance when a value comes from another system or AI output.
- Specify null, unknown, partial, stale, and conflicting states; do not collapse them into false certainty.
- For migrations, define backfill, validation, mixed-version reads/writes, repair, and rollback/roll-forward.
- Never overwrite newer durable state with an older client snapshot without an explicit conflict policy.

## Permission contract

Permissions must be enforced in the authoritative layer, not only through hidden/disabled UI.

Validate:

- allowed role and object state;
- denied role and object state;
- cross-tenant/workspace/object access boundaries;
- stale permission after page load;
- bulk action with mixed eligibility;
- request-access or handoff path;
- audit identity and scope;
- error response that is useful without leaking sensitive policy or data.

A redesigned entry point must not become a bypass.

# Side-effect and concurrency safety

## Idempotency

Use idempotent semantics or a deduplication mechanism when retries, double clicks, reconnects, queue redelivery, or automation can repeat an action.

Define:

- idempotency/deduplication key scope;
- retention window;
- response for repeated identical requests;
- response for reused key with different payload;
- behavior after partial completion;
- audit and user-visible status;
- client retry rules.

Disabling a button is not sufficient protection against network or process-level duplication.

## Duplicate submit

The interface should:

1. acknowledge the first action;
2. prevent accidental repeat while state is known;
3. show whether the operation was accepted, queued, running, or completed;
4. allow retry only when safe or after status reconciliation;
5. recover after refresh or reconnect without creating another operation.

## Retry behavior

Classify failures:

| Failure | Typical treatment |
|---|---|
| Client validation | Correct locally; do not send |
| Authorization/policy | Explain and route to access/handoff; blind retry is wrong |
| Conflict/stale state | Refresh/merge/review; blind retry may overwrite |
| Rate limit/transient dependency | Controlled retry with backoff/jitter where appropriate; expose state |
| Timeout with unknown server result | Reconcile operation status before retry |
| Permanent domain rejection | Explain correction; repeated retry is wrong |
| Partial batch failure | Retry eligible failed items only; preserve successful results |

Do not expose a generic `Retry` control unless the operation is safe to repeat or the system first reconciles its status.

## Concurrency and stale data

Choose and document a policy:

- optimistic concurrency/version check;
- last-write-wins only for low-risk data where acceptable;
- field-level merge;
- lock/lease for bounded operations;
- append-only event or command model;
- review/diff before overwrite.

The UI must make a conflict understandable and preserve the user's work. Avoid silent discard or silent overwrite.

## Optimistic UI

Use only when:

- the action is low consequence and likely to succeed;
- pending state is distinguishable when needed;
- rollback is truthful and understandable;
- concurrent updates are handled;
- duplicate side effects are prevented;
- refresh/re-entry can reconcile the real state.

For high-consequence work, prefer acknowledged/queued/running/durable states over pretending completion.

## Cancellation and undo

Distinguish:

- **cancel before start** — queued work never begins;
- **cancel in progress** — system can stop safely at a defined boundary;
- **undo** — original effect is reversed;
- **compensate** — a new effect offsets the original but history remains;
- **request cancellation** — request is accepted but completion is not immediate.

Label the actual behavior. Never promise cancellation or undo that cannot be honored.

## Partial failure

Represent each affected item's result or a trustworthy aggregate with a route to item detail.

Required implementation properties:

- stable operation identity;
- explicit committed versus uncommitted effects;
- safe retry of eligible failures;
- no replay of successful side effects;
- retained preview/scope for comparison;
- durable history and support trace;
- accessible summary and item-level feedback.

# Interaction-state implementation

Implement the states that the domain can actually enter.

## Base state inventory

| State | Required UI behavior |
|---|---|
| Idle/ready | Correct object, permissions, and primary action visible |
| Editing/dirty | Changed values identifiable; save/cancel/discard behavior defined |
| Validating | Do not erase input; avoid blocking unrelated inspection |
| Submitting | Acknowledge action; prevent accidental duplicate; retain context |
| Accepted/queued | Name operation, scope, and how to leave/return |
| Running | Progress or meaningful status; safe cancel if supported |
| Succeeded | Show durable result, affected object/state, next action, and audit/history route |
| Partially succeeded | Separate success/failure, exceptions, and safe retry |
| Failed | Preserve valid work; explain cause/next step; reconcile unknown result |
| Empty | Distinguish first use, no matches, no permission, loading, or failure |
| Partial data | Identify what is missing and whether action is allowed |
| Stale/conflicted | Preserve edits; show change/diff and resolution options |
| Interrupted/resumed | Restore object, draft, status, and return path |
| Read-only/denied | Explain state, owner, and access/handoff route when appropriate |
| Cancelled/undone/compensated | State exactly what was stopped or reversed and what remains |

## Feedback placement

- Keep local feedback beside the action or object that caused it.
- Use a global notification only for cross-surface or background completion.
- Do not rely on transient toast alone for consequential results or errors.
- Keep durable status in the object/history.
- Make status available programmatically without unnecessary focus movement.
- Use specific operation and result language.

## Focus behavior

Define focus for:

- route/page entry;
- opening and closing dialogs/drawers;
- inline edit start/save/cancel;
- validation error and error summary;
- added/removed/reordered content;
- async completion and status messages;
- destructive confirmation;
- return from detail to list;
- failed permission/access request.

Do not move focus simply to announce success when a non-disruptive status message is sufficient.

# Accessibility gates

Use the applicable accessibility standard and the product's established conformance target. WCAG 2.2 is the baseline for web content; platform and organizational requirements may add more.

## Semantic and keyboard gate

Verify:

- native elements or equivalent semantics for controls;
- accurate accessible name, role, value, state, and relationships;
- logical reading and focus order;
- full keyboard operation without traps;
- visible focus that is not obscured;
- focus return after transient surfaces;
- no essential hover-only or drag-only action;
- shortcut behavior does not conflict with input or assistive technology and has a discoverable equivalent.

## Visual and reflow gate

Verify:

- text and non-text contrast meet the applicable requirement;
- information is not conveyed by color, position, shape, or motion alone;
- zoom/reflow preserves all content and functions;
- text resizing does not clip or overlap essential information;
- targets meet applicable minimum size/spacing or a defined exception;
- sticky/fixed elements do not obscure focus or content;
- reduced-motion preference is respected;
- high-volume tables have a usable small-viewport strategy.

## Forms and error gate

Verify:

- persistent labels and programmatic instructions;
- autocomplete/input purpose where applicable;
- required/optional and formats conveyed in text;
- field errors associated with the field;
- useful error summary for multiple errors;
- valid values preserved;
- redundant entry reduced within the same process unless an exception applies;
- review/reversal/checking for consequential submissions as required;
- no timeout or session behavior that causes unavoidable loss without warning/extension where required.

## Dynamic status gate

Verify:

- loading, progress, result, and error states are programmatically exposed;
- updates do not steal focus unnecessarily;
- busy, expanded, selected, pressed, invalid, current, and disabled states are accurate;
- partial success is perceivable and navigable;
- async operations remain understandable after leaving and returning.

## Authentication gate

Where authentication changes are in scope:

- support password managers and autofill as allowed by policy;
- do not unnecessarily block paste;
- avoid cognitive-function tests without an accessible alternative where requirements apply;
- provide usable recovery and clear session-expiration behavior;
- do not weaken security policy in the name of streamlining.

## Manual task gate

Automated scanning is necessary but insufficient. Replay the critical episode using:

- keyboard only;
- representative screen reader or other relevant assistive technology;
- zoom/reflow or small viewport;
- touch where relevant;
- reduced motion where relevant;
- error, permission, slow, partial, and interrupted states.

Record the equivalent outcome and any extra effort or blocked route.

# Performance and responsiveness

Measure the interaction the user experiences, not only build output or average server latency.

## Interaction budgets

For interaction-critical paths, define:

- input acknowledgment target;
- client rendering/update target;
- service acceptance target;
- durable operation completion expectation;
- progress threshold and update cadence;
- timeout and reconciliation behavior;
- payload, query, and rendering constraints;
- field performance guardrails by device/context.

For web products, use field Core Web Vitals where applicable and relevant to the workflow. Current widely used “good” thresholds at the 75th percentile are LCP no more than 2.5 seconds, INP no more than 200 milliseconds, and CLS no more than 0.1; treat them as supporting quality thresholds, not proof of task usability.

## Performance implementation rules

- Do not block initial task orientation on secondary data.
- Reserve layout space to avoid disruptive shifts.
- Defer nonessential work without hiding required status.
- Virtualize or paginate high-volume data without breaking semantics, selection, or position.
- Avoid re-fetch loops and duplicate requests caused by state changes.
- Cache only with explicit freshness/invalidation behavior.
- Make slow dependencies and partial data states truthful.
- Do not use a skeleton that implies unavailable content structure inaccurately.
- Test degraded network/service behavior, not only local speed.

## Operation latency

Separate:

1. interaction-to-acknowledgment;
2. acknowledgment-to-acceptance/queue;
3. queue/run time;
4. completion-to-interface update;
5. completion-to-notification;
6. failure-to-recovery availability.

This separation reveals whether the problem is responsiveness, backend work, polling/event propagation, or feedback.

# Content, localization, and design-system fit

## Reuse before inventing

Prefer existing:

- semantic components;
- tokens and themes;
- spacing/type scales;
- form and error patterns;
- table/list primitives;
- dialog/drawer behavior;
- notification and status patterns;
- localization mechanisms;
- content voice and domain terminology.

Create or change a shared abstraction only when the workflow exposes a reusable policy or state boundary—not merely because two screens look similar.

## Content implementation

- Use action labels that name the result.
- Keep exact domain terms when precision matters; explain them locally.
- Avoid embedding copy in logic when the repository uses catalogs or content models.
- Account for expansion, pluralization, grammar, date/number/time zones, right-to-left layout, and dynamic item counts.
- Do not concatenate fragments that translators cannot reorder safely.
- Keep status, error, and confirmation messages tied to real state, not client guesses.

## Visual change discipline

- Use existing tokens before hard-coded values.
- Preserve responsive and theme behavior.
- Avoid one-off variants that duplicate an existing semantic component.
- Verify hierarchy at realistic content lengths and data volumes.
- Do not lower contrast, hide labels, or reduce target size to create visual minimalism.

# Instrumentation

Use [workflow-lab.md](workflow-lab.md#instrumentation-contract) for the event model. During implementation:

## Instrument stable boundaries

Prefer events for:

- episode start and entry point;
- first meaningful destination/action;
- action attempted and acknowledged;
- accepted/queued/running when relevant;
- success, partial success, failure, cancellation, stale conflict;
- recovery started/completed;
- durable verification;
- support/handoff initiation if part of the episode.

Avoid exhaustive click logging that creates noise, privacy risk, and brittle analytics without a decision use.

## Event implementation checks

- event name and fields follow repository taxonomy;
- completion event is emitted from or reconciled with the durable source of truth;
- retries and duplicate events are deduplicated or analytically interpretable;
- old and new versions can be compared or are explicitly versioned;
- no sensitive/free-text/secret data is captured;
- event failure does not block the product action;
- local/test verification confirms expected event sequence and absence of duplicates.

## Audit versus analytics

Do not treat product analytics as an audit log.

An audit record for consequential actions may require:

- actor identity;
- authority/context;
- affected object/scope;
- prior and resulting state or diff;
- timestamp and operation identity;
- approval or automation policy;
- partial failure/compensation;
- immutable retention and access controls.

Follow domain policy and existing audit architecture.

# Test strategy

Use the lowest-cost test that proves each contract, then replay the complete task.

## Test layers

| Layer | Proves | Does not prove |
|---|---|---|
| Static/type/lint/build | Syntax, types, repository conventions, buildability | Runtime behavior or usability |
| Unit | Pure rules, transformations, formatting, state reducers | Integration and user task completion |
| Component | Component states, events, semantics, local interaction | Service contracts or full navigation |
| Contract/schema | Producer/consumer compatibility and validation | End-to-end side effects |
| Integration | State, service, permissions, persistence, and error wiring | Full deployed environment or human usability |
| End-to-end | Critical route and system interaction in the test environment | Population-level usability or production reliability |
| Accessibility automation | Detectable rule violations | Equivalent task completion with AT |
| Visual/regression | Unexpected rendered differences | Correct hierarchy, comprehension, or accessibility |
| Performance | Defined lab/field latency and budgets | Correct task outcome by itself |
| Manual scenario replay | Complete behavior across meaningful branches | Population frequency or causal improvement |
| Production monitoring/experiment | Real-world outcome and guardrails | Why behavior occurred without qualitative evidence |

## Scenario test matrix

Select relevant cells; do not test only the happy path.

| Dimension | Cases |
|---|---|
| Entry | primary navigation, notification/deep link, search/recent, expired link |
| Data | typical, empty, partial, stale, malformed, high-volume, conflicting |
| Role | allowed, read-only, request access, wrong owner, mixed bulk eligibility |
| Action | first submit, double submit, refresh during submit, retry after unknown result |
| Service | immediate, slow, queued, timeout, dependency failure, partial success |
| Continuity | back, refresh, interruption, resume, session expiry, cross-device where supported |
| Consequence | reversible, destructive, external side effect, compensation/undo |
| Accessibility | keyboard, representative AT, zoom/reflow, touch, reduced motion |
| Layout/content | supported viewports, long labels, localization expansion, large values |
| AI/automation | missing tool/data, low confidence, user correction, stop, partial action, stale source |

## Workflow test naming

Name tests by observable behavior and outcome:

```text
[actor/context] can [verified outcome] when [condition]
[actor/context] cannot [prohibited outcome] when [permission/state]
[operation] preserves [context/data] after [failure/interruption]
[operation] reports [partial/stale state] without [false completion/duplicate effect]
```

Avoid tests that merely reproduce implementation structure.

## Test-data discipline

- Use representative object states and volumes.
- Include boundary and mixed-eligibility cases.
- Keep deterministic fixtures for contract tests.
- Avoid production personal/sensitive data.
- Make time, queue, and failure behavior controllable where practical.
- Verify test data does not accidentally bypass permission or validation logic.

## No weakening rule

Do not:

- skip or delete a failing test without proving it is obsolete;
- weaken assertions to accept contradictory state;
- disable accessibility checks to make a custom component pass;
- expand timeouts instead of diagnosing a race or missing acknowledgment;
- mock away the permission, persistence, or side effect being changed;
- claim a check passed when it was not run or its environment failed.

# Release, rollout, and rollback

Design rollback before release for changes with material uncertainty or blast radius.

## Release strategy chooser

| Strategy | Use when | Requirements |
|---|---|---|
| Direct release | Low-risk, local, easily reversible, well-covered change | Standard deployment rollback and monitoring |
| Feature flag | Behavior must be separated, tested by cohort, or quickly disabled | Owner, default, targeting, telemetry, removal date, safe code paths |
| Canary/staged ramp | Production behavior or scale is uncertain | Small initial exposure, health/guardrail checks, automatic/manual halt, gradual ramp |
| Shadow/dark evaluation | New computation/AI path can be evaluated without affecting users | Privacy-safe comparison, no unintended side effects, clear quality criteria |
| Dual-read/write or expand/contract | Data/API migration across mixed versions | Compatibility, reconciliation, backfill, cutover, cleanup, rollback/roll-forward |
| Prototype/research only | Policy, mental model, or usability is unresolved | No production side effect; explicit evidence goal |

A flag is not a substitute for safe behavior. Both flag states must preserve permissions and data integrity.

## Feature-flag record

```markdown
**Flag:**
**Owner:**
**Purpose/hypothesis:**
**Default:**
**Eligible cohort:**
**Dependencies:**
**Primary metric:**
**Guardrails:**
**Kill/rollback behavior:**
**Expiration/removal date:**
**Cleanup issue/owner:**
```

Use a vendor-neutral abstraction where the repository has one; avoid spreading provider-specific checks through domain logic.

## Canary/ramp plan

```markdown
**Initial exposure:**
**Ramp stages:**
**Required observation per stage:**
**Primary outcome:**
**Technical health:**
**Accessibility/support signals:**
**Business/risk guardrails:**
**Automatic halt conditions:**
**Manual decision owner:**
**Rollback steps:**
**Data repair/compensation:**
```

Compare event dates and versions carefully. Do not attribute pre-existing incidents or instrumentation changes to the candidate.

## Rollback types

- **Code rollback** — prior version restores compatible behavior.
- **Flag disable** — candidate path is bypassed immediately.
- **Configuration rollback** — policy/default returns to prior state.
- **Data roll-forward/repair** — safer than destructive schema rollback when data already changed.
- **Compensating action** — external effects are offset while history remains.
- **Operational pause** — automation/batch processing stops while queued/in-flight state is reconciled.

Document what rollback cannot reverse.

## Release checklist

- compatibility path tested;
- flag/ramp targeting verified;
- instrumentation sequence verified;
- dashboards/alerts or manual checks available;
- support/operations know the changed state and recovery route when relevant;
- migrations/backfills rehearsed;
- rollback/compensation steps executable;
- in-flight operations behavior defined;
- stale clients/sessions behavior defined;
- no unresolved critical accessibility, permission, security, or data-integrity issue.

# Proof and reporting

Report what changed by workflow behavior, not only by file.

## Implementation proof template

```markdown
## Implementation and proof

**Authorized episode:**
**Behavior changed:**
**Behavior preserved:**
**Routes/deep links:**
**State/source of truth:**
**Permissions/audit:**
**Failure/recovery:**
**Accessibility behavior:**
**Instrumentation:**
**Release/rollback:**

### Checks actually run
- [command/check]: [pass/fail/not run and why]

### Scenario replay
- [scenario]: [result and evidence]

### Proof boundary
- [not tested, unavailable environment, unmeasured human outcome]

### Remaining risks/unknowns
- [item, owner or validation method]
```

Rules:

- Distinguish code inspection, automated pass, manual task replay, staging behavior, and production evidence.
- Include failures and unrun checks.
- A local pass does not prove deployed behavior.
- An end-to-end test does not prove improved human usability.
- An unmeasured redesign remains a hypothesis.

# Definition of done

The implementation is done only when all applicable conditions hold:

## Scope and architecture

- [ ] Change stays within the authorized task episode.
- [ ] Source of truth, state ownership, permissions, and side effects are explicit.
- [ ] Existing routes, contracts, or migration paths remain compatible or have an approved transition.
- [ ] Generated artifacts were updated through their owner.
- [ ] Unrelated behavior and local work are preserved.

## Workflow behavior

- [ ] Dominant and consequential scenario paths are implemented.
- [ ] Loading, empty, partial, stale, error, retry, success, and interrupted states are covered as applicable.
- [ ] Valid work and context survive recoverable errors and re-entry.
- [ ] Completion reflects durable state; partial failure is not presented as success.
- [ ] Duplicate, retry, concurrency, cancellation, and compensation behavior is safe and truthful.

## Protection and inclusion

- [ ] Authorization is enforced in the authoritative layer.
- [ ] Consent, review, audit, privacy, security, compliance, and safety controls retain their purpose.
- [ ] Keyboard, focus, semantics, status, error, target, reflow, motion, and relevant AT behavior are validated.
- [ ] No actor or downstream team inherits hidden work without an explicit handoff.

## Quality and evidence

- [ ] Repository-native build/static checks pass or failures are reported.
- [ ] Focused unit/component/contract/integration/end-to-end tests pass as applicable.
- [ ] Critical task scenarios were replayed at the complete episode boundary.
- [ ] Instrumentation uses stable outcome transitions and protects sensitive data.
- [ ] Performance and operation-state feedback meet the defined guardrails.
- [ ] Release, monitoring, and rollback/compensation are ready for the risk tier.
- [ ] Claims in the final report match the proof actually run.
- [ ] Remaining usability improvement is described as a hypothesis until measured with task-level evidence.
