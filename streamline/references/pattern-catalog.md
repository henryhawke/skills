# Streamlining pattern catalog

Use this catalog to select interaction treatments after the task episode, evidence boundary, root cause, and risk are understood.

A pattern is a **candidate mechanism**, not a universal answer. The same pattern can reduce effort in one context and create errors in another. State why the pattern fits, what safeguard it preserves, what new friction it introduces, and how the result will be tested.

## Pattern-selection contract

Before choosing a pattern, answer:

1. What verified user outcome is being improved?
2. Which scenario and exact step contains the friction?
3. Is the root cause policy, information architecture, content, interaction, data, state, permission, reliability, accessibility, or operations?
4. What value does the current step provide?
5. What is the action's consequence, reversibility, and blast radius?
6. Does the actor perform the task once, occasionally, or repeatedly at scale?
7. What state, context, and source of truth must remain visible?
8. What would make the candidate worse than the current path?
9. What metric and guardrail can decide between them?

Do not use a new component to disguise a missing product decision or inconsistent data model.

# Diagnostic treatment matrix

| Symptom | Likely root causes to test | First treatments to consider | Common wrong fix | Proof |
|---|---|---|---|---|
| Users cannot find an action | Wrong grouping, vague label, hidden permission, weak entry point, low prominence | Rename, regroup, expose at task point, add deep link or contextual entry | Add another dashboard card or generic “More” menu | Tree/first-action task and discovery time |
| Users open the wrong destination | Labels do not predict content; taxonomy mirrors system structure | Reframe navigation around user objects/outcomes; clarify nearby context | Change icon or color only | Direct/indirect success and backtracking |
| Same data is entered repeatedly | State not carried, systems disconnected, validation clears values | Retain, prefill, select from prior entries, derive safely | Add copy buttons or instruct users to remember IDs | Redundant-entry count and recovery task |
| Users hesitate over many choices | Premature decisions, weak defaults, mixed frequencies, unclear consequence | Remove, delay, group, recommend, or progressively disclose | Put all choices in a larger modal | First-attempt success and decision time |
| Users keep checking whether work finished | Weak acknowledgment, hidden async state, stale view, no durable completion signal | Show accepted/queued/running/result states in context; notify on completion | Add a spinner with no operation name or result | Duplicate actions and false completion |
| Validation creates rework | Late validation, generic errors, lost input, hidden requirements | Prevent where possible; preserve valid input; local errors; useful summary | Add more pre-submit confirmation | Recovery success/time and lost-work incidents |
| Frequent users repeat the same sequence | No saved context, batch operation, template, shortcut, or deep link | Saved views, defaults, recents, templates, bulk actions, keyboard acceleration | Compress the interface for everyone without testing novices | Successful throughput and error guardrails by segment |
| A setting is hard to find | Wrong local/global placement, naming, search, or migration | Put task-specific control at point of use; keep global policy in stable searchable home | Duplicate the setting in several unsynchronized places | Discovery task and source-of-truth check |
| Users cannot act because of permissions | Hidden ownership, unclear eligibility, no request/handoff route | Explain owner and state; request access; hand off with context | Show a dead disabled button or generic “not authorized” | Handoff completion and support escalation |
| A “simpler” screen creates downstream work | Boundary excludes verification, other roles, or operations | Expand episode and service map; preserve shared context | Optimize only the submitting user | End-to-end completion and downstream rework |
| AI output is accepted incorrectly | Poor calibration, weak provenance, automation bias, hidden uncertainty | Show basis/limits, make output inspectable, require review by risk, support correction | Add a confidence percentage with no calibration or one-click autonomous action | Corrected-result quality, false completion, override/recovery |

# Reduction patterns

Apply treatments in this order unless risk or evidence indicates otherwise.

## Eliminate

Use when a step has no outcome, comprehension, protection, continuity, or coordination value.

Required checks:

