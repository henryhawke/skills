# UX streamlining research brief

Research date: 2026-07-22  
Purpose: evidence base for the canonical Codex skill `/streamline`

## Executive conclusion

`/streamline` should optimize **successful, confident task completion with the least total human effort**, not chase the fewest screens or clicks. ISO treats usability as an outcome of use in a specified context; the core dimensions are effectiveness, efficiency, and satisfaction, not UI compactness in isolation ([ISO 9241-11:2018](https://www.iso.org/standard/63500.html)). Nielsen Norman Group likewise defines interaction cost as the combined mental and physical effort of reading, locating, understanding, clicking, typing, waiting, switching attention, and remembering ([interaction cost](https://www.nngroup.com/articles/interaction-cost-definition/)).

This distinction is decisive. Original UIE/Center Centre clickstream research found that successful and unsuccessful paths had the same click-count distribution, so click count did not predict success ([Testing the Three-Click Rule](https://articles.centercentre.com/three_click_rule/)). Baymard's first-party checkout studies similarly find that the number of fields and perceived effort matter more than the number of steps ([checkout-flow research](https://baymard.com/blog/checkout-flow-average-form-fields)). A clear five-step flow can be easier and safer than a crowded two-step flow.

The skill should produce two things together:

1. an evidence-backed redesign that removes redundant work and makes the next useful action obvious; and
2. a before/after measurement contract that can disprove the redesign.

Synthetic workflow stories are useful **design probes**, not user research. They should make hidden complexity vivid, enumerate hypotheses, and generate test tasks. They must never be presented as evidence about what real users do; GOV.UK explicitly requires continuous research with real users and their end-to-end journeys ([user-research guidance](https://www.gov.uk/service-manual/user-research/how-user-research-improves-service-design)).

## Evidence-derived operating principles

### 1. Start with the whole job, not the current screen

Map the user's trigger, desired outcome, starting information, handoffs, interruptions, offline steps, and confirmation of completion. Do not preserve a cumbersome screen merely because it reflects an organizational or database structure. GOV.UK recommends working end-to-end, front-to-back, and across channels, while avoiding exposure of internal structures to users ([good-service characteristics](https://www.gov.uk/service-manual/design/introduction-designing-government-services)).

The streamlining unit is a **task episode**: intent to verified outcome, including recovery. Local savings that create extra work elsewhere are regressions.

### 2. Minimize total interaction cost, not raw clicks

For every step, inventory:

- decisions and concepts the user must understand;
- text to scan, fields to inspect, data to type, and facts to remember;
- pointer/keyboard actions, scrolling, backtracking, and window/context switches;
- waiting, uncertain system state, help seeking, errors, and rework;
- consequences, reversibility, and confidence checks.

Clicks are one diagnostic component. A click that narrows choices with strong information scent may reduce effort; a single click that exposes a wall of options may increase it. Prefer fewer **meaningless decisions, redundant entries, ambiguous paths, and attention switches** over fewer screens at any cost.

### 3. Make functions findable in the user's language

Navigation labels, action names, settings locations, and grouping should match user concepts and expected task order. NN/g's information-scent model says a user's next choice depends on the label, surrounding context, and prior experience; vague labels such as “More” disclose little about the destination ([information scent](https://www.nngroup.com/articles/information-scent/)). Place task-specific controls near the task rather than in a distant global settings maze; Apple likewise recommends minimizing settings and deriving what the system already knows ([Apple HIG: Settings](https://developer.apple.com/design/human-interface-guidelines/settings)).

Diagnose the right layer before redesigning. Tree testing isolates information architecture; card sorting examines grouping and labels; click testing examines visual prominence; usability testing observes the combined experience. Direct success, indirect success/backtracking, first choice, and time are useful IA measures ([findability testing methods](https://www.nngroup.com/articles/navigation-ia-tests/)). Do not solve a taxonomy problem by merely enlarging a button, or solve a visibility problem by rebuilding the taxonomy.

### 4. Externalize memory; disclose complexity progressively

Keep needed labels, prior choices, current state, requirements, and consequences visible or immediately retrievable. Recognition generally requires less memory work than recall ([recognition versus recall](https://www.nngroup.com/articles/recognition-and-recall/)). Preserve inputs across navigation and errors, show meaningful recent items, and put contextual help beside the decision it supports.

Progressive disclosure is appropriate when advanced or infrequent options would otherwise compete with common work. The primary surface must contain frequently needed actions, and the reveal control must clearly predict what it contains. Usage analytics can suggest the split, but observational testing must validate it; more than two disclosure levels often harms orientation ([progressive disclosure](https://www.nngroup.com/articles/progressive-disclosure/)). Do not bury rare-but-critical safety, permission, recovery, or compliance controls merely because they are infrequent.

### 5. Use defaults carefully, and prefer direct action when it remains safe

Good defaults can remove configuration work, but defaults are not neutral. GOV.UK advises against preselecting answers to questions because users may miss the question or submit the wrong answer; a settings control may have a default when it represents an intentional product configuration rather than a claimed fact or consent ([radios](https://design-system.service.gov.uk/components/radios/), [selects](https://design-system.service.gov.uk/components/select/)). Defaults should be visible, easy to change, based on strong evidence, and safe for the common case.

When appropriate, let users act on visible objects with rapid, incremental, reversible operations and immediate visible results. Those are the defining properties of direct manipulation in Shneiderman's original work ([1983 paper](https://www.cs.umd.edu/users/ben/papers/Shneiderman1983Direct.pdf)). Use inline editing, drag/drop with an equivalent non-drag route, immediate filtering, and undo where they reduce indirection. Keep explicit review for consequential or ambiguous changes.

### 6. Design public forms and expert admin tools for their different contexts

For forms, ask only what is necessary, reuse already supplied information, infer safely, preserve data after validation, and reveal conditional questions only when relevant. WCAG 2.2 requires previously entered information in the same process to be auto-populated or selectable unless an exception applies ([SC 3.3.7 Redundant Entry](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html)). Baymard's research reinforces that visible fields and fields users must consider drive perceived effort more than nominal step count.

“One thing per page” is a strong starting point for unfamiliar public flows because it improves focus, mobile use, analytics, and error recovery, but it is not universal ([GOV.UK form structure](https://www.gov.uk/service-manual/design/form-structure)). Repetitive admin work may need compact comparison, fast switching, bulk actions, saved views, and keyboard accelerators. GOV.UK explicitly notes that internal users who repeat and switch tasks may need to see more information at once; internal systems still require the same accessibility and user-needs standard ([services for government users](https://www.gov.uk/service-manual/design/services-for-government-users)). Test novices and high-frequency experts separately.

### 7. Prevent expensive errors; make recovery local and humane

Prioritize error prevention by consequence, not annoyance. Use constraints, clear units and formats, review-before-commit for high-impact operations, double-submit protection, undo where truthful, and explicit destructive-action labels. Do not add confirmations to every harmless action; habituation and extra work can make indiscriminate confirmation counterproductive.

When an error occurs, identify the affected item in text, preserve valid entries, explain the cause in plain language, suggest a correction, focus/scroll to a useful location, and keep the user in the task. WCAG requires textual error identification and, for legal/financial/data changes, reversibility, checking, or review/confirmation ([WCAG 2.2 input assistance](https://www.w3.org/TR/WCAG22/#input-assistance)). GOV.UK's check-answers pattern is specifically intended to reduce error rates before submission ([check answers](https://design-system.service.gov.uk/patterns/check-answers/)).

### 8. Make every wait and state transition legible

Feedback is part of streamlining: a user who cannot tell whether a click registered may click again, wait unnecessarily, or leave. For web products, measure field performance rather than relying only on lab speed. Google's current Core Web Vitals targets at the 75th percentile are LCP at or below 2.5 seconds, INP at or below 200 ms, and CLS at or below 0.1 ([Web Vitals](https://web.dev/articles/vitals)).

Across platforms, give immediate acknowledgment, name the operation, distinguish queued/running/succeeded/failed, and expose a reliable completion state. For genuinely long work, show determinate progress or meaningful milestones and allow safe cancellation when possible. The classic 0.1/1/10-second thresholds are useful perceptual rules of thumb, not service-level guarantees: roughly immediate, flow-preserving, and attention-breaking respectively ([response-time limits](https://www.nngroup.com/articles/response-times-3-important-limits/)). Status messages must also be programmatically available without unnecessarily moving focus ([WCAG status messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages)).

### 9. Accessibility is a completion requirement, not polish

Streamlining must work with keyboard, screen reader, zoom/reflow, touch, reduced motion, and constrained attention or motor control. WCAG 2.2 requires visible focus, consistent identification/navigation, keyboard operation, error support, and minimum pointer-target sizing of 24 by 24 CSS pixels subject to defined exceptions; 44 by 44 is the enhanced target ([WCAG 2.2](https://www.w3.org/TR/WCAG22/)). Dragging must have a single-pointer alternative when dragging is not essential. Automating or hiding controls is not an improvement if it removes an accessible route or makes state changes unannounced.

### 10. Aesthetic refinement should strengthen hierarchy, not add decoration

Minimalism means removing competition with the primary goal, not making controls faint, unlabeled, or unfamiliar. NN/g's heuristic says every irrelevant unit competes with relevant information ([ten usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)). Apple's current HIG emphasizes hierarchy, harmony, and consistency with platform conventions ([Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines?lang=en)).

Use typography, spacing, grouping, alignment, contrast, and one clear primary action to encode importance. Reuse the product's design system and platform patterns. A visually sparse screen with weak affordances is not streamlined; a dense expert dashboard with disciplined grouping may be. Because visual appeal can improve *perceived* usability even when behavior has not improved, measure perceived craft separately from task performance ([Tractinsky et al.](https://doi.org/10.1016/S0953-5438(00)00031-X)).

## Universal guardrails versus context-dependent choices

| Treat as a standing guardrail | Treat as a hypothesis to test in context |
|---|---|
| Visible system status and completion state | One page versus a multi-step flow |
| User language, consistent labels, and strong information scent | Which functions deserve first-level visibility |
| Recognition over unnecessary recall | Progressive-disclosure split and number of visible controls |
| Preserve work; prevent and recover from errors | Autosave, optimistic UI, and automatic application of changes |
| Reversible exits and explicit consequential actions | Defaults, personalization, recommendations, and automation |
| Keyboard/AT operation and WCAG-conformant semantics | Cards versus tables; modal versus inline editing |
| A clear hierarchy and one dominant next action where one exists | Density, bulk actions, shortcuts, and saved views for experts |
| Measure end-to-end outcomes with real users | Exact step, field, and click-count targets |

Safety, security, legal review, consent, permissions, audit trails, and necessary confirmation are not “fat.” Streamline their presentation and data reuse, but do not remove their control purpose.

## Synthetic workflow method for `/streamline`

Synthetic stories should create a precise mental simulation from repository/runtime evidence, then expose uncertainty. For each important workflow, generate at least these lenses:

1. first-time or infrequent user;
2. high-frequency expert/admin repeating the task at scale;
3. interrupted user returning with partial work;
4. keyboard/screen-reader or zoomed/mobile user;
5. slow-network or degraded-response user;
6. exception path: invalid data, permission denial, partial failure, stale state, or risky/destructive action.

Use this story contract:

```text
Actor and context: role, proficiency, frequency, device/input, environment, constraints
Trigger: what happened immediately before opening the product
Goal and success state: the observable outcome, including confirmation
Starting state/data: what is known, selected, dirty, stale, or missing
Current episode: exact screens/actions/decisions/waits from intent to outcome
Friction ledger: for each beat, locate/interpret/decide/type/remember/wait/recover
Failure branch: likely slip or system failure, consequence, and recovery path
Streamlined episode: proposed path with preserved safeguards
Predicted delta: counts and timings, explicitly labeled hypothesis
Unknowns: facts that require analytics, user research, or runtime proof
```

At each beat, perform a cognitive walkthrough: will the actor pursue the right goal, notice the correct action, connect it to the outcome, and understand the resulting feedback? This discipline is documented in AHRQ's original workflow-assessment toolkit ([cognitive walkthrough](https://digital.ahrq.gov/health-it-tools-and-resources/evaluation-resources/workflow-assessment-health-it-toolkit/all-workflow-tools/cognitive-walkthrough)).

Tag every story detail as **verified**, **inferred**, or **unknown**. Do not invent preferences, frequency, or business rules. The stories should end as realistic benchmark tasks with a clear correct result. GOV.UK recommends believable, representative, stable tasks and measuring success, time, abandonment/false confidence, ease, and confidence ([usability benchmarking](https://www.gov.uk/service-manual/measuring-success/usability-benchmarking-a-website-or-whole-service)).

## Before/after measurement contract

Capture a baseline before recommending changes. Report by workflow and user segment; do not hide a severe regression inside a single composite “UX score.”

| Outcome | Measure | Interpretation |
|---|---|---|
| Correct completion | Unassisted correct completions / attempts | Primary effectiveness measure; define the end state before testing |
| Safe completion | Correct completions with no critical error / attempts | Required for consequential admin, money, permission, or destructive work |
| Efficiency | Median and P75/P90 time on task among successful attempts | Compare equivalent users, tasks, devices, and data volumes |
| Effort profile | Required decisions, fields, keystrokes, pointer actions, waits, context switches, backtracks, recall dependencies | A vector, not one magic number; weight observed pain and accessibility barriers |
| Findability | Direct tree-test success, indirect success, first choice, time to target | Separates IA/label issues from visual prominence issues |
| Errors and recovery | Error rate, correction attempts, recovery success, recovery time, lost-work incidents | Classify by severity and user/system cause |
| Flow health | Start-to-finish completion, abandonment by step, help/contact rate, repeated submission | Diagnose where a live journey breaks; GOV.UK defines completion against explicit start/end points ([completion rate](https://www.gov.uk/service-manual/measuring-success/measuring-completion-rate)) |
| Confidence/satisfaction | Post-task ease, confidence, expected-versus-actual time; consistent rating scale | Pair self-report with observed success; false confidence is a serious finding |
| Workload | Mental, physical, and temporal demand; effort, frustration, perceived performance | For complex workflows, compare with NASA-TLX rather than treating click count as cognitive load ([NASA-TLX](https://www.nasa.gov/human-systems-integration-division/nasa-task-load-index-tlx/)) |
| Accessibility | Critical-task completion by keyboard and representative AT; WCAG 2.2 checks | Automated findings supplement, never replace, task testing |
| Responsiveness | P75 field LCP/INP/CLS for web; operation acknowledgment and completion latency | Segment mobile/desktop and key workflows; do not report only averages |
| Frequency-weighted benefit | Workflow frequency × median successful time saved | Estimate system value without letting rare cosmetic savings outrank common blockers |

Each recommendation should include:

- baseline and proposed flow diagrams or beat lists;
- friction removed, friction moved, and safeguards retained;
- predicted metric direction and numeric target/range where evidence permits;
- evidence grade: runtime/repository fact, analytics, user research, external heuristic, or synthetic hypothesis;
- reach, severity, confidence, implementation cost, and regression risks;
- validation method and stop/revert condition.

Good targets are task-specific: for example, “raise unassisted completion from 68% to at least 85% without increasing critical errors,” or “reduce median successful admin-review time by 25% while preserving keyboard completion.” “Reduce clicks by 40%” is useful only as a secondary mechanical observation and is never sufficient acceptance evidence.

## Recommended shape of the skill output

1. **Scope and evidence boundary** — product surface, inspected evidence, unknowns, user segments.
2. **Workflow map** — highest-value jobs and their start/end states.
3. **Friction ledger** — severity-ranked locate/understand/decide/type/wait/recover costs.
4. **Synthetic stories** — current and streamlined episodes, including expert, interrupted, accessible, degraded, and failure paths.
5. **Recommendations** — remove, combine, relocate, rename, default, prefill, reveal, accelerate, or automate; retain safeguards explicitly.
6. **Before/after scorecard** — baseline, hypothesis, target, validation, and no-regression checks.
7. **Implementation sequence** — reversible, high-confidence changes first; riskier structural changes behind prototypes or experiments.

The skill should refuse to call a redesign “intuitive,” “simpler,” or “better” solely from heuristic inspection. It can call it a stronger hypothesis, then say what evidence would confirm or falsify it.

