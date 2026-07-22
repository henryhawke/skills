---
name: streamline
description: Diagnose, redesign, implement, and validate end-to-end product workflows across web, mobile, desktop, admin, dashboard, settings, forms, onboarding, operations, and multi-role services. Use when asked to simplify a workflow, reduce unnecessary effort, improve findability, consolidate scattered actions, remove duplicate work, clarify navigation or state, improve recovery, accelerate expert work, or make an agent-built interface intentional, accessible, resilient, and measurably easier to complete correctly.
---

# Streamline

Improve **verified task completion per unit of total human effort**. Optimize the complete task episode—from trigger to confirmed outcome and later re-entry—not an isolated screen, component, route, or click count.

Total effort includes finding, understanding, deciding, remembering, entering, navigating, waiting, coordinating, recovering, and verifying. Preserve steps that earn their place through comprehension, consent, safety, security, privacy, compliance, auditability, or reliable recovery.

## Reference map

Use the smallest set of references needed for the task:

- Read [references/workflow-lab.md](references/workflow-lab.md) for evidence labels, scenario templates, workflow maps, ledgers, scorecards, and study plans.
- Read [references/pattern-catalog.md](references/pattern-catalog.md) before choosing between competing interaction patterns or automating work.
- Read [references/implementation-playbook.md](references/implementation-playbook.md) before changing a repository, state model, API boundary, permission path, or production workflow.
- Read [references/ux-streamlining-research.md](references/ux-streamlining-research.md) when a recommendation needs an external basis, a standard, or a way to adjudicate conflicting heuristics.

## Choose the operating mode

| Mode | Use when | Permission boundary | Required result |
|---|---|---|---|
| **Audit** | Review, diagnose, or recommend | Inspect only; do not modify product artifacts | Evidence boundary, current episode, ranked friction, lean-path hypotheses, validation plan |
| **Design** | Define a future flow, information architecture, interaction model, content model, wireframe, or specification | Create design artifacts; do not implement unless authorized | Future episode, state/branch specification, retained safeguards, acceptance criteria |
| **Implement** | Change or build the product | Modify only the authorized scope | Smallest coherent vertical change, tests, instrumentation where appropriate, and actual proof run |
| **Measure** | Establish a baseline, compare a candidate, or prove an outcome | Instrument or study only within authorization | Fixed task definition, metrics, population/context, results, uncertainty, and decision |

Combine modes only when the request authorizes the combination. Never silently turn an audit into an implementation or a design hypothesis into a proven improvement.

## Non-negotiable outcome contract

A candidate is not streamlined merely because it has fewer controls, pages, fields, or clicks. It must improve—or credibly preserve while reducing effort—the outcomes that matter for the named task.

Use these priorities in order:

1. **Correct and safe completion** — the intended outcome actually occurs, without critical error or false completion.
2. **Comprehension and control** — the user understands the next action, consequence, status, and available recovery.
3. **Accessibility and inclusion** — the task remains operable with relevant input methods, assistive technology, zoom/reflow, and constrained contexts.
4. **Efficiency** — unnecessary decisions, recall, entry, navigation, waits, handoffs, and rework are reduced.
5. **Confidence and craft** — hierarchy, language, density, and feedback make the product feel coherent without masking risk or state.
6. **Operational viability** — permissions, auditability, data integrity, support, performance, and business guardrails remain intact.

A regression in a higher priority cannot be justified by a gain in a lower priority.

## Evidence discipline

Label material claims with one or more of these evidence classes:

- **INSTRUMENTED** — analytics, production traces, controlled experiments, support data, or measured performance with a defined denominator.
- **OBSERVED** — reproducible runtime inspection, repository-backed behavior, accessibility inspection, or direct task observation.
- **REPORTED** — a user, stakeholder, support, or domain-expert claim not independently verified.
- **EXTERNAL** — a standard, published study, design system, or industry reference that supports a general principle.
- **HYPOTHESIS** — a reasoned prediction, heuristic diagnosis, synthetic scenario, or estimated effect.
- **UNKNOWN** — information not available or not yet verified.

Rules:

