---
name: streamline
description: Audit, redesign, and, when authorized, implement streamlined product workflows across frontend, mobile, admin, dashboard, settings, forms, onboarding, and multi-role operational interfaces. Use when asked to streamline or simplify UX, reduce unnecessary steps or clicks, remove redundancy, improve findability, consolidate scattered actions or settings, clarify navigation, reduce cognitive load, or make an agent-built UI feel intentional, intuitive, efficient, accessible, and measurably easier to use.
---

# Streamline

Optimize the user's end-to-end task, not isolated screens. Create a concrete mental movie of real use with clearly labeled synthetic stories, remove friction that provides no user or system value, and preserve friction that protects comprehension, consent, safety, security, or recovery.

## Choose the operating mode

- **Audit** when asked to review, diagnose, or recommend. Inspect and report; do not edit.
- **Design** when asked for a future flow, information architecture, wireframe, or specification. Produce the design artifact without implementing unless requested.
- **Implement** when asked to change or build. Make the smallest coherent change that improves the full task, then validate it.
- **Measure** when asked to prove an improvement. Define or use instrumentation, compare a baseline with a candidate, and state the evidence boundary.

Combine modes only when the request authorizes them. Preserve unrelated work and existing capabilities outside the named scope.

## Ground the work

1. Identify the user outcome, primary and secondary actors, starting points, completion state, frequency, device/context, permissions, and cost of error.
2. Inspect the actual product surface, routes, states, copy, design system, analytics, support signals, and tests that are available. Trace the workflow across screens and handoffs rather than inferring it from one component.
3. Distinguish observed facts, instrumented facts, stakeholder claims, and hypotheses. Within synthetic stories, tag details as **verified**, **inferred**, or **unknown**. Never present synthetic users, estimated timings, or heuristic scores as real research.
4. Establish the current path before proposing a shorter one. If no runnable UI or data exists, create an explicit hypothesis baseline and say what remains unverified.

Do not stop for every missing input. Make reversible, labeled assumptions when they do not materially change the scope; ask only when the answer changes product policy, risk, or the intended user outcome.

## Run the streamlining loop

### 1. Build the mental movie

Write synthetic workflow stories in present tense so the interface can be pictured in use. For each important workflow, include:

- the persona's role, experience, context, trigger, and goal;
- where they enter and what they expect to find;
- each decision, input, system response, wait, and state change;
- branches for errors, empty states, permissions, interruption, and return;
- what information must remain visible or remembered;
- the exact observable condition that means the task is complete.

Cover the dominant happy path plus the most consequential variants. Prefer a novice or infrequent user, a frequent expert, a recovery case, and a cross-role or cross-device handoff when those variants exist. Label every story **Synthetic scenario**.

At each consequential step, run a cognitive walkthrough: will this actor pursue the right goal, notice the correct action, connect it to the intended outcome, and understand the feedback? Treat a confident but incorrect completion as a failure, not success.

Read [references/workflow-lab.md](references/workflow-lab.md) before mapping a complex workflow or creating a scorecard.

### 2. Measure the current path

Select metrics that reflect the outcome:

- unassisted task success, critical-error-free success, first-attempt success, and false completion;
- median and tail completion time;
- time to find the first correct action;
- error, recovery, abandonment, and support-escalation rates;
- repeated inputs, reversals, context switches, handoffs, and navigation transitions;
- post-task ease or confidence;
- accessibility and keyboard completion;
- acknowledgment latency and field responsiveness for interaction-critical web paths;
- business or operational outcomes affected by the task.

Treat click count as supporting evidence, never the goal. One clear, reversible step can be better than a shorter path that hides state, overloads a screen, or increases errors. Do not fabricate a numeric baseline. Record observable counts, instrument real usage, or mark a target as a hypothesis.

### 3. Build a friction ledger

For every step or control, ask whether it:

1. advances the user's outcome;
2. supplies information needed for a sound decision;
3. prevents a material error or protects consent, security, privacy, or compliance;
4. preserves state, coordination, or recovery across a system boundary.

If none applies, remove, combine, default, automate, or relocate it. Record the affected scenario, evidence, severity, frequency, proposed treatment, possible regression, and proof method.

Look especially for agent-built UI residue:

- navigation that mirrors routes, services, or database entities instead of user goals;
- one card, page, or setting per backend capability;
- repeated summaries, confirmations, fields, filters, or status labels;
- nested modals, dashboard-within-dashboard layouts, and dead-end detail pages;
- primary actions hidden in overflow menus or unrelated settings screens;
- jargon, raw identifiers, and system state presented without a user decision;
- premature choices, noisy helper copy, decorative containers, and competing calls to action;
- lost context after save, search, validation, refresh, permission failure, or back navigation.