- confirm the step is not carrying a hidden policy, audit, ownership, or recovery function;
- remove the related route, state, copy, analytics, tests, and migration residue coherently;
- verify that another actor or channel does not inherit the work.

Avoid “removing” a step by hiding it in an overflow, background job, or support process.

## Prevent

Use when the best experience is avoiding the condition that creates the task, error, or choice.

Examples:

- constrain invalid states before submission;
- avoid duplicate records or submissions;
- make incompatible choices unavailable with a clear reason;
- detect stale data before overwrite;
- surface eligibility before a long form;
- fix the upstream notification or entry link.

Measure prevented incidents and unintended blocks. Prevention is not successful when it silently rejects legitimate edge cases.

## Reuse and retain

Use when the product already knows the value or context.

- retain valid form values through validation, navigation, refresh, and recoverable errors;
- carry object identity, filters, return path, ownership, and task state across surfaces;
- reuse previously supplied information within the same process;
- make prior values selectable when direct reuse is not safe;
- preserve draft and interrupted work according to policy.

Do not reuse stale, disputed, permission-restricted, or context-specific values without making their source and edit path clear.

## Derive and suggest

Use when the system can calculate or infer a low-risk value from reliable data.

- show the derived value at the decision point;
- make the basis understandable at the level needed for correction;
- allow correction when the result is not authoritative;
- provide a manual fallback when lookup or inference can fail;
- distinguish authoritative data from a suggestion.

Never silently derive a factual claim, consent, eligibility answer, legal assertion, or high-consequence choice that the actor must deliberately make.

## Relocate and co-locate

Use when the action or information is correct but appears away from the decision it supports.

- place object-specific actions on or beside the object;
- show requirements, consequences, owner, and status where the action occurs;
- keep global policy and defaults in one stable settings home;
- link from contextual controls to the governing global setting when needed;
- keep related inspect/edit/verify work in one workspace when the source of truth is shared.

Do not duplicate editable controls across surfaces unless synchronization and ownership are explicit.

## Combine

Use when separate steps operate on the same object, authority, and state boundary.

Combine only when:

- users need the information together;
- the actions share a source of truth and permission model;
- combined density remains scannable;
- errors can still be localized;
- the new surface does not erase distinct review or ownership boundaries.

Do not combine unrelated jobs into a universal dashboard or “command center.”

## Sequence and disclose

Use when complexity is legitimate but not all relevant at once.

- order questions and controls by dependency and task sequence;
- reveal conditional fields only after the triggering answer;
- keep common actions visible and advanced/infrequent actions behind a predictive label;
- preserve orientation, current choices, and a clear route back;
- avoid deep chains of disclosure.

Do not hide rare but critical safety, recovery, permission, or compliance actions solely because usage is low.

## Accelerate

Use after the basic path is understandable and reliable.

- saved views and remembered low-risk preferences;
- recent objects and deep links;
- templates and repeat-last-value where appropriate;
- batch selection and actions;
- keyboard shortcuts with visible discovery and non-keyboard equivalents;
- command/search surfaces for experts without replacing clear navigation;
- defaults scoped by role, workspace, or task when evidence supports them.

Measure expert throughput and error severity separately from novice success.

## Automate

Use only when the task is bounded, authorized, observable, and recoverable.

Automation requires:

- explicit scope and source of authority;
- reliable trigger and inputs;
- confidence/quality adequate for the consequence;
- visible state and ownership;
- exception and partial-failure handling;
- stop, override, correction, and recovery routes;
- audit/history for consequential effects;
- monitoring and rollback or compensation;
- a manual or degraded fallback where necessary.

Do not automate ambiguity. A repeated decision may still require human judgment, consent, or policy interpretation.

# Information architecture and navigation

## Organize around objects and outcomes

Prefer navigation labels that answer one of:

- What object am I working on?
- What outcome am I trying to reach?
- What stage or responsibility do I own?

Avoid top-level structures that expose service names, database entities, engineering boundaries, or feature inventory unless those are genuinely user concepts.

## Entry-point pattern