- Product-specific behavior requires product-specific evidence. External research can justify a design principle; it cannot prove what this product's users do.
- Synthetic scenarios are design probes, not user research. Label them **Synthetic scenario** and tag uncertain details.
- Do not invent analytics, frequencies, timings, user quotes, business rules, personas, or usability findings.
- Use `unknown` rather than false precision. A directional target is acceptable when the method for establishing a baseline is explicit.
- Separate fact, interpretation, recommendation, and predicted effect.

Proceed with reversible, labeled assumptions when missing information does not materially change the decision. Ask only when the answer changes the intended outcome, authorization, source of truth, product policy, material risk, or an irreversible data/permission action.

# Streamlining protocol

## 0. Frame the task episode

Define the unit of work before evaluating the interface.

Record:

- actor, role, permissions, proficiency, frequency, device/input, environment, and constraints;
- trigger and entry points;
- desired user outcome and observable completion state;
- start and end boundaries, including offline work and human handoffs;
- primary object or case being acted on;
- known, missing, stale, dirty, or derived data;
- consequence and reversibility of error;
- interruption, recovery, and re-entry expectations;
- business or operational guardrails that must not regress.

Use a **task episode**, not “the page,” as the optimization boundary:

`trigger -> enter -> orient -> decide -> act -> system transition -> verify -> recover/handoff if needed -> done -> re-enter`

When several jobs share a surface, choose the highest-value episode first. Do not collapse distinct jobs into one vague “manage” workflow.

## 1. Inspect the real system end to end

Trace the current episode through every available layer:

- entry links, routes, navigation, search, notifications, and deep links;
- visible hierarchy, labels, controls, defaults, forms, tables, dialogs, and settings;
- loading, empty, partial, stale, validation, permission, error, retry, success, and interrupted states;
- state ownership, persistence, API or service calls, side effects, asynchronous work, and source of truth;
- roles, permissions, approval boundaries, handoffs, and audit records;
- design-system components, content conventions, localization, responsive behavior, and accessibility semantics;
- analytics, support signals, performance data, tests, feature flags, release controls, and monitoring.

Follow the vertical path from entry to durable outcome. Do not infer a workflow from one component or mistake repository structure for the user's mental model.

If no runnable product or reliable data exists, create a clearly labeled hypothesis baseline and state what runtime, analytics, research, or policy evidence remains unavailable.

## 2. Build the current mental movie

Write concrete present-tense stories so the task can be pictured in use. Cover the dominant path plus only the variants capable of changing the design.

Select from:

- first-time or infrequent use;
- frequent expert or high-volume use;
- interruption and later resumption;
- validation error, partial failure, stale state, or degraded response;
- permission boundary or cross-role handoff;
- keyboard, assistive-technology, zoomed, touch, or small-viewport use;
- high-consequence, destructive, financial, publication, consent, or security action.

For every consequential step, run a cognitive walkthrough:

1. Will this actor pursue the correct sub-goal?
2. Will they notice the correct action?
3. Will the label and surrounding context predict the result?
4. Will the system make the result, status, and next step understandable?
5. Can they detect and recover from a mistake without losing valid work?

Treat confident but incorrect completion as failure.

## 3. Establish the baseline

Define completion before selecting metrics. Keep the task, population, environment, data complexity, and denominator stable across comparisons.

Use a small outcome-focused set:

- unassisted verified task success;
- critical-error-free and first-attempt success;
- false completion;
- median plus a tail completion time among successful attempts;
- time to the first correct action;
- error incidence, recovery success, recovery time, and lost work;
- abandonment, re-entry success, and support escalation;
- redundant entries, backtracks, context switches, waits, and handoffs;
- keyboard and relevant assistive-technology completion;
- post-task ease or confidence, paired with observed success;
- interaction-critical responsiveness and operation latency;
- task-specific business or operational guardrails.

Counts and click paths are diagnostic evidence, not the success definition. Never manufacture a numeric baseline.

## 4. Build the friction and value ledger

For each meaningful user or system step, classify its effort and its current value.

### Effort types

