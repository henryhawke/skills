# Workflow lab

Use this reference to turn an ambiguous “simplify this” request into inspectable workflow artifacts, evidence-tagged decisions, and a falsifiable before/after contract.

Keep these labels visible wherever claims are mixed:

- **INSTRUMENTED**
- **OBSERVED**
- **REPORTED**
- **EXTERNAL**
- **HYPOTHESIS**
- **UNKNOWN**

Do not create every artifact by default. Use the smallest set that exposes the decision, the risk, and the proof boundary.

## Contents

- [Evidence rules](#evidence-rules)
- [Task-episode brief](#task-episode-brief)
- [Workflow inventory](#workflow-inventory)
- [Scenario portfolio](#scenario-portfolio)
- [Mental-movie template](#mental-movie-template)
- [Cognitive walkthrough](#cognitive-walkthrough)
- [Workflow and service maps](#workflow-and-service-maps)
- [Friction model](#friction-model)
- [Risk, failure, and state models](#risk-failure-and-state-models)
- [Metric catalog](#metric-catalog)
- [Instrumentation contract](#instrumentation-contract)
- [Before-and-after scorecard](#before-and-after-scorecard)
- [Method selection](#method-selection)
- [Benchmark and study plans](#benchmark-and-study-plans)
- [Prioritization](#prioritization)
- [Recommendation and decision records](#recommendation-and-decision-records)
- [Worked example](#worked-example)

# Evidence rules

## Evidence classes

| Label | What qualifies | What it can support | What it cannot support by itself |
|---|---|---|---|
| **INSTRUMENTED** | Analytics, traces, measured performance, support counts, experiment results, or controlled study data with a defined denominator | Frequency, distribution, correlation, measured outcome, or causal effect when design supports it | Why behavior occurred unless the measure captures it |
| **OBSERVED** | Reproducible runtime inspection, repository-backed behavior, accessibility inspection, or direct task observation | What the product does; what a participant did in the observed context | Population frequency or broad preference |
| **REPORTED** | User, support, stakeholder, operator, or domain-expert statement | A need, concern, policy claim, or investigation lead | Prevalence or verified product behavior |
| **EXTERNAL** | Standard, published research, design-system guidance, or reputable industry evidence | General principles, known risks, pattern rationale, and study methods | Local user behavior or proof that a candidate works here |
| **HYPOTHESIS** | Heuristic diagnosis, synthetic scenario, prediction, estimate, or inference | A testable explanation or candidate direction | A finding, baseline, or proven improvement |
| **UNKNOWN** | Missing, inaccessible, ambiguous, or conflicting information | A visible evidence gap | Any confident conclusion |

## Claim format

Use this structure for material claims:

```text
[EVIDENCE] Fact or observation.
Interpretation: what the fact may mean.
Decision: what should change, if anything.
Proof boundary: what remains unverified.
```

Example:

```text
[OBSERVED] A validation failure clears three valid fields and returns focus to the page heading.
Interpretation: recovery requires duplicate entry and the error may be difficult to locate.
Decision: preserve valid values, associate errors with fields, and move focus to a useful error summary.
Proof boundary: effect on completion and recovery time has not been measured.
```

## Evidence boundary template

```markdown
### Evidence boundary

**Inspected**
- [runtime surfaces, routes, states, code paths, analytics, tests, support evidence]

**Not inspected or unavailable**
- [production data, user research, policy owner, assistive-technology environment, mobile build]

**Reliable facts**
- [INSTRUMENTED/OBSERVED statements]

**Reported constraints**
- [REPORTED statements]

**Working hypotheses**
- [HYPOTHESIS statements]

**Unknowns capable of reversing the design**
- [UNKNOWN statements]
```

# Task-episode brief

Complete this before counting steps or proposing surfaces.

```markdown
## Task episode — [verb + object + verified result]

**Actor and role:**
**Permissions/authority:**
**Proficiency and frequency:**
**Device/input/environment:**
**Trigger:**
**Entry point(s):**
**Primary object/case:**
**User outcome:**
**Observable completion state:**
**Start boundary:**
**End boundary:**
**Known data at start:**
**Missing, stale, or disputed data:**
**Offline work or external tools:**
**Human handoffs:**
**Interruption/re-entry expectation:**
**Cost of error:**
**Reversibility:**
**Business/operational guardrails:**
**Evidence boundary:**
```

## Boundary test

The episode boundary is probably too narrow when:

- the user enters from a notification, message, search result, or external system that is excluded;
- “success” is submission rather than a verified durable outcome;
- another person must approve, repair, or reconcile the result;
- the user must return to a queue, email, or report to confirm completion;
- interruption, refresh, or cross-device continuation is common;
- errors create downstream work not visible on the current screen.

The boundary is probably too broad when it combines unrelated outcomes, actors, or policies under verbs such as “manage,” “handle,” or “administer.” Split it into independently completable episodes.

# Workflow inventory

When several workflows compete for attention, inventory them before selecting one.

| Workflow | Actor | Trigger | Verified outcome | Frequency/reach | Error consequence | Current evidence | Suspected friction | Decision |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

Choose first the workflow with the strongest combination of user consequence, frequency, evidence, and tractable scope. Do not let a visually messy but low-value screen outrank a common blocked outcome.

# Scenario portfolio

Choose the smallest portfolio that can reveal a different design decision.

| Scenario lens | Include when | What it exposes | Likely design reversal |
|---|---|---|---|
| First-time or infrequent | Labels, sequence, or policy are unfamiliar | Learnability, information scent, requirement clarity | More guidance, focus, or review may beat compression |
| Frequent expert | Task repeats or volume is high | Scanning, density, shortcuts, templates, bulk work | Dense comparison and acceleration may beat one-item-at-a-time flow |
| Interrupted/resumed | Work is long, asynchronous, or performed amid other tasks | Persistence, re-entry, draft state, ownership | Autosave, deep links, recents, and explicit state become essential |
| Error/recovery | Inputs, dependencies, or services can fail | Prevention, retained work, feedback, escalation | Inline recovery or compensation may beat a shorter happy path |
| Permission/handoff | Another role owns data or approval | Discoverability, disabled/hidden actions, responsibility, audit | Handoff and status may be more important than direct action |
| Accessible/constrained input | Keyboard, assistive technology, zoom, touch, or motion constraints matter | Semantics, focus, order, targets, alternatives | Custom gestures, hover, or hidden updates may be unacceptable |
| Empty/partial/stale/high-volume data | Data state changes the task | Guidance, trust, scanning, refresh, partial action | One default layout may not serve all states |
| Slow/degraded system | Acknowledgment or completion can be delayed | Duplicate submit, polling, progress, retry safety | Explicit operation states and cancellation may be required |
| High-consequence | Money, deletion, publication, permissions, consent, security, legal or safety effect | Scope, review, authorization, audit, reversibility | Protective friction must remain, but can be made clearer and less duplicative |
| AI-assisted | Suggestions or actions are probabilistic | Calibration, provenance, correction, authority, partial failure | Draft/review may be safer than direct automation |

Selection rule:

1. Always include the dominant scenario.
2. Add a scenario only when it exposes a meaningful branch, risk, accessibility need, or frequency pattern.
3. Add the highest-consequence plausible failure even if it is infrequent.
4. Stop when additional stories repeat the same design implications.

# Mental-movie template

Write in present tense. Use concrete product nouns and observable states. Do not write a generic persona biography.

> **Synthetic scenario — [role, proficiency, frequency, context]**\
> **Trigger:** [what happens immediately before entry].\
> **Goal:** [observable outcome] before/under [constraint].\
> **Starting state:** [known, selected, dirty, stale, missing, or permission-limited data].\
> **Current episode:** [entry, orientation, decisions, actions, waits, feedback, branches, and verification].\
> **Failure or interruption:** [likely error/degradation and recovery].\
> **Done means:** [durable state visible to the actor and affected roles].\
> **Re-entry:** [how the actor returns without reconstructing context].\
> **Evidence tags:** [which details are observed, reported, hypothesized, or unknown].

Follow the narrative with a path:

```text
trigger -> entry -> orient -> decide -> act -> acknowledge -> system transition -> verify -> recover/handoff if needed -> done -> re-enter
```

Then use a beat table:

| Beat | Actor goal | Visible state | Action or decision | System response | Context carried | Branch/failure | Completion evidence | Effort tags | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

## Scenario quality check

A useful scenario includes only traits that change the workflow:

- role and authority;
- proficiency and frequency;
- device/input and environment;
- urgency or interruption;
- accessibility need;
- data state or volume;
- consequence of error.

Reject scenarios that rely on invented preferences, demographics, motivation, frequency, or business rules.

# Cognitive walkthrough

Run the walkthrough at each consequential beat, not merely once per screen.

| Question | Failure signal | Likely root cause | Candidate evidence |
|---|---|---|---|
| Will the actor form the correct immediate goal? | They pursue a plausible but wrong subtask | Task model, hierarchy, or sequence mismatch | First action, observation, tree test, support issue |
| Will they notice the correct action? | Action is missed, found late, or reached through search/backtracking | Weak prominence, placement, availability, or access | First-click path, discovery time, visual/keyboard inspection |
| Will the label predict the result? | They hesitate, open the wrong destination, or avoid a vague action | Poor information scent or domain mismatch | Tree test, terminology research, observation |
| Can they supply the required information? | They must recall, re-enter, translate, or seek help | Missing context, redundant entry, premature question | Form trace, process map, error logs |
| Will they understand system feedback? | Repeated clicks, polling, false completion, or uncertainty | Missing acknowledgment, progress, status, or completion state | Trace timings, observation, status inspection |
| Can they detect a wrong result? | They leave believing the task is complete | Ambiguous success, stale UI, hidden partial failure | False-completion task test, audit comparison |
| Can they recover locally? | Valid work is lost, context resets, or support is required | Weak validation, retry, undo, persistence, or escalation | Error replay, recovery task, support traces |
| Is the same outcome accessible? | Keyboard/AT/touch users cannot reach or perceive it | Semantic, focus, target, gesture, or announcement failure | Manual task test and automated accessibility checks |

Record failures as evidence-tagged ledger items. Do not convert the walkthrough directly into a claim about real-user prevalence.

# Workflow and service maps

## Step map

Use one row per meaningful user or system transition.

| ID | Stage | Actor and intent | Surface/state | Action or decision | Data used/created | System transition | Feedback | Branch/failure | Context retained | Evidence | Effort | Value | Risk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | |

## Service map

Use this when the episode crosses people, systems, channels, or asynchronous boundaries.

| Stage | User/actor lane | Interface/channel | Service or backend lane | Human/operations lane | Data/audit lane | Failure and recovery | Owner |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Object and state map

Use this when the user acts on a durable object such as an order, case, record, document, deployment, request, or account.

```markdown
**Object:**
**Source of truth:**
**Identity and deep-link key:**
**Actors and permissions:**
**Valid states:**
**Allowed transitions:**
**Transition initiator:**
**Side effects:**
**Audit requirement:**
**Concurrency/staleness rule:**
**Cancellation/compensation rule:**
**Visible completion evidence:**
```

# Friction model

## Effort taxonomy

Tag each step with every meaningful cost. Keep the vector; do not collapse it prematurely into one score.

| Tag | Cost | Diagnostic questions |
|---|---|---|
| **FIND** | Locate destination, object, action, or status | Is the entry point where the actor expects? Does the label predict the destination? |
| **UNDERSTAND** | Interpret terminology, hierarchy, requirements, state, or consequence | Is the information decision-relevant and expressed in the actor's language? |
| **DECIDE** | Make a choice | Is the choice necessary now? Can it be constrained, delayed, recommended, or safely defaulted? |
| **REMEMBER** | Carry facts or state in memory | Can the product keep it visible, retain it, or provide recognition instead? |
| **ENTER** | Type, select, format, or repeat data | Does the system already know it? Is the requested precision necessary? |
| **NAVIGATE** | Change page, layer, mode, tool, channel, or device | Does the transition preserve context and match the task boundary? |
| **WAIT** | Experience latency or uncertain progress | Is acknowledgment immediate? Is progress useful? Is completion detectable? |
| **COORDINATE** | Handoff, approve, notify, or reconcile | Is ownership visible? Can the handoff preserve context and an audit trail? |
| **RECOVER** | Correct, retry, undo, recreate, or escalate | Is valid work preserved? Is recovery local, safe, and comprehensible? |
| **VERIFY** | Confirm the durable outcome | Is verification built into the completion state or forced into another surface? |
| **ACCESS** | Overcome an input, semantic, visual, motor, cognitive, or assistive-technology barrier | Is there an equivalent, perceivable, operable route and feedback? |

## Value test

For every step or control, ask whether it supplies:

1. **Outcome** — advances the intended result.
2. **Comprehension** — supports a sound decision.
3. **Protection** — prevents material error or preserves safety, consent, privacy, security, or compliance.
4. **Continuity** — preserves state, synchronization, ownership, recovery, or re-entry.
5. **Coordination** — enables a necessary approval, handoff, shared understanding, or audit record.
6. **None** — avoidable, duplicate, ornamental, misplaced, or implementation-driven work.

## Root-cause prompts

Before selecting a UI treatment, test the layer:

- **Outcome:** Is the task itself necessary, or can the upstream condition be prevented?
- **Policy:** Does a rule require this step, or has the interface merely inherited a convention?
- **Information architecture:** Is the destination grouped and named according to the actor's mental model?
- **Content:** Is terminology, instruction, or consequence unclear?
- **Interaction:** Is the right capability present but poorly placed or sequenced?
- **Data:** Is known data unavailable, duplicated, stale, or inconsistent?
- **State:** Is the source of truth, transition, ownership, or completion unclear?
- **Permission:** Is the actor blocked by authorization or by poor discoverability of a handoff?
- **Reliability/performance:** Does latency, partial failure, or retry behavior create duplicate work?
- **Accessibility:** Is the route unavailable or disproportionately costly for an input/context?
- **Operations:** Does local simplification move work to another person or system?

## Friction ledger

| ID | Scenario/step | Evidence | Friction and root cause | Effort tags | Frequency/reach | Severity | Current value | Proposed treatment | Safeguard retained | Regression risk | Proof method | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | |

### Severity anchors

| Severity | Definition |
|---|---|
| **S0 Cosmetic** | No meaningful task effect; polish only |
| **S1 Minor** | Noticeable effort or delay with easy recovery |
| **S2 Material** | Repeated waste, avoidable errors, abandonment risk, or impaired confidence |
| **S3 Major** | Task failure, lost work, support/privileged rescue, cross-user impact, or serious accessibility barrier |
| **S4 Critical** | Material financial, permission, privacy, security, legal, safety, or irreversible harm |

Do not infer frequency from severity. A rare critical failure and a common minor cost require different treatments and proof.

# Risk, failure, and state models

## Risk tier worksheet

```markdown
**Action/transition:**
**Affected object(s):**
**Who is affected:**
**External side effect:**
**Reversible:** yes / partially / no
**Time to detect:**
**Time/cost to recover:**
**Authorization required:**
**Consent or review required:**
**Audit requirement:**
**Duplicate-action consequence:**
**Stale/concurrent-action consequence:**
**Risk tier:** low / moderate / high / critical
**Required safeguards:**
**Owner of policy decision:**
```

## Failure-mode table

Use a lightweight failure analysis when errors can be expensive or hidden.

| Failure mode | Cause | Affected scenario | User/system consequence | Severity | Likelihood evidence | Detectability | Current prevention | Current recovery | Candidate safeguard | Verification |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |

Do not turn severity × likelihood × detectability into unquestioned truth. Raw factors and safety vetoes remain visible.

## State-transition table

| Current state | Trigger | Preconditions | User-visible acknowledgment | System work | Success state | Partial state | Failure state | Retry rule | Cancel/undo/compensate | Audit/instrumentation |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |

Common states to consider:

```text
idle -> editing -> validating -> submitting -> accepted/queued -> running
running -> succeeded | partially_succeeded | failed | cancelled | timed_out
editing/submitting/running -> stale | interrupted
failed/stale/interrupted -> corrected -> retried | abandoned | escalated
succeeded -> undone/compensated where truthful
```

Use only states that exist in the domain. Never show completion before the durable source of truth confirms it unless the interface clearly identifies an optimistic, reversible state.

## Branch matrix

| Dimension | Required variants |
|---|---|
| Data | empty, partial, stale, malformed, high-volume, conflicting |
| Permission | allowed, read-only, hidden by policy, request access, handoff required |
| Network/service | immediate, slow acknowledgment, long-running, timeout, partial failure, unavailable dependency |
| User continuity | fresh entry, deep link, refresh, browser/app back, interruption, cross-device return |
| Action consequence | reversible, destructive, bulk, external side effect, duplicate submission |
| Input/context | keyboard, touch, representative AT, zoom/reflow, reduced motion, small viewport |

# Metric catalog

Choose the fewest metrics that can decide whether the task improved. Fix the definition and denominator before comparison.

| Metric | Definition | Notes |
|---|---|---|
| **Unassisted verified success** | Eligible episodes reaching the defined durable completion state without help / eligible episodes started | Primary effectiveness metric for most tasks |
| **Critical-error-free success** | Episodes completed without a predefined critical error / episodes started | Required for consequential workflows |
| **First-attempt success** | Correct completions without a failed submit, wrong branch, or rescue / episodes started | Useful for clarity and prevention |
| **False completion** | Episodes the actor believes are complete but are not durably complete / episodes started | Treat as a severe feedback failure |
| **Completion time** | Time from defined start to verified completion among successful episodes | Report median and a tail percentile or range; do not report only mean |
| **Discovery time** | Time from entry to the first correct action | Useful for findability and hierarchy |
| **Direct path rate** | Episodes reaching the intended destination without backtracking or alternate destinations / episodes started | Useful for information architecture |
| **Recoverable error incidence** | Episodes containing a recoverable error / episodes started | Classify by cause and severity |
| **Recovery success** | Correct recoveries / recoverable-error episodes | Pair with recovery time and lost work |
| **Abandonment** | Started episodes not completed within the defined window / eligible episodes started | Define the window and exclusions |
| **Re-entry success** | Interrupted episodes later completed without reconstruction or rescue / interrupted episodes | Tests persistence and continuity |
| **Redundant entry** | Values already known to the system that must be entered again per episode | Count fields and keystroke groups separately if useful |
| **Navigation reversals** | Backtracks or repeated destination visits per episode | Diagnose misleading grouping or labels |
| **Context switches** | Changes of tool, mode, surface, device, or person required per episode | Include offline and human handoffs |
| **Unproductive wait** | Time without useful progress, acknowledgment, or actionable feedback | Separate system latency from uncertainty |
| **Support escalation** | Episodes requiring support or privileged rescue / episodes started | Reveals hidden operational cost |
| **Accessible completion** | Equivalent verified completion by keyboard and representative AT/input contexts | Record barriers and extra effort, not only pass/fail |
| **Post-task ease/confidence** | Consistently worded rating immediately after the task | Pair with observed success to detect false confidence |
| **Operation latency** | Acknowledgment and durable-completion latency for the task action | Use distributions and distinguish client/server/queue work |
| **Field web performance** | Relevant P75 LCP, INP, and CLS by workflow/device where applicable | Supporting quality guardrail, not a substitute for task metrics |
| **Business/operational guardrail** | Task-specific quality, revenue, risk, throughput, support, or rework measure | Define direction and unacceptable regression before testing |

## Measurement rules

- Segment when role, permission, device, task complexity, data volume, or accessibility context materially changes the workflow.
- Do not average away a failed minority or high-consequence path.
- Use counts and observed ranges for small samples. Add confidence intervals or statistical tests only when the design supports them.
- Measure time among successful attempts and separately report failures; a fast failure is not efficiency.
- Keep subjective ease separate from correctness; both matter, but they answer different questions.
- A target is a hypothesis until measured.

## Diagnostic effort vector

Use this for mechanical before/after comparison without pretending it is a validated usability score.

| Component | Baseline | Candidate | Delta | Evidence |
|---|---:|---:|---:|---|
| Decisions required | | | | |
| Concepts/requirements introduced | | | | |
| Recall dependencies | | | | |
| Fields/values entered | | | | |
| Known values re-entered | | | | |
| Pointer selections | | | | |
| Keystroke groups | | | | |
| Navigation transitions | | | | |
| Modal/layer changes | | | | |
| Tool/device switches | | | | |
| Human handoffs | | | | |
| Waits without useful feedback | | | | |
| Backtracks/failed attempts | | | | |
| Recovery actions | | | | |
| Separate verification actions | | | | |
| Accessibility barriers | | | | |

If a team uses a weighted local index, declare the weights before comparing candidates, publish all components, and never let the index override success, critical errors, accessibility, or confidence.

# Instrumentation contract

Instrument stable task boundaries and state transitions, not every click by default.

## Episode event model

```text
workflow_started
workflow_step_reached       # only for diagnostically meaningful boundaries
workflow_action_attempted
workflow_action_acknowledged
workflow_action_completed
workflow_action_partially_completed
workflow_action_failed
workflow_recovery_started
workflow_recovered
workflow_abandoned          # only when the definition is defensible
workflow_verified
```

## Minimum event fields

| Field | Purpose |
|---|---|
| `workflow_name` and version | Stable task identity and change comparison |
| `episode_id` | Correlates the task without relying on personal data |
| `timestamp` | Ordering and latency |
| `entry_point` | Findability and channel analysis |
| `actor_segment` | Role/permission/frequency segment when privacy-safe |
| `object_state` | Relevant state, not sensitive content |
| `step_or_transition` | Stable diagnostic boundary |
| `result` | succeeded, partial, failed, cancelled, stale, duplicate, denied |
| `error_class` | Actionable category, not raw secret/user content |
| `duration_ms` | Acknowledgment or transition timing |
| `experiment_or_release` | Candidate attribution |
| `client_context` | Platform/input/viewport class only when needed and privacy-safe |

## Instrumentation rules

- Define the durable completion signal from the source of truth.
- Avoid personal, sensitive, free-text, credential, or secret data in analytics.
- Do not change event semantics silently. Version them when the task boundary changes.
- Distinguish attempted, acknowledged, accepted/queued, completed, and verified.
- Track partial failure and duplicate-action prevention explicitly when relevant.
- Test that instrumentation itself does not block the task.

# Before-and-after scorecard

| Outcome or guardrail | Baseline | Candidate hypothesis/target | Evidence source | Validation method | Result | Decision threshold |
|---|---|---|---|---|---|---|
| Unassisted verified success | | | | | | |
| Critical-error-free success | | | | | | |
| First-attempt/false completion | | | | | | |
| Discovery/completion time | | | | | | |
| Errors, recovery, and lost work | | | | | | |
| Redundant work and handoffs | | | | | | |
| Accessible completion | | | | | | |
| Confidence/post-task ease | | | | | | |
| Acknowledgment and operation latency | | | | | | |
| Business/operational guardrail | | | | | | |

Use `unknown` instead of invented precision. When no baseline exists, define how it will be established and keep the target directional unless evidence supports a number.

## Recommendation-to-proof matrix

| Change | Evidence | Root cause | Scenario | Friction removed/moved | Safeguard retained | Predicted metric direction | Regression risk | Validation | Stop/revert condition |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

# Method selection

Choose the method that answers the actual uncertainty.

| Question | Best-fit methods | Useful outputs | Common misuse |
|---|---|---|---|
| Can users find a destination in the proposed hierarchy? | Tree test, navigation observation, search logs | Direct success, first choice, backtracking, time | Testing visual prominence instead of taxonomy |
| Is the visible action noticed and understood? | First-click/click test, cognitive walkthrough, task observation | First action, discovery time, interpretation | Rebuilding IA when placement is the issue |
| Can people complete the end-to-end task? | Moderated/unmoderated usability task, field observation | Success, errors, time, recovery, confidence | Calling a prototype preference test usability proof |
| What happens at scale? | Production funnel/traces, support data, performance telemetry | Frequency, distribution, breakpoints, segments | Inferring motivation from event sequences |
| Why does the breakdown happen? | Direct observation, contextual inquiry, interviews paired with behavior | Mental model, context, workaround, language | Using self-report alone to establish actual behavior |
| Does the candidate cause improvement? | Controlled experiment, matched before/after, interrupted time series where appropriate | Effect estimate and guardrails | Changing task definitions, populations, or instrumentation mid-comparison |
| Is the task accessible? | Keyboard and representative AT task testing plus automated checks | Equivalent completion, barriers, extra effort | Treating an automated scan as complete accessibility validation |
| Is an async or operational path reliable? | Trace/log review, fault injection where authorized, scenario replay | State transitions, duplicate/retry behavior, partial failure | Testing only immediate success |
| Is workload meaningfully lower in a complex task? | Task metrics plus a validated workload instrument such as NASA-TLX when appropriate | Mental/physical/temporal demand and frustration | Treating clicks as cognitive load |
| Is a high-risk change safe enough to release? | Failure analysis, domain review, staged rollout, monitored canary | Failure modes, safeguards, rollback evidence | Letting an opportunity score override a safety veto |

# Benchmark and study plans

## Benchmark task template

```markdown
### Benchmark task — [stable task name]

**Participant segment:**
**Starting context:**
**Trigger:**
**Provided data:**
**Information intentionally withheld:**
**Instruction:** [state the goal without revealing the path]
**Correct durable result:**
**Critical errors:**
**Allowed help:**
**Start timestamp:**
**End timestamp:**
**Abandonment rule:**
**Follow-up ease/confidence questions:**
**Environment/device/input:**
**Data complexity:**
**Version/build:**
```

Tasks should be believable, representative, stable across comparison, and objectively scorable. Do not coach the interface path in the task wording.

## Usability study plan

```markdown
## Study plan

**Decision this study will inform:**
**Workflow and version:**
**Research questions:**
**Segments and rationale:**
**Scenario portfolio:**
**Sample size and limitation:**
**Environment and data:**
**Primary metric:**
**Guardrails:**
**Critical-error taxonomy:**
**Task order/counterbalancing:**
**Facilitation and help policy:**
**Evidence capture:**
**Analysis method:**
**Success/revise/stop criteria:**
**Known bias and evidence boundary:**
```

## Production experiment plan

```markdown
## Experiment or staged comparison

**Decision:**
**Baseline and candidate:**
**Eligibility and assignment:**
**Task boundary/version:**
**Primary metric and denominator:**
**Guardrails:**
**Segments declared in advance:**
**Instrumentation validation:**
**Sample/runtime rationale:**
**Novelty, carryover, and interference risks:**
**Exposure and ramp plan:**
**Stop/revert conditions:**
**Analysis plan:**
**Owner and decision date:**
```

Do not launch an experiment that knowingly exposes users to an unbounded high-consequence failure mode. Establish the safety controls first.

# Prioritization

## Raw-factor table

| Candidate | Reach/frequency | Outcome impact | Error severity | Accessibility impact | Evidence confidence | Effort/migration | Reversibility | Blast radius | Policy/data dependency | Decision |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |

## Confidence anchors

| Confidence | Basis |
|---|---|
| **C1 Low** | Heuristic or synthetic hypothesis only |
| **C2 Emerging** | Reproducible observation or repeated report, but no population evidence |
| **C3 Strong** | Multiple evidence types or clear instrumented breakdown |
| **C4 Causal/validated** | Controlled comparison or repeated task evidence supports the expected effect |

Confidence is not importance. A severe low-confidence risk may justify a reversible investigation before a large build.

## Default sequence

1. Stop critical harm, false completion, inaccessible dead ends, and data loss.
2. Remove duplicate work, dead ends, and contradictory sources of truth.
3. Fix misleading entry points, labels, task order, hierarchy, and status.
4. Preserve context, valid input, ownership, and re-entry.
5. Reuse or safely derive known data.
6. Co-locate related actions around the user's object and outcome.
7. Add recovery, undo, or compensation before removing protective steps.
8. Accelerate high-frequency work with batch, saved state, templates, deep links, and shortcuts.
9. Automate bounded, observable, recoverable work.
10. Refine density and visual craft after the structural path is sound.

## Vetoes

A composite score cannot approve a candidate that:

- lowers correct or critical-error-free completion;
- creates an accessibility blocker or removes an equivalent route;
- violates authorization, consent, privacy, security, compliance, or audit requirements;
- creates silent partial failure, stale overwrite, or irrecoverable data loss;
- lacks a viable rollback/compensation path for a high-blast-radius change;
- depends on an unresolved product-policy decision.

# Recommendation and decision records

## Recommendation card

```markdown
### [Action-oriented recommendation]

**Affected episode and scenario:**
**Evidence:**
**Current friction:**
**Root cause:**
**Current control value:**
**Treatment:**
**Why this treatment:**
**Friction removed:**
**Friction moved or added:**
**Safeguards retained:**
**Predicted metric direction:**
**Accessibility implications:**
**Dependencies/migration:**
**Regression risk:**
**Validation method:**
**Stop/revert condition:**
**Confidence:**
```

## Decision record

```markdown
## Decision — [title]

**Date/version:**
**Owner:**
**Episode:**
**Decision:**
**Alternatives considered:**
**Evidence used:**
**Assumptions:**
**Safeguards:**
**Expected outcome:**
**Guardrails:**
**Validation:**
**Rollback/revision trigger:**
**Unresolved questions:**
```

## Compact narrow-change format

```markdown
**Outcome:**
**Observed current path:**
**Highest-leverage friction:**
**Proposed path:**
**Safeguard retained:**
**Expected delta (hypothesis):**
**Proof:**
**Unknowns:**
```

# Worked example

## Task episode

**Synthetic scenario — experienced operations lead, desktop, interrupted work**

A failed payout enters review. The operations lead needs to identify the cause, correct recoverable data, and leave a durable trace for Finance. The alert contains the payout identifier, but the link opens a generic queue. The lead filters, opens the payout, copies an identifier, searches a separate customer surface, returns, opens an overflow menu, and enters the same identifier in a repair form. A validation error clears valid values. After resubmission, the lead returns to the queue to confirm status. The task is complete only when the payout source of truth shows `Ready for retry`, the correction is recorded, and Finance can open the same object.

Evidence tags for this example are **HYPOTHESIS**; it is a reusable demonstration, not a real finding.

### Current path

```text
alert -> generic queue -> filter -> payout -> copy identifier -> customer search
-> return -> overflow menu -> repair form -> re-enter identifier
-> validation loss -> repeat -> submit -> return to queue -> verify
```

### Lean-path hypothesis

```text
deep-linked payout workspace -> cause, owner, and relevant customer context visible
-> inline repair with known values retained -> local validation -> consequence preview
-> submit -> acknowledged/running state -> durable status and audit note update in place
```

### Friction ledger excerpt

| ID | Step | Friction/root cause | Tags | Current value | Treatment | Safeguard | Proof |
|---|---|---|---|---|---|---|---|
| P1 | Alert to queue | Deep link discards known object context | FIND, NAVIGATE, REMEMBER | None | Link to object workspace | Permission check at destination | Discovery and completion task |
| P2 | Customer search | Separate surface forces identifier transfer | REMEMBER, ENTER, NAVIGATE | Comprehension | Show relevant customer context in the payout workspace | Preserve authoritative customer link | Error and time comparison |
| P3 | Validation | Valid input is cleared | ENTER, RECOVER | None | Retain valid values and focus useful error feedback | Existing validation rules | Recovery success/time |
| P4 | Post-submit verification | Completion is not visible where action occurs | WAIT, VERIFY, NAVIGATE | Continuity | Show acknowledged, running, and durable result in place | Source-of-truth confirmation and audit note | False-completion and duplicate-action test |

### Scorecard excerpt

| Outcome | Baseline | Candidate hypothesis | Guardrail | Validation |
|---|---|---|---|---|
| Unassisted verified success | unknown | increase | No loss of permission/audit integrity | Same benchmark task |
| Redundant entry | one repeated identifier plus validation re-entry | remove known-data entry and preserve valid fields | User can inspect linked customer | Step trace |
| Context switches | queue, payout, customer search, repair form, queue | one object workspace | No hidden cross-object dependency | Scenario replay |
| False completion | unknown | decrease through durable in-place status | No optimistic success label | Slow/partial-failure test |

The proposed path is a stronger hypothesis because it removes re-identification, cross-surface recall, duplicate entry, lost state, and a verification round trip while retaining permission, validation, preview, ownership, auditability, and recovery. It is not proven until the task is replayed or measured.