For each important episode, provide the best available entry:

1. contextual deep link from the trigger or notification;
2. stable object URL or route;
3. user-language navigation path;
4. search or recent item fallback;
5. recovery path from expired or unauthorized links.

A deep link should preserve object identity and intent while still enforcing current permissions and state.

## Breadcrumb, back, and return behavior

Use breadcrumbs for hierarchy, not browser history. Preserve:

- the user's prior list/query/filter state;
- a clear return destination after inspect/edit;
- deep-link behavior independent of prior navigation;
- refresh and browser/app-back semantics;
- no surprise loss of unsaved work.

Do not implement custom back behavior that contradicts platform expectations without a strong task need.

## Tabs

Use tabs when sections are peer views of the same object or workspace and users benefit from switching without losing context.

Required behavior:

- stable, concise labels;
- active state available visually and programmatically;
- predictable URL/history behavior when deep linking matters;
- no hidden sequential dependency between tabs;
- preserve unsaved state or warn truthfully.

Do not use tabs as a disguised multi-step process or to compress unrelated applications into one page.

## Local versus global settings

| Control type | Preferred placement |
|---|---|
| Changes only the current object or task | At the point of use |
| Repeated preference for one actor/workspace | Contextual control plus a stable preferences home when needed |
| Organization-wide policy or default | One governed, searchable settings location with owner and scope |
| Rare recovery/diagnostic action | Contextual error/recovery surface, not a generic settings maze |
| System-derived value with safe correction | At point of decision; avoid a setting unless users truly need persistent control |

When moving a setting, also update naming, search, links, help, permissions, migration cues, and any duplicated source of truth.

# Surface chooser

Choose the surface that matches task complexity, linkability, state, and consequence.

| Surface | Use when | Required behavior | Avoid when |
|---|---|---|---|
| **Inline action/edit** | Small, local, frequent, reversible change where surrounding context matters | Clear edit/save/cancel state, validation, focus, no layout surprise | Complex dependencies, long forms, high consequence without room for review |
| **Popover/menu** | Short secondary choices or low-complexity actions | Predictive trigger label, keyboard/focus support, close behavior, no critical hidden state | Primary action, long content, validation-heavy task, destructive action needing explanation |
| **Modal dialog** | A bounded decision must be resolved before continuing | Clear title, consequence, primary/secondary actions, focus containment/return, no nesting | Main journey, long multi-step work, comparison with background, deep linking/resumption |
| **Drawer/side panel** | Inspect or make a modest edit while preserving list/object context | Stable context, accessible focus/order, responsive fallback, clear close/save behavior | Deep workflows, multiple nested layers, small screens without suitable adaptation |
| **Dedicated page/workspace** | Complex, linkable, resumable, multi-state, high-context, or high-consequence work | Stable URL, complete hierarchy, status, recovery, responsive behavior | Tiny reversible action that would cause unnecessary navigation |
| **Sequential flow/wizard** | Questions depend on prior answers; unfamiliar task benefits from focus; progress is meaningful | Back without loss, progress, conditional sequence, review where needed, resumability | Expert comparison/bulk work or independent fields that fit one coherent surface |
| **Background/batch job** | Work is long-running or applies to many objects | Preview/scope, acknowledgment, queued/running/partial/result states, cancellation when safe, history | Immediate feedback is required or failures cannot be recovered per item |

Never nest modals. Avoid stacks of drawers, popovers, and dialogs that destroy orientation and focus behavior.

# Forms and data entry

## Ask only what is needed now

For every field, identify:

- the decision or downstream use it supports;
- who is authoritative for the value;
- whether the system already knows or can safely derive it;
- whether it can be asked later;
- whether a conditional branch can remove it for most users;
- the cost of wrong or missing data;
- retention, privacy, and permission constraints.

Delete fields without a current, legitimate use. “Might be useful later” is not enough.

## Labels, help, and requirements