- **Find** — locating the correct destination, object, or action.
- **Understand** — interpreting labels, state, requirements, or consequences.
- **Decide** — making a choice the system could avoid, delay, constrain, or support.
- **Remember** — carrying facts, identifiers, prior state, or instructions across steps.
- **Enter** — typing, selecting, formatting, or re-entering data.
- **Navigate** — changing page, layer, mode, device, or tool.
- **Wait** — latency, queueing, uncertainty, or polling.
- **Coordinate** — ownership, approval, handoff, or communication overhead.
- **Recover** — correcting errors, retrying, recreating lost work, or escalating.
- **Verify** — checking whether the intended durable outcome actually occurred.
- **Access** — barriers caused by input, semantics, focus, target size, reflow, motion, or assistive technology.

### Value classes

A step earns its place only if it provides one or more of:

- **Outcome** — directly advances the user's result.
- **Comprehension** — enables a sound decision.
- **Protection** — prevents material harm or preserves consent, privacy, security, compliance, or safety.
- **Continuity** — preserves state, ownership, synchronization, recovery, or re-entry.
- **Coordination** — creates a necessary handoff, approval, audit, or shared understanding.
- **None** — duplicate, ornamental, implementation-driven, avoidable, or misplaced work.

`None` makes a step a removal candidate, not an automatic deletion. First check whether a hidden policy, system dependency, or recovery function was omitted from the map.

Inspect especially for generated-product residue:

- navigation that mirrors routes, services, tables, or backend capabilities rather than user outcomes;
- one page, card, or setting for every implementation concept;
- repeated identifiers, summaries, fields, filters, confirmations, or status labels;
- generic dashboards, nested dashboards, nested modals, and dead-end detail pages;
- primary actions buried in overflow menus or distant settings;
- raw identifiers, internal statuses, or technical jargon without a user decision;
- premature choices, decorative containers, verbose helper text, and competing primary actions;
- context loss after validation, save, refresh, back navigation, permission failure, or interruption;
- status that is hidden, delayed, contradictory, or impossible to verify;
- workflows that require users to reconcile multiple sources of truth.

## 5. Classify risk before removing friction

Use the highest applicable risk tier:

| Tier | Typical properties | Streamlining posture |
|---|---|---|
| **Low** | Local, reversible, low-cost, no external side effect | Prefer direct action, immediate feedback, and undo |
| **Moderate** | Recoverable but cross-record, cross-user, or operationally costly | Add constraints, previews where useful, clear status, and reliable recovery |
| **High** | Money, deletion, publication, permissions, consent, security, legal effect, or significant external side effect | Preserve explicit review, consequence clarity, authorization, auditability, idempotency, and recovery |
| **Critical** | Irreversible, regulated, safety-critical, or broad blast radius | Require domain-specific policy and stronger controls; do not infer authorization from a UX request |

Do not call protective friction waste. Streamline its presentation, data reuse, ordering, and recovery while preserving its control purpose.

## 6. Design the lean path

Apply this intervention order. Prefer the earliest effective treatment:

1. **Eliminate** work that has no user or system value.
2. **Prevent** the condition that creates the work or error.
3. **Reuse** known data, retained state, or existing context.
4. **Derive** safe values the system already knows; show the derivation and allow correction when needed.
5. **Relocate** actions and information to the point of decision.
6. **Combine** related work around the user's object or outcome.
7. **Sequence** complexity in the order it becomes relevant.
8. **Clarify** labels, hierarchy, status, consequences, and information scent.
9. **Accelerate** repetition with bulk actions, saved views, templates, recents, shortcuts, or deep links.
10. **Automate** only when authority, confidence, observability, exception handling, and recovery are adequate.
11. **Polish** density, spacing, typography, motion, and visual hierarchy after structural friction is addressed.

Design rules:

- Organize around user-recognizable objects, outcomes, and task order—not internal architecture.
- Keep the likely next action prominent while making alternatives discoverable.
- Put local controls at the point of use; keep truly global settings in one stable, searchable home.
- Prefer recognition over recall: retain prior choices, labels, requirements, ownership, and state.
- Preserve valid input after errors and navigation.
- Use progressive disclosure for advanced or infrequent choices, with a label that predicts what is hidden.
- Use defaults only when safe and visible. Never preselect factual claims, eligibility, consent, or answers requiring deliberate user assertion.
- Prefer constraints, previews, reversible drafts, or undo over habitual confirmations when risk permits.
- Keep ownership, progress, system status, exceptions, and completion evidence near the action that caused them.
- Make equivalent outcomes available by keyboard and relevant assistive technology; do not require a precise pointer gesture when an alternative is feasible.
- Do not create a giant dashboard, universal action, or abstraction unless it removes a real boundary without erasing distinct decisions or ownership.

