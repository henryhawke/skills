# Workflow lab

Use this reference to construct synthetic scenarios, workflow maps, scorecards, and prioritization artifacts. Keep the labels **synthetic**, **observed**, **instrumented**, and **hypothesis** visible throughout.

## Contents

- [Mental-movie template](#mental-movie-template)
- [Scenario portfolio](#scenario-portfolio)
- [Workflow map](#workflow-map)
- [Metric catalog](#metric-catalog)
- [Diagnostic interaction cost](#diagnostic-interaction-cost)
- [Friction ledger](#friction-ledger)
- [Prioritization](#prioritization)
- [Before-and-after scorecard](#before-and-after-scorecard)
- [Example](#example)

## Mental-movie template

Write in present tense and use concrete product nouns.

> **Synthetic scenario — [role, experience, context]**  
> When [trigger] occurs, [persona] needs to [outcome] before [constraint]. They enter through [entry point] expecting [mental model]. They see [essential state], choose [first decision], and the system [response]. They then [next steps]. If [consequential branch], they [recovery or handoff] without losing [context]. They know the task is complete when [observable state], and they can later return through [re-entry path].

Follow the narrative with a path:

`trigger -> entry -> orient -> decide -> act -> system response -> verify -> recover/handoff if needed -> done -> re-enter`

Do not use a generic persona biography. Include only traits that change the workflow: frequency, expertise, permissions, device, environment, urgency, accessibility needs, or error cost.

## Scenario portfolio

Choose the smallest portfolio that exposes the workflow's meaningful variation:

| Scenario | Exposes |
|---|---|
| Novice or infrequent user | Learnability, naming, information scent, defaults |
| Frequent expert | Repetition, density, shortcuts, batch work, interruption cost |
| Error and recovery | Prevention, feedback, retained state, undo, escalation |
| Permission boundary | Disabled versus hidden actions, ownership, handoff, audit trail |
| Cross-device or resumed task | State continuity, deep links, re-entry, responsive constraints |
| Assistive-technology or keyboard use | Semantics, focus, order, target and feedback accessibility |
| Empty, partial, or stale data | Guidance, trust, refresh, incomplete state handling |
| Slow or degraded system | Acknowledgment, progress, retry safety, duplicate-action prevention |
| Irreversible or high-consequence action | Review, consent, consequence clarity, auditability |

Do not force every scenario into every audit. Include the dominant path and the variants most likely to reverse a design decision.

## Workflow map

Record one row per meaningful user or system step:

| Stage | User intent | Surface/state | User action or decision | System response | Context carried | Branch/failure | Evidence | Cost | Value |
|---|---|---|---|---|---|---|---|---|---|

Classify value as one or more of:

- **Outcome**: directly advances completion.
- **Comprehension**: supplies information needed for a sound choice.
- **Protection**: prevents material harm or preserves consent, privacy, security, or compliance.
- **Continuity**: preserves state, ownership, synchronization, recovery, or an auditable handoff.
- **None**: duplicate, ornamental, implementation-driven, or avoidable work.

A `None` step is a removal candidate, not an automatic deletion. Check whether its value is merely hidden from the current map.

## Metric catalog

Choose a few metrics tied to the outcome. Keep the task definition and denominator fixed across comparisons.

| Metric | Definition | Useful for |
|---|---|---|
| Unassisted task success | Eligible tasks completed correctly without help / eligible tasks started | Primary outcome |
| Critical-error-free success | Correct completions without defined critical errors / tasks started | Safety-sensitive outcomes |
| First-attempt success | Correct completions without a failed attempt / tasks started | Error prevention and clarity |
| False completion | Tasks the user believes are complete but are not / tasks started | Misleading feedback and hidden state |
| Completion time | Median plus a tail percentile from task start to verified completion | Efficiency and outliers |
| Discovery time | Time from entry to the first correct action | Findability and information scent |
| Recoverable error rate | Tasks containing a recoverable error / tasks started | Friction diagnosis |
| Recovery success | Correct recoveries / recoverable-error cases | Feedback, undo, and re-entry |
| Abandonment | Started tasks not completed within the defined window / tasks started | Severe friction |
| Re-entry success | Interrupted tasks completed after return / interrupted tasks | State continuity |
| Input redundancy | Values the system already knows that the user must re-enter per task | Form and handoff waste |
| Navigation reversals | Backtracks or repeated destination visits per task | Misleading structure or labels |
| Context switches | Surface, tool, mode, or person changes required per task | Operational overhead |
| Post-task ease | A consistently worded, immediately administered ease rating | Perceived effort |
| Accessible completion | Success by keyboard and relevant assistive technology with equivalent outcome | Inclusive usability |
| Support escalation | Tasks requiring support or privileged rescue / tasks started | Hidden operational cost |
| Field responsiveness | P75 LCP, INP, and CLS plus operation acknowledgment/completion latency | Perceived and actual web performance |

Segment results when roles, devices, permissions, or task complexity differ materially. Do not average away a failed minority path.

Use counts when sample sizes are small. Use confidence intervals or statistical tests only when the study design supports them. A target such as “reduce median completion time by 20% without lowering success” is a hypothesis until measured.

## Diagnostic interaction cost

Use interaction counts to locate friction, not to declare usability. Count separately:

- direct selections or keystroke groups;
- navigation transitions and modal layers;
- new concepts the user must recall rather than recognize;
- fields re-entered despite known data;
- mode or tool switches;
- waits without useful progress or feedback;
- backtracks, failed attempts, and recovery actions;
- permission or ownership handoffs.

If a single comparison number is useful, create a **local diagnostic index** with stable weights chosen before comparing candidates. Label it as a team heuristic, publish the components, and never present it as a validated human-factors measure. A lower index must not override worse task success, accessibility, error severity, or user confidence.

## Friction ledger

| ID | Scenario and step | Friction | Evidence class | Frequency | Severity | Current value | Treatment | Regression risk | Proof |
|---|---|---|---|---|---|---|---|---|---|

Use these evidence classes:

1. **Instrumented**: product analytics, controlled study, support volume, or production traces with a defined denominator.
2. **Observed**: reproducible inspection, runtime walkthrough, accessibility audit, or code-backed path.
3. **Reported**: stakeholder or user claim not yet independently verified.
4. **Hypothesis**: heuristic judgment or synthetic-scenario prediction.

Treat evidence class as confidence, not importance. A high-severity hypothesis may deserve a small reversible experiment before a large implementation.

## Prioritization

Rank candidates using:

- reach or workflow frequency;
- outcome impact and error severity;
- evidence confidence;
- implementation and migration effort;
- reversibility and blast radius;
- dependency on product policy or missing data.

If a numeric score aids sorting, document the formula before scoring and retain the raw factors. Never use a composite score to conceal a safety veto, accessibility failure, or weak evidence.

Prefer this sequence:

1. Remove duplicate work and dead ends.
2. Fix misleading labels, hierarchy, and entry points.
3. Preserve context and make system state visible.
4. Default or automate predictable low-risk choices.
5. Consolidate related actions around the user's object.
6. Add expert acceleration after the basic path is sound.
7. Refine visual density and polish after structural friction is resolved.

## Before-and-after scorecard

| Outcome or guardrail | Baseline | Candidate target | Evidence source | Validation method | Result |
|---|---|---|---|---|---|
| Task and critical-error-free success | | | | | |
| First-attempt success | | | | | |
| Completion/discovery time | | | | | |
| Errors, false completion, and recovery | | | | | |
| Redundant work/handoffs | | | | | |
| Accessible completion | | | | | |
| Confidence or post-task ease | | | | | |
| Responsiveness and state feedback | | | | | |
| Business/operational guardrail | | | | | |

Use `unknown` rather than invented precision. Keep targets directional if no baseline exists, then define how to establish the baseline.

## Example

**Synthetic scenario — experienced operations lead, desktop, interrupted work**

When a failed payout enters review, Mira needs to identify the cause, correct recoverable data, and leave a trace for Finance. She enters from the alert expecting the affected payout and its owner, but lands on a generic queue. She filters the queue, opens a detail page, copies an identifier into a separate customer search, returns, opens an overflow menu, and starts a repair form that asks for the same identifier. A validation error clears the form. She repeats the search and submits, then returns to the queue to verify status. The task is complete only when the payout shows `Ready for retry` with her note and Finance can follow the same deep link.

Current path:

`alert -> generic queue -> filter -> payout -> copy ID -> customer search -> back -> overflow -> repair form -> re-enter ID -> validation loss -> repeat -> submit -> queue -> verify`

Lean path hypothesis:

`deep-linked payout workspace -> cause and owner visible -> inline repair with known data -> retained validation -> preview -> submit -> status and audit note update in place`

The improvement is not merely fewer clicks. It removes re-identification, cross-surface recall, duplicate input, lost state, and a verification round trip while preserving preview, auditability, ownership, and recovery.