- Use a persistent text label, not placeholder-only instruction.
- Put units, format, eligibility, and consequence beside the field they govern.
- Use examples only when they clarify a real ambiguity.
- Explain unusual data requests at the point of request.
- Mark optional fields clearly when most fields are required, or required fields clearly when most are optional; be consistent.
- Avoid long helper paragraphs that compete with the task. Link or disclose secondary detail predictively.

## Defaults, prefill, and memory

| Input type | Treatment |
|---|---|
| Value already supplied in this process | Prefill or make selectable unless policy/security exception applies |
| Stable low-risk preference | Remember visibly and make easy to change |
| Reliable system fact | Show as read-only or prefilled with source/edit route as appropriate |
| Low-risk inference | Suggest; do not silently assert if it may be wrong |
| Factual user claim, eligibility, consent, declaration | Require deliberate answer; do not preselect |
| High-consequence target/scope | Require explicit inspection and confirmation of affected objects |

## Validation

Use prevention before error messaging:

- constrain impossible formats without blocking legitimate input;
- accept reasonable formatting variations;
- validate when the system has enough information to help;
- avoid noisy validation while a user is still typing;
- preserve valid values;
- identify the specific field/item in text;
- explain the problem and a correction;
- place field errors beside the field and provide a useful summary when several errors exist;
- move focus or scroll only to help recovery, not as punishment;
- prevent duplicate submit while preserving a truthful retry path.

Server or source-of-truth validation remains authoritative even when client validation exists.

## Conditional questions

Reveal a question when its answer becomes relevant. The triggering control must make the dependency understandable.

When the trigger changes:

- clear hidden answers only when retaining them would be incorrect or unsafe;
- warn if clearing destroys meaningful work;
- preserve them when users may legitimately switch back and policy permits;
- ensure hidden fields are not accidentally submitted;
- make conditional state accessible and testable.

## Review/check step

Use a review step when users benefit from comparing consequential answers before commit, especially for money, publication, permissions, legal declarations, or complex multi-part submissions.

A review step must:

- show actual values and affected scope, not a generic summary;
- provide direct edit links that return to the same review state;
- preserve all valid data;
- state what happens after submission;
- use a specific final action label.

Do not add review to harmless, immediately reversible edits merely to create ceremony.

# Public and infrequent flows versus expert operations

| Dimension | Public/infrequent task | Expert/high-frequency operation |
|---|---|---|
| Primary need | Learnability, confidence, explanation | Throughput, comparison, state awareness |
| Density | Focused, fewer concepts at once | Compact but disciplined and scannable |
| Sequence | Explicit task order; one decision cluster at a time | Flexible order when independent; fast switching |
| Guidance | Plain requirements and contextual help | Concise labels, tooltips/help on demand |
| Defaults | Conservative and visible | Role/workspace defaults and remembered views when safe |
| Navigation | Clear forward/back/progress | Deep links, recents, saved views, shortcuts |
| Data presentation | Summary and progressive detail | Tables, comparison, sorting, filtering, bulk selection |
| Errors | Guided local recovery | Fast per-item resolution and batch exception handling |
| Review | Useful for consequential submission | Preview/diff for bulk or high-impact actions |
| Measurement | Success, false completion, confidence | Throughput, tail latency, error severity, interruption cost |

Do not force one layout to serve both segments when their task frequency and information needs materially differ. Shared semantics and accessibility still apply.

# Lists, tables, search, and filters

## Table versus cards

Use a table when users compare many records across consistent attributes, sort/filter, scan status, or act in bulk.

Use cards when items are heterogeneous, imagery or a small summary dominates, or comparison across columns is not the main task.

A useful table provides:

- meaningful default ordering;
- clear column labels and units;
- status expressed in text, not color alone;
- row identity and a stable detail route;
- responsive behavior that preserves priority or offers an alternate representation;
- keyboard and screen-reader semantics;
- explicit selection state and action scope;
- loading, empty, error, stale, and partial states.

Do not hide critical comparison data in repeated row expansion or tooltips.