Apply the deletion test to every new surface or abstraction: removing it must erase a distinct user decision, durable state boundary, safety control, or reusable policy. Otherwise, do not add it.

## 7. Compare, prioritize, and decide

Show the current and proposed episodes side by side. For every change, complete this chain:

`evidence -> friction -> root cause -> treatment -> affected scenario -> predicted metric -> no-regression guardrail -> validation -> rollback or revision trigger`

Rank using raw factors:

- workflow reach or frequency;
- outcome impact and error severity;
- evidence confidence;
- accessibility impact;
- implementation and migration effort;
- reversibility, dependencies, and blast radius;
- policy or data uncertainty.

A numeric score may sort candidates only if its formula and raw inputs are shown. It may never override a safety, accessibility, consent, security, privacy, or data-integrity veto.

Prefer the smallest coherent set of changes that improves the complete episode. Avoid scattered cosmetic patches that leave the structural cause intact.

## 8. Implement only when authorized

Follow [references/implementation-playbook.md](references/implementation-playbook.md).

At minimum:

- trace and preserve the source of truth, state model, permissions, side effects, deep links, contracts, audit trail, and adjacent capabilities;
- reuse established components, tokens, domain language, content patterns, and localization mechanisms unless they are the diagnosed cause;
- cover idle, editing, validating, submitting, acknowledged, queued/running, succeeded, partially succeeded, failed, stale, cancelled, retried, and interrupted states as applicable;
- prevent duplicate or unsafe actions; make retries and cancellations truthful;
- preserve valid work and focus through validation and recovery;
- add focused workflow tests and outcome-boundary instrumentation where justified;
- avoid broad rewrites, unrelated cleanup, dependency churn, or weakened quality gates;
- use a reversible rollout and explicit rollback path when the change has material uncertainty or blast radius.

A compile, unit test, screenshot, or local happy-path pass does not prove improved usability or deployed correctness.

## 9. Validate the complete task

Replay the selected scenario portfolio against the candidate, not just the edited screen. Validate relevant combinations of:

- novice and expert use;
- viewport, input method, zoom/reflow, keyboard, and representative assistive technology;
- empty, partial, stale, high-volume, and malformed data;
- permissions, ownership, and cross-role handoffs;
- slow acknowledgment, long-running work, partial failure, retry, duplicate submit, and interruption;
- destructive, financial, publication, consent, or security consequences;
- deep-link entry, browser/app back behavior, refresh, and re-entry.

Use automated checks for contracts and regressions. Use task-level observation, production measurement, or controlled study evidence for claims about human usability.

When comparing before and after, report:

- exact task and verified success condition;
- participants or traffic population and relevant segments;
- environment, device/input, data complexity, and version;
- metric definitions and denominators;
- sample size or event count;
- uncertainty, exclusions, and known bias;
- guardrail outcomes;
- stop, revise, or rollback criteria.

Call an unmeasured candidate a **stronger hypothesis**, not “intuitive,” “simpler,” or “better.”

# Context overlays

## Public, unfamiliar, or infrequent tasks

Bias toward focus, plain task language, explicit requirements, one dominant next action, visible progress, local error recovery, and review before consequential submission. Fewer concepts per step can be more efficient than fewer screens.

## Frequent expert and operational tasks

Bias toward comparison, stable density, strong scanning structure, saved views, bulk operations, templates, keyboard acceleration, interruption recovery, and visible system/ownership state. Do not force expert work through repetitive novice scaffolding.

## AI- or agent-assisted workflows

Treat model output and autonomous action as additional system states and risk boundaries.

- Set accurate expectations about capability, limits, data use, and authority before reliance.
- Distinguish suggestion, draft, planned action, executing action, and completed effect.
- Show the relevant basis, uncertainty, or provenance at the decision point without dumping raw internals.
- Let users inspect, correct, reject, override, stop, and recover.
- Require explicit approval at consequential boundaries unless a bounded policy explicitly authorizes automation.
- Make partial success, skipped items, tool failure, stale inputs, and unavailable actions visible.
- Preserve durable history for consequential actions and make responsibility clear.
- Evaluate calibration, false completion, automation bias, correction effort, and exception handling—not only acceptance rate or speed.