### 4. Design the lean path

Prefer changes that remove whole decisions or handoffs over cosmetic click reduction:

- organize navigation around user objects and outcomes;
- make the likely next action obvious while keeping alternatives discoverable;
- place local controls at the point of use and keep global settings in one stable, searchable home;
- provide safe defaults, remembered context, recents, deep links, and sensible preselection;
- reveal advanced or infrequent controls progressively with a visible information scent;
- use inline editing and validation when they preserve context;
- support bulk actions for genuinely repetitive work and previews for consequential work;
- replace repeated confirmations with prevention, constraints, undo, or reversible drafts where risk permits;
- maintain status, ownership, progress, and system feedback near the action that caused them;
- preserve keyboard access, focus order, readable targets, responsive behavior, and assistive-technology semantics.

Refine aesthetics systemically: establish one visual hierarchy, align spacing and typography to existing tokens, group by meaning, tune density to task frequency, reduce ornamental chrome, and use color or motion only to convey state or priority. Do not trade clarity for minimalism.

Do not preselect factual, consent, eligibility, or other answers that require a deliberate user claim. Design unfamiliar public flows for focus and explanation; design repeated expert work for comparison, density, batch operation, and shortcuts without lowering accessibility.

Apply the deletion test before adding a new abstraction or surface: if removing it would not erase a distinct user decision, durable state boundary, safety control, or reusable policy, do not add it.

### 5. Compare before and after

Show the current and proposed paths side by side. For each proposed change, connect:

`friction -> design treatment -> affected scenario -> expected metric -> validation method -> regression risk`

Rank changes by user impact, frequency, evidence confidence, implementation effort, and reversibility. Prefer the smallest coherent set that improves the outcome without scattering the experience.

### 6. Implement only when authorized

- Reuse the product's routes, state model, components, tokens, and domain language.
- Preserve deep links, permissions, auditability, validation, undo/recovery, and adjacent capabilities.
- Cover loading, empty, partial, stale, error, retry, success, and interrupted states.
- Acknowledge actions promptly and expose queued, running, succeeded, failed, and safely cancellable states where they exist.
- Avoid weakening tests, accessibility gates, browser budgets, or safety controls to make the redesign pass.
- Add focused workflow tests and instrumentation at stable outcome boundaries where appropriate.
- Keep generated artifacts and source in sync through their owning generator.

### 7. Validate the complete task

Replay every synthetic scenario against the candidate. Validate the dominant path and consequential branches across relevant viewport, input, permission, and data states. Use automated checks for contracts and regressions, but use interaction-level evidence for claims about usability.

When possible, compare the same task and population before and after. Report sample size, environment, metric definition, and uncertainty. A locally passing test proves neither deployed behavior nor improved human usability.

## Guardrails

- Do not equate fewer clicks with better UX.
- Do not hide essential status or destructive consequences to make a screen look clean.
- Do not remove authentication, consent, confirmation, or review steps without evaluating their risk function.
- Do not consolidate unrelated work into a giant dashboard or ambiguous universal action.
- Do not invent analytics, user quotes, personas, or usability findings.
- Do not optimize only the happy path; include recovery and re-entry.
- Do not move a hard-to-find setting without also fixing navigation, naming, search, links, and migration cues.
- Do not replace domain language merely to sound friendly when precision matters; explain it at the decision point.

Read [references/ux-streamlining-research.md](references/ux-streamlining-research.md) when a recommendation needs source-backed rationale, when choosing between competing heuristics, or when defining a study.

## Output contract

Scale the detail to the task, but keep this order:

1. **Outcome** — the user outcome and the highest-leverage simplification.
2. **Mental movie** — labeled synthetic scenarios that make current use tangible.
3. **Current path** — workflow map and baseline evidence.
4. **Friction ledger** — ranked unnecessary, misplaced, or risky interactions.
5. **Lean path** — proposed future flow and why each change earns its place.
6. **Scorecard** — baseline, target, evidence source, and validation method.
7. **Implementation and proof** — only when authorized; list changed surfaces and actual validation.
8. **Risks and unknowns** — preserved friction, policy questions, and unverified assumptions.

For a narrow change, compress these into a concise before/after recommendation. For a systemic workflow, include the full ledger and scorecard.

## Final self-check

Before responding, verify that:

- every removal maps to a real workflow step;
- every recommendation serves a named scenario and measurable outcome;
- synthetic evidence is labeled and real evidence is traceable;
- safety, accessibility, permissions, and recovery remain intact;
- the proposal reduces cognitive or operational work, not merely visible controls;
- implementation claims match the proof actually run.