## Search

- Search the user-recognizable fields and aliases relevant to the task.
- State what scope is being searched.
- Preserve the query on return and error.
- Show useful matches and explain zero results.
- Tolerate reasonable formatting and identifiers where safe.
- Do not use search as a substitute for coherent navigation when users should browse by known categories.

## Filters

- Use labels that describe the resulting set.
- Show active filters and result count.
- Provide a clear-all route.
- Preserve filters through detail inspection and return.
- Make default filters visible; avoid invisible exclusions that undermine trust.
- Order/filter choices by task value, not backend field order.
- Use dependent filters only when the relationship is clear and accessible.
- Consider saved views for repeated expert work.

## Pagination, infinite loading, and virtualization

Choose based on task behavior:

- pagination supports stable position, deep links, and bounded comparison;
- load-more supports continued browsing with an explicit user action;
- infinite loading can suit casual exploration but harms footer access, position, and task resumption when poorly implemented;
- virtualization may be needed for performance but must preserve semantics, keyboard behavior, and reliable selection.

Do not let loading strategy erase selection, scroll position, filter state, or an object's stable route.

## Bulk actions

Use bulk actions for genuinely repetitive operations where per-item policy and side effects are consistent.

Required behavior:

- explicit selection and selected count;
- clear scope across current page, filtered result, or all matching records;
- preview for consequential effects;
- per-item eligibility and exception reporting;
- no ambiguous partial success;
- idempotent/retry-safe execution where possible;
- progress and cancellation when work is long-running;
- durable result/history and a route to failed items;
- keyboard-accessible selection and action.

Do not make a destructive bulk action the visual default.

# Progressive disclosure and advanced controls

Use progressive disclosure when common work is being obscured by advanced or infrequent controls.

A good disclosure control:

- names what will be revealed;
- sits where the need arises;
- preserves current context and values;
- uses a stable open/closed state when repeated work benefits;
- remains keyboard and assistive-technology operable;
- does not hide status, errors, selected filters, or consequential effects.

Avoid generic labels such as “More,” “Advanced,” or icon-only controls when users cannot predict the content. Avoid more than one or two nested disclosure levels without strong evidence and orientation support.

# System status and asynchronous work

## Status model

Distinguish these states when they exist:

1. **Action received** — the product acknowledges input.
2. **Accepted/queued** — durable system acceptance is confirmed.
3. **Running** — work is in progress.
4. **Succeeded** — all intended effects are durably complete.
5. **Partially succeeded** — some items/effects completed and others did not.
6. **Failed** — no or incomplete durable outcome; cause and next action are clear.
7. **Cancelled** — cancellation was accepted and its scope is clear.
8. **Stale/conflicted** — source data changed and the action needs reconciliation.

Do not label `accepted`, `queued`, optimistic, or client-only state as `completed`.

## Feedback timing

- acknowledge interaction immediately at the interface level;
- keep brief operations in context without disruptive overlays;
- for longer operations, name the work and show meaningful progress or milestones when available;
- let users leave and return when work need not block them;
- notify on completion through an appropriate channel when the user cannot reasonably watch;
- provide safe cancellation only when the system can honor it truthfully;
- prevent duplicate action while preserving a controlled retry.

A spinner without an operation name, state, or recovery route is not sufficient for consequential work.

## Optimistic updates

Use only when:

- failure is uncommon and low consequence;
- rollback is fast and comprehensible;
- concurrent changes are handled;
- the UI distinguishes pending from durable state when that distinction matters;
- retries cannot duplicate side effects.

Avoid optimistic success for money movement, permission changes, publication, deletion, or other high-consequence effects unless domain-specific controls make it safe and explicit.

## Partial failure

Show:

- what succeeded;
- what failed or was skipped;
- why, at an actionable level;
- whether successful items will remain committed;
- how to retry only eligible failed items;
- what changed since the original preview;
- how the audit/history records the result.

Never collapse partial failure into a generic success toast.