## High-consequence workflows

For money, permissions, deletion, publication, legal/consent, security, regulated, or safety-sensitive actions:

- define the critical-error taxonomy before optimizing;
- verify authorization and source-of-truth ownership;
- show exact affected objects, scope, irreversible effects, and exceptions;
- use prevention, constraints, idempotency, review, explicit action labels, and audit records as appropriate;
- design rollback, compensation, escalation, or safe failure before removing steps;
- require domain review where policy—not interface design—determines the control.

# Output contracts

Scale detail to the task. A narrow change may use a compact before/after; a systemic workflow should use the full artifacts.

## Audit output

1. **Outcome and scope** — task episode, actors, completion state, risk, inspected evidence, and unknowns.
2. **Current mental movie** — labeled synthetic scenarios and path maps.
3. **Baseline** — available measures, observable counts, and missing evidence.
4. **Friction ledger** — ranked root causes, current value, severity, and evidence class.
5. **Lean-path hypotheses** — before/after path, retained safeguards, and why each change earns its place.
6. **Scorecard and validation** — expected metric direction, guardrails, proof method, and stop/revert conditions.
7. **Risks and decisions needed** — policy, data, permission, migration, or research questions.

## Design output

Include the audit essentials plus:

- future episode and information architecture;
- screen/state inventory and transition model;
- primary, alternate, error, empty, loading, stale, permission, interrupted, and re-entry behavior;
- content and action hierarchy;
- accessibility and responsive requirements;
- analytics and acceptance criteria;
- open policy decisions and no-regression contract.

## Implement output

Include:

- authorized scope and surfaces changed;
- current-to-future episode delta;
- source-of-truth, permission, contract, migration, and side-effect notes;
- implementation summary by workflow behavior, not file count alone;
- tests, accessibility checks, performance checks, and task replay actually run;
- instrumentation, rollout, monitoring, and rollback when applicable;
- remaining risks, unknowns, and proof boundary.

## Measure output

Include:

- fixed task definition and verified completion state;
- baseline/candidate, population, segments, environment, and data complexity;
- primary metric, guardrails, event or study definitions, and denominator;
- results with counts, distributions, uncertainty, and exclusions;
- interpretation separated from fact;
- decision: retain, revise, roll back, or collect more evidence.

# Guardrails

- Do not optimize an isolated screen at the expense of the end-to-end episode.
- Do not equate fewer clicks, fields, pages, controls, or visible elements with better UX.
- Do not hide status, ownership, consequences, exceptions, or recovery to make a surface look clean.
- Do not remove authentication, consent, review, approval, or confirmation without identifying and preserving its risk function.
- Do not automate a decision merely because it is repetitive; verify authority, confidence, reversibility, observability, and exception handling.
- Do not expose internal architecture, raw identifiers, or technical state unless it supports a user decision or operational diagnosis.
- Do not consolidate unrelated jobs into an ambiguous dashboard or universal action.
- Do not optimize only the happy path or only the average user.
- Do not move a hard-to-find function without fixing naming, entry points, search, links, and migration cues.
- Do not replace precise domain language merely to sound friendly; explain it where the decision occurs.
- Do not use an aggregate score to hide a failed minority path, critical error, or accessibility barrier.
- Do not claim research, measurement, or validation that was not performed.

# Final gate

Before responding or shipping, verify:

- the task start, verified end state, actors, context, and risk are explicit;
- every claimed fact has an evidence class and every unknown is visible;
- every removal maps to a real step and preserves any hidden control value;
- every recommendation serves a named scenario and expected outcome;
- current and proposed paths are comparable at the same boundary;
- safety, consent, security, privacy, permissions, accessibility, auditability, and recovery remain intact;
- status and completion are observable, including partial and failed outcomes;
- the proposal reduces total human or operational effort, not merely visible UI;
- implementation stayed within authorization and preserved unrelated capabilities;
- proof claims match the tests, observations, or measurements actually performed;
- an unmeasured redesign is labeled as a hypothesis.