# Errors, recovery, and interruption

## Error prevention hierarchy

1. Remove the invalid path.
2. Constrain input or action safely.
3. Provide required context before the decision.
4. Validate early enough to help.
5. Preview exact consequences when risk warrants it.
6. Make action idempotent or duplicate-safe.
7. Offer undo, cancellation, compensation, or local correction.
8. Explain and escalate when recovery cannot remain local.

## Error message contract

Every actionable error should identify:

- what failed;
- which item or field is affected;
- why, when known and safe to expose;
- what remains saved or completed;
- what the user can do next;
- whether retry is safe;
- where support/escalation can find the relevant trace or identifier.

Avoid blame, raw stack traces, vague “Something went wrong,” and generic retry when repeated retry can worsen the result.

## Draft, autosave, and resume

Use draft persistence when loss or interruption cost is material.

Specify:

- what is saved and when;
- where it is stored and for how long;
- whether it is shared across devices or actors;
- how conflicts are handled;
- visible save state;
- privacy/security implications;
- how to discard or finalize;
- what happens after schema or policy changes.

Autosave without visible state or conflict handling can reduce trust and create silent overwrite.

## Undo versus confirmation

| Consequence | Preferred treatment |
|---|---|
| Low, local, immediately reversible | Direct action with visible result and undo |
| Moderate, recoverable, cross-record/user | Clear action label, constraints, scope summary, and undo/compensation when truthful |
| High, consequential or hard to reverse | Explicit review of exact objects/effects, specific final action, authorization, and audit |
| Critical/irreversible/regulated | Domain-governed confirmation, review, separation of duties, re-authentication, or approval as required |

Do not add confirmation to every harmless action. Repeated generic confirmation teaches users to dismiss it.

## Destructive action pattern

- Use a specific verb such as `Delete 12 records`, not `OK` or `Confirm`.
- State what will be deleted, what will remain, who is affected, and whether recovery exists.
- Show dependent or blocked items before commit.
- Place destructive action away from routine primary actions without hiding it.
- Do not rely on color alone.
- Use typed confirmation only when it adds meaningful deliberate review; avoid ritual phrases for routine operations.
- After action, show the durable result and recovery/compensation route.

# Permissions, ownership, and handoffs

## Hide, disable, or explain

| Situation | Treatment |
|---|---|
| Action is irrelevant to the actor and revealing it provides no value or may expose sensitive capability | Hide |
| Actor expects the action, can become eligible, or needs to understand why it is unavailable | Show disabled or read-only state with reason and next step |
| Another role must act | Show owner, state, and handoff/request action with preserved context |
| Action is temporarily unavailable due to object/system state | Show state-based reason and what must change |
| Policy cannot be safely disclosed | Provide a safe explanation and support/escalation route |

A disabled control with no explanation is a dead end. A hidden control can make permission boundaries impossible to understand. Choose based on user need and disclosure risk.

## Handoff pattern

A good handoff carries:

- object identity and deep link;
- requester and intended owner;
- reason, requested action, urgency, and due state;
- relevant context without manual copying;
- permission-safe attachments or history;
- accepted/declined/in-progress/completed state;
- notifications and escalation policy;
- an audit trail;
- a return path for the original actor.

Do not use email or free-text copying as the only continuity mechanism when the product owns the workflow.

# Empty, partial, stale, and first-use states

## Empty state

Distinguish:

- true first use;
- no data because of current filters/search;
- no permission;
- data still loading;
- data failed to load;
- all work completed;
- feature not configured.

Each requires a different message and action. An empty illustration with generic encouragement is not a recovery path.

## First use and onboarding

Prefer onboarding inside the real task:

- orient to the object and outcome;
- reveal guidance at the first relevant decision;
- provide sample/demo data only when it cannot be mistaken for real data;
- let users skip nonessential tours;
- avoid blocking setup before value is visible;
- keep help available after dismissal.

Use a setup checklist when tasks are independently completable and progress is durable. Do not turn a linear dependency into a misleading checklist.

## Stale or conflicting state

- identify what changed and by whom/when if appropriate;
- preserve the user's unsaved work;
- show a meaningful diff or conflicting fields;
- let the user refresh, merge, overwrite only when authorized, or abandon;
- prevent silent last-write-wins for consequential data;
- record the resolution.

# Accessibility and constrained-context patterns

Accessibility is part of task completion, not a separate polish phase.

For every candidate, verify:

- semantic role, name, value, and state;
- logical reading and focus order;
- keyboard access and visible focus;
- focus placement/return after errors, dialogs, updates, and route changes;
- text labels for icons, status, errors, and color-coded information;
- target size and spacing appropriate to the platform and applicable standard;
- zoom/reflow and small-viewport behavior without lost functions or context;
- status updates available programmatically without unnecessary focus movement;
- equivalent alternative to drag, hover, complex gesture, or motion-dependent action;
- reduced-motion behavior;
- errors that identify the item and correction in text;
- authentication that does not unnecessarily block password managers, paste, or accessible completion;
- time limits with warning/extension where required;
- preserved values and redundant-entry reduction.

Custom controls must earn their cost. Prefer platform and established design-system semantics when they meet the need.

# Mobile and cross-device continuity

- Prioritize the current task and essential status; do not merely stack a desktop dashboard.
- Keep primary actions reachable without obscuring content or platform controls.
- Avoid hover-only information and tiny icon targets.
- Preserve object identity, draft state, and completion status across device changes when the service promises continuity.
- Design keyboard appearance, input types, scanning, camera/file access, and intermittent connectivity deliberately.
- Make long tables and dense expert tools adapt through column priority, alternate views, or task-specific mobile flows rather than horizontal chaos.
- Do not assume mobile means novice or desktop means expert.

# AI- and agent-assisted patterns

Treat AI as a probabilistic collaborator with explicit authority boundaries, not as decorative autocomplete or an invisible backend detail.

## Automation ladder

Choose the lowest level that delivers value:

| Level | System role | User control | Suitable use |
|---|---|---|---|
| **1. Inform** | Summarize, explain, retrieve, or surface signals | User decides and acts | Ambiguous or high-judgment work |
| **2. Recommend** | Rank or propose options | User selects; alternatives remain available | Repeated decisions with understandable basis |
| **3. Draft** | Prepare content, configuration, query, or action plan | User inspects and edits before commit | Work where generation saves effort but correctness needs review |
| **4. Execute with approval** | Prepare exact bounded side effects | User reviews scope/diff and explicitly approves | Reversible or well-controlled operational actions |
| **5. Bounded automation** | Execute within explicit policy and limits | User monitors, can stop/override, receives exceptions/history | High-volume low-ambiguity work with mature safeguards |

Do not move to a higher level solely because the model can technically call a tool.

## Expectation and calibration

Before reliance, communicate:

- what the system can and cannot do in this context;
- what data and tools it can access;
- whether output is generated, retrieved, or authoritative;
- what requires human judgment or approval;
- likely failure modes at the level needed for safe use.

Avoid anthropomorphic certainty and unsupported claims of understanding.

## Suggestion and draft pattern

- Make generated content clearly editable.
- Preserve the user's original input and source material.
- Show relevant provenance or basis close to the claim/action.
- Separate generated suggestions from authoritative records.
- Provide regenerate/alternate only when it helps; do not create endless option churn.
- Capture corrections in a way that improves the current task without implying model retraining unless true.

## Plan-and-act pattern

Before consequential execution, show:

- intended goal;
- objects and scope;
- planned steps or meaningful diff;
- permissions/tools to be used;
- external side effects;
- assumptions, skipped items, and uncertainty;
- approval boundary;
- stop/cancel and recovery behavior.

During execution, show current step and state without exposing irrelevant internal chain-of-thought. After execution, show durable outcomes, partial failures, exceptions, and history.

## AI failure and recovery

Handle separately:

- unsupported request;
- missing permission/tool/data;
- stale or conflicting source;
- low-confidence/ambiguous input;
- unsafe or policy-blocked action;
- tool timeout or partial failure;
- hallucinated or unverifiable claim;
- user correction or override;
- automation stopped mid-run.

Do not convert all failures into “try again.” Route each to clarification, manual completion, alternate source, escalation, or safe stop as appropriate.

## AI evaluation scorecard

Include task outcomes plus:

- correct-use and correct-rejection rates;
- false completion and undetected wrong output;
- correction/verification effort;
- override, stop, and recovery success;
- provenance use and trust calibration;
- quality by subgroup/task complexity;
- partial-failure transparency;
- time saved among correct completions;
- downstream rework or harm;
- operator workload and alert fatigue for bounded automation.

Acceptance rate is not proof of quality. Speed is not a benefit when review or downstream correction grows.

# Visual hierarchy, density, and content

## Hierarchy

A coherent surface makes these answers obvious:

1. Where am I and what object/state am I seeing?
2. What matters now?
3. What is the likely next action?
4. What alternatives or secondary details exist?
5. What changed after I acted?

Use typography, spacing, grouping, alignment, contrast, and placement before adding containers, icons, color, or motion.

## Primary actions

Use one dominant primary action when the workflow has one. Multiple primary-looking actions are acceptable only when the user truly faces peer outcomes and the consequence is clear.

Action labels should name the result:

- `Send for approval`
- `Save draft`
- `Publish 3 changes`
- `Retry failed 8`

Avoid vague labels such as `Submit`, `Continue`, `Apply`, or `OK` when a more specific result can be named.

## Density

Tune density to frequency and comparison needs:

- more whitespace and explanation for unfamiliar consequential decisions;
- tighter rows, stable alignment, and more visible state for expert scanning;
- responsive adaptation rather than one fixed density;
- user-selectable density only when distinct sustained needs justify the setting.

Sparse is not automatically clear. Dense is not automatically complex. Test task performance and scanability.

## Content reduction

Delete copy that:

- repeats the heading or control label;
- explains obvious UI mechanics instead of the decision;
- exposes implementation details without a user consequence;
- gives generic reassurance unsupported by behavior;
- hides the actual requirement in a paragraph.

Retain copy that clarifies eligibility, required data, consequence, state, recovery, or unfamiliar domain language.

# Anti-patterns

Reject these unless strong evidence and safeguards justify them:

- route/database-shaped navigation;
- dashboard-within-dashboard layouts;
- one card per backend capability;
- nested modal or drawer stacks;
- icon-only critical actions;
- generic `More` menus containing primary work;
- placeholder-only labels;
- destructive action beside a routine primary action with the same visual weight;
- confirmation after every harmless change;
- optimistic success before durable completion;
- spinners with no named operation, status, or recovery;
- clearing valid input after an error;
- invisible default filters;
- duplicated editable settings with unclear ownership;
- bulk actions with ambiguous selection scope;
- disabled actions with no explanation or handoff;
- tutorial overlays that block the real task;
- infinite scroll for position-sensitive operational work without recovery;
- tables forced into unreadable mobile layouts;
- automation that hides assumptions, tools, side effects, or partial failure;
- confidence scores that are not calibrated or actionable;
- visual minimalism achieved through low contrast, missing labels, or hidden state.

# Pattern specification template

Use this for each significant design choice.

```markdown
## Pattern decision — [name]

**Episode and scenario:**
**Root cause:**
**Evidence:**
**Risk tier:**
**Current control value:**
**Selected pattern:**
**Why it fits:**
**Alternatives rejected:**
**Required states:**
**Permission/ownership behavior:**
**Error and recovery behavior:**
**Accessibility behavior:**
**Responsive/cross-device behavior:**
**Analytics:**
**Predicted benefit:**
**New friction introduced:**
**Guardrails:**
**Validation:**
**Stop/revise condition:**
```
