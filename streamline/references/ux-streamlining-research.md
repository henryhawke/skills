# UX streamlining evidence and standards playbook

Use this reference to justify decisions, resolve conflicting heuristics, select a validation method, and keep the skill aligned with current authoritative guidance. It is an operating reference, not evidence that any specific product or user population behaves a certain way.

**Source set reviewed through:** 2026-07-22

## Contents

- [How to use evidence](#how-to-use-evidence)
- [Decision authority](#decision-authority)
- [Standing operating rules](#standing-operating-rules)
- [Context-dependent choices](#context-dependent-choices)
- [Measurement and method map](#measurement-and-method-map)
- [Accessibility requirements map](#accessibility-requirements-map)
- [AI and automation requirements map](#ai-and-automation-requirements-map)
- [Reliability and release requirements map](#reliability-and-release-requirements-map)
- [Source index](#source-index)
- [Maintenance rules](#maintenance-rules)

# How to use evidence

## Match evidence to the question

| Question | Strongest useful evidence | Supporting evidence | Do not substitute |
|---|---|---|---|
| What actually happens in this product? | Production instrumentation, direct observation, runtime/repository trace | Support cases and stakeholder reports | External heuristics |
| Why does it happen? | Task observation, contextual inquiry, interviews paired with behavior | Cognitive walkthrough and support evidence | Event sequence alone |
| How often and for whom? | Defined production denominator and segments | Repeated support/research samples | One anecdote or synthetic persona |
| Is the experience accessible? | Applicable standard plus keyboard/representative AT task testing | Automated checks and platform guidance | Visual inspection alone |
| Is the change safe or allowed? | Law/policy/domain/security/privacy owner and authoritative system contract | Failure analysis and standards | UX preference or opportunity score |
| Which pattern is a strong starting point? | Direct user evidence and established design system | External research and platform guidance | Trend or personal taste |
| Did the candidate cause improvement? | Controlled experiment or defensible matched comparison | Repeated benchmark task evidence | Before/after screenshots or click counts |
| Is workload lower? | Task outcomes plus appropriate workload measure | Effort-vector counts | Click count as cognitive load |
| Is an AI/automation level appropriate? | Task risk, authority, quality evaluation, exception data, and human-control testing | Human-AI guidelines and risk frameworks | Model capability demo or acceptance rate |
| Is a production rollout safe? | Compatibility tests, staged release, monitoring, rollback/compensation | SRE and resilience guidance | Local happy-path pass |

## Evidence-label rule

Use the labels defined in [workflow-lab.md](workflow-lab.md#evidence-rules).

External sources support general statements such as:

> Preserving previously entered information reduces redundant entry.

They do not support local claims such as:

> Users abandon this form because the address is repeated.

The latter requires product evidence and must otherwise be labeled a hypothesis.

## Claim-strength rule

| Wording | Use when |
|---|---|
| **Must / required** | Applicable law, policy, standard/conformance target, security/privacy rule, or explicit product contract requires it |
| **Should / strong default** | Multiple strong sources support the principle and local risk does not conflict |
| **Prefer / consider** | Pattern commonly reduces the diagnosed cost but context can reverse it |
| **Hypothesis / predict** | Effect has not been measured locally |
| **Unknown** | Evidence is absent, ambiguous, stale, or inaccessible |

Do not turn a reputable company's design convention into a universal requirement.

# Decision authority

When sources conflict, resolve in this order:

1. **Safety, law, consent, security, privacy, and binding product policy.**
2. **Authoritative domain and source-of-truth constraints.**
3. **Correct and accessible task completion in the real context of use.**
4. **Direct product evidence: instrumented and observed behavior.**
5. **Applicable standards and platform conventions.**
6. **External research and mature design-system guidance.**
7. **Heuristics and synthetic scenario predictions.**
8. **Aesthetic preference.**

This is not a simple evidence-quality ranking. Each source answers a different question. Instrumentation can reveal scale but not motive; observation can reveal cause but not prevalence; standards define requirements but do not choose every layout.

# Standing operating rules

Treat these as defaults unless a higher authority or context-specific result overrides them.

## 1. Optimize the complete outcome in context

**Operational requirement**

- Define actor, goal, context, start, verified end, errors, recovery, and re-entry.
- Include cross-channel and human/system handoffs.
- Measure effectiveness, efficiency, and confidence/satisfaction in the specified context.
- Do not expose organizational or technical structure as the service model unless users actually think and work that way.

**Primary references**

- [ISO 9241-11:2018 — Usability: Definitions and concepts](https://www.iso.org/standard/63500.html)
- [ISO 9241-210:2019 — Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)
- [ISO 9241-110:2020 — Interaction principles](https://www.iso.org/standard/75258.html)
- [ISO 9241-115:2024 — Conceptual, interaction, interface, and navigation design](https://www.iso.org/standard/80773.html)
- [GOV.UK — What good services look like](https://www.gov.uk/service-manual/design/introduction-designing-government-services)

## 2. Minimize total interaction cost, not raw clicks

**Operational requirement**

Count and reduce unnecessary finding, reading, interpreting, deciding, remembering, entering, navigating, waiting, switching, coordinating, recovering, and verifying. A useful click that narrows choices or preserves context can reduce total effort; a one-click action with hidden consequence can increase it.

Treat screen, field, and click counts as diagnostic components only. Keep task success and critical errors primary.

**Primary references**

- [Nielsen Norman Group — Interaction cost](https://www.nngroup.com/articles/interaction-cost-definition/)
- [Center Centre/UIE — Testing the Three-Click Rule](https://articles.centercentre.com/three_click_rule/)
- [Baymard — Checkout fields and perceived effort](https://baymard.com/blog/checkout-flow-average-form-fields)

## 3. Make functions findable in user language

**Operational requirement**

- Name destinations and actions by object, outcome, or task stage.
- Put task-specific controls at the point of use.
- Use stable global settings only for genuinely global policy/preferences.
- Diagnose taxonomy separately from visual prominence.
- Prefer predictive labels over generic `More`, icon-only, or internal terms.

**Primary references**

- [Nielsen Norman Group — Information scent](https://www.nngroup.com/articles/information-scent/)
- [Nielsen Norman Group — Navigation and IA testing methods](https://www.nngroup.com/articles/navigation-ia-tests/)
- [GOV.UK — Naming your service](https://www.gov.uk/service-manual/design/naming-your-service)
- [Apple Human Interface Guidelines — Settings](https://developer.apple.com/design/human-interface-guidelines/settings)

## 4. Externalize memory and preserve state

**Operational requirement**

- Keep needed labels, requirements, prior choices, owner, status, and consequences visible or immediately retrievable.
- Retain valid information through errors and navigation.
- Reuse or make selectable information already supplied in the same process unless an exception applies.
- Preserve object identity and return context across surfaces.

**Primary references**

- [Nielsen Norman Group — Recognition rather than recall](https://www.nngroup.com/articles/recognition-and-recall/)
- [WCAG 2.2 Understanding SC 3.3.7 — Redundant Entry](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html)

## 5. Ask only necessary questions and handle defaults carefully

**Operational requirement**

- Every field must support a current decision, operation, or binding requirement.
- Reuse known data and reveal conditional questions only when relevant.
- Explain unusual requests at the field.
- Use defaults for safe product configuration or stable low-risk preference.
- Do not preselect factual claims, eligibility, declarations, or consent that require deliberate user assertion.
- Provide a manual fallback for lookup, autocomplete, or derivation failure.

**Primary references**

- [GOV.UK — Form structure](https://www.gov.uk/service-manual/design/form-structure)
- [GOV.UK Design System — Radios](https://design-system.service.gov.uk/components/radios/)
- [GOV.UK Design System — Selects](https://design-system.service.gov.uk/components/select/)
- [Baymard — Explain why a required phone number is needed](https://baymard.com/blog/explain-phone-number-field)
- [Baymard — Postal-code auto-detection with fallback](https://baymard.com/blog/zip-code-auto-detection)
- [WCAG 2.2 Understanding SC 3.3.7 — Redundant Entry](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html)

## 6. Design public/infrequent and expert/repetitive work differently

**Operational requirement**

- In unfamiliar flows, bias toward focus, task order, clear requirements, local errors, and review where consequential.
- In expert operations, bias toward comparison, stable density, saved views, batch work, shortcuts, and interruption recovery.
- Test the segments separately when their frequency, data volume, or information needs differ.
- Keep accessibility and equivalent outcomes constant across both.

**Primary references**

- [GOV.UK — Form structure and one thing per page](https://www.gov.uk/service-manual/design/form-structure)
- [GOV.UK — Designing services for government users](https://www.gov.uk/service-manual/design/services-for-government-users)

## 7. Prevent expensive errors and make recovery local

**Operational requirement**

- Prioritize prevention by consequence.
- Use constraints, clear requirements, duplicate protection, review, and idempotency as appropriate.
- Preserve valid data after an error.
- Identify the affected field/item in text, explain the correction, and keep the user in context.
- For consequential submissions, provide reversal, checking, or review/confirmation as required.
- Prefer undo over ritual confirmation for low-risk reversible actions.

**Primary references**

- [WCAG 2.2 — Input Assistance](https://www.w3.org/TR/WCAG22/#input-assistance)
- [GOV.UK Design System — Validation](https://design-system.service.gov.uk/patterns/validation/)
- [GOV.UK Design System — Error message](https://design-system.service.gov.uk/components/error-message/)
- [GOV.UK Design System — Error summary](https://design-system.service.gov.uk/components/error-summary/)
- [GOV.UK Design System — Check answers](https://design-system.service.gov.uk/patterns/check-answers/)
- [GOV.UK Design System — Buttons and warning/destructive actions](https://design-system.service.gov.uk/components/button/)

## 8. Make waits and state transitions legible

**Operational requirement**

- Acknowledge actions immediately at the interface level.
- Distinguish attempted, accepted/queued, running, succeeded, partially succeeded, failed, cancelled, and stale states when applicable.
- Show durable completion, not optimistic or client-only state, for consequential effects.
- Provide meaningful progress or milestones for long work and safe cancellation when truthful.
- Make status available programmatically without unnecessary focus movement.
- Measure field and operation latency as distributions, not only averages.

**Primary references**

- [Nielsen Norman Group — Visibility of system status](https://www.nngroup.com/articles/visibility-system-status/)
- [Nielsen Norman Group — Response-time limits](https://www.nngroup.com/articles/response-times-3-important-limits/)
- [WCAG 2.2 Understanding SC 4.1.3 — Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)
- [Google — Web Vitals](https://web.dev/articles/vitals)
- [Google — Interaction to Next Paint](https://web.dev/articles/inp)
- [Google — RAIL performance model](https://web.dev/articles/rail)
- [Apple Human Interface Guidelines — Progress indicators](https://developer.apple.com/design/human-interface-guidelines/progress-indicators)

For web field performance, the current widely used “good” thresholds at the 75th percentile are LCP at or below 2.5 seconds, INP at or below 200 milliseconds, and CLS at or below 0.1. Treat these as quality guardrails, not proof of task success.

## 9. Accessibility is a completion requirement

**Operational requirement**

- Design and validate keyboard, focus, semantics, status, error support, reflow/zoom, touch targets, reduced motion, and equivalent alternatives.
- Do not require dragging, hover, or precise gestures when an equivalent route is feasible.
- Do not hide or automate away the accessible route.
- Use automated tools as support; validate critical task completion with representative input and assistive technology.
- Apply platform and organizational requirements in addition to WCAG where relevant.

**Primary references**

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [W3C — Guidance on applying WCAG 2.2 to mobile applications](https://www.w3.org/TR/wcag2mobile-22/)
- [W3C — Guidance on applying WCAG 2.2 to non-web software](https://www.w3.org/TR/wcag2ict-22/)
- [ISO 9241-171:2025 — Software accessibility](https://www.iso.org/standard/86308.html)
- [ISO 9241-161:2025 — Visual user-interface elements](https://www.iso.org/standard/85790.html)

## 10. Visual refinement must strengthen hierarchy

**Operational requirement**

- Use typography, spacing, grouping, alignment, contrast, and placement to express importance.
- Reuse platform and design-system conventions.
- Remove ornament and duplicate explanation before reducing labels, contrast, or affordance.
- Tune density to task frequency and comparison needs.
- Measure perceived ease/craft separately from correct task performance.

**Primary references**

- [Nielsen Norman Group — Aesthetic and minimalist design](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines)
- [ISO 9241-161:2025 — Visual user-interface elements](https://www.iso.org/standard/85790.html)
- [Tractinsky, Katz, and Ikar — What is beautiful is usable](https://doi.org/10.1016/S0953-5438(00)00031-X)

Aesthetic appeal can influence perceived usability. It does not replace task evidence.

## 11. Human-centred work is iterative and evidence-driven

**Operational requirement**

- Involve representative users or operators throughout design when feasible.
- Use synthetic scenarios to expose hypotheses, not replace research.
- Evaluate designs against explicit tasks and context.
- Iterate based on evidence and preserve a decision history.
- Assess organizational HCD capability when streamlining is systemic, not a one-off screen change.

**Primary references**

- [ISO 9241-210:2019 — Human-centred design](https://www.iso.org/standard/77520.html)
- [ISO 9241-222:2026 — Self-assessment of human-centred design approach](https://www.iso.org/standard/88373.html)
- [GOV.UK — How user research improves service design](https://www.gov.uk/service-manual/user-research/how-user-research-improves-service-design)

# Context-dependent choices

Treat these as hypotheses. Select using the task episode, risk, frequency, evidence, and validation method.

| Choice | Prefer option A when | Prefer option B when | Required test/guardrail |
|---|---|---|---|
| One page vs sequential flow | Users compare independent fields, experts scan/edit repeatedly, content is manageable | Questions depend on prior answers, task is unfamiliar, focus/recovery benefits | Same-task success, time, error, mobile/AT completion |
| Inline edit vs dedicated page | Change is local, small, frequent, reversible, and context matters | Work is complex, linkable, resumable, or high consequence | Validation, focus, interruption, deep link, review |
| Modal vs page/drawer | Decision is bounded and must be resolved before continuing | User needs comparison, long work, navigation, or resumption | Focus/keyboard, responsive behavior, no nested layers |
| Table vs cards | Comparison across consistent attributes and bulk work dominate | Items are heterogeneous and comparison is secondary | Scan task, responsive/AT behavior, density |
| Progressive disclosure vs always visible | Advanced/infrequent controls compete with common work | Hidden item is frequent, safety-critical, or needed for comparison | Discovery rate, first action, orientation, no critical hidden control |
| Default vs explicit choice | Default is safe, visible, easy to change, and based on reliable context | Answer is a factual claim, consent, eligibility, or high-consequence scope | Wrong-default rate and correction cost |
| Autosave vs explicit save | Work is long/interruption-prone and conflicts/privacy are handled | Commit has consequential side effects or users need an explicit boundary | Save-state visibility, conflict, recovery, accidental commit |
| Optimistic vs confirmed update | Failure is rare, low-risk, reversible, and reconcilable | Money, deletion, permission, publication, or uncertain server result | Duplicate/rollback/stale tests; no false completion |
| Confirmation vs undo | Action is hard to reverse or requires deliberate consequence review | Action is low-risk and immediately reversible | Critical-error and habituation risk |
| Bulk vs one-at-a-time | Operation is truly repetitive and per-item policy is consistent | Cases need judgment or mixed eligibility is hard to explain | Scope/preview, partial failure, idempotency, audit |
| Sparse vs dense | Task is unfamiliar and explanation/focus dominate | Expert comparison, scanning, and throughput dominate | Segment-specific success, scan time, accessibility |
| Personalization vs stable defaults | Repeated use and reliable preference evidence justify variation | Predictability, shared work, support, or safety requires consistency | Discoverability, reset, shared-state effects, subgroup quality |
| AI suggestion vs execution | Ambiguity, consequence, or quality requires human judgment | Task is bounded, authorized, observable, recoverable, and quality is adequate | Correct-use/rejection, correction cost, partial failure, stop/override |

## Progressive-disclosure adjudication

Use analytics to identify candidate frequency splits, but use observation or task testing to determine whether users understand and find the reveal. Avoid deep disclosure chains; hidden safety, permission, recovery, and status controls require especially strong justification.

Reference: [Nielsen Norman Group — Progressive disclosure](https://www.nngroup.com/articles/progressive-disclosure/)

## Direct-manipulation adjudication

Prefer visible, incremental, reversible action with immediate feedback when the object and consequence are clear. Preserve non-drag and keyboard alternatives. Keep explicit review for ambiguous or consequential changes.

Reference: [Shneiderman — Direct Manipulation: A Step Beyond Programming Languages](https://www.cs.umd.edu/users/ben/papers/Shneiderman1983Direct.pdf)

# Measurement and method map

## End-to-end benchmarking

Use believable, representative, stable tasks with an objectively correct outcome. Record success, critical errors, time, abandonment, false confidence, ease, and confidence. Keep population, task wording, data, and environment comparable.

- [GOV.UK — Usability benchmarking](https://www.gov.uk/service-manual/measuring-success/usability-benchmarking-a-website-or-whole-service)
- [GOV.UK — Measuring completion rate](https://www.gov.uk/service-manual/measuring-success/measuring-completion-rate)

## Cognitive walkthrough

Use to predict whether a specified actor can form the right goal, notice the action, connect it to the outcome, and understand feedback. Treat results as heuristic/observed evidence depending on whether a runnable product is inspected—not as population research.

- [AHRQ — Cognitive walkthrough](https://digital.ahrq.gov/health-it-tools-and-resources/evaluation-resources/workflow-assessment-health-it-toolkit/all-workflow-tools/cognitive-walkthrough)

## Information-architecture testing

- **Card sorting** explores grouping and language.
- **Tree testing** isolates hierarchy/labels without visual design.
- **First-click/click testing** examines visible prominence and interpretation.
- **Usability testing** evaluates the combined end-to-end experience.

- [Nielsen Norman Group — Navigation and IA tests](https://www.nngroup.com/articles/navigation-ia-tests/)

## Workload

For complex workflows, pair task outcomes with a validated workload instrument when the decision needs mental, physical, temporal, performance, effort, and frustration evidence.

- [NASA — NASA Task Load Index](https://www.nasa.gov/human-systems-integration-division/nasa-task-load-index-tlx/)

Do not label a local weighted click/decision score as validated cognitive load.

## Failure analysis

Use a lightweight failure-mode analysis for high-consequence or hard-to-detect errors. Keep severity, likelihood evidence, detectability, controls, and recovery visible; do not let a single composite score override critical risk.

- [Institute for Healthcare Improvement — Failure Modes and Effects Analysis tool](https://www.ihi.org/library/tools/failure-modes-and-effects-analysis-fmea-tool)

## Controlled experiments

Define the primary metric, guardrails, eligibility, assignment, instrumentation, segments, stop conditions, and interpretation before exposure. Validate metric semantics and avoid changing the task denominator during comparison.

- [Microsoft Experimentation Platform — Safe velocity](https://exp-platform.com/Documents/2019%20TongXiaSumitBhardwajPavelDmitrievAleksanderFabijan_Safe-Velocity-ICSE-SEI.pdf)
- [Microsoft Experimentation Platform — Metric interpretation pitfalls](https://exp-platform.com/Documents/2017-08%20KDDMetricInterpretationPitfalls.pdf)

# Accessibility requirements map

Use the applicable WCAG conformance target and organizational/platform rules. The following are especially relevant to streamlining.

| Streamlining concern | Requirement/reference | Operational implication |
|---|---|---|
| Preserve/reuse data | [SC 3.3.7 Redundant Entry](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html) | Previously supplied information in the same process should be auto-populated or selectable unless an exception applies |
| Programmatic status | [SC 4.1.3 Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html) | Announce result/progress/errors without moving focus unnecessarily |
| Target size | [SC 2.5.8 Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum) | Provide at least the required target area/spacing or meet a defined exception; do not shrink critical controls for visual minimalism |
| Drag alternatives | [SC 2.5.7 Dragging Movements](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html) | Provide a single-pointer alternative unless dragging is essential |
| Focus visibility | [WCAG 2.2 Focus Appearance/Not Obscured criteria](https://www.w3.org/TR/WCAG22/#keyboard-accessible) | Sticky layers, dialogs, and route changes must not hide or lose focus |
| Errors and high-consequence input | [WCAG 2.2 Input Assistance](https://www.w3.org/TR/WCAG22/#input-assistance) | Identify errors in text and provide checking/reversal/confirmation where criteria apply |
| Authentication | [SC 3.3.8 Accessible Authentication (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html) | Avoid unnecessary cognitive-function tests and preserve password-manager/paste-compatible routes where applicable |
| Mobile application application | [WCAG2Mobile 2.2](https://www.w3.org/TR/wcag2mobile-22/) | Apply WCAG principles to native and hybrid mobile contexts |
| Non-web software application | [WCAG2ICT 2.2](https://www.w3.org/TR/wcag2ict-22/) | Apply relevant success criteria to non-web software/documents |

The WCAG minimum pointer target in SC 2.5.8 is 24 by 24 CSS pixels subject to defined exceptions; the enhanced target in SC 2.5.5 is 44 by 44 CSS pixels. Product/platform standards may require larger targets.

# AI and automation requirements map

## Human-AI interaction lifecycle

Apply guidance across first use, normal use, failure, correction, and changing system behavior.

| Lifecycle moment | Required behavior |
|---|---|
| Before use | Set accurate expectations for capability, limits, data, tools, authority, and likely failure |
| During recommendation | Make basis/provenance and uncertainty useful at the decision point; preserve alternatives |
| Before action | Show goal, scope, affected objects, side effects, assumptions, and approval boundary |
| During action | Show meaningful progress/state; allow stop or override where safe |
| After action | Show durable results, partial failure, exceptions, history, and recovery |
| After correction | Let users edit/reject/override; do not imply learning or memory unless it actually occurs |
| Over time | Monitor subgroup quality, drift, calibration, exception burden, and automation bias |

**Primary references**

- [Microsoft — Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/)
- [Microsoft — Designing loops, not paths](https://microsoft.design/articles/designing-loops-not-paths/)
- [Microsoft Research — Human-agent interaction challenges](https://www.microsoft.com/en-us/research/publication/human-agent-interaction-challenges/)
- [Google PAIR Guidebook](https://pair.withgoogle.com/guidebook/)
- [Google PAIR — Explainability and trust](https://pair.withgoogle.com/chapter/explainability-trust/)
- [Google PAIR — Feedback and control](https://pair.withgoogle.com/chapter/feedback-controls/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/)

## AI evidence rule

Do not use model benchmark capability alone to justify workflow automation. Evaluate:

- task-specific quality and critical-error taxonomy;
- representative data and edge cases;
- correct acceptance and correct rejection;
- human verification/correction effort;
- provenance and uncertainty comprehension;
- tool/permission failure and partial action;
- stop, override, rollback, and audit;
- subgroup and complexity variation;
- downstream rework/harm;
- operational monitoring and exception load.

## Authority rule

Separate these states in UI and implementation:

```text
suggested -> drafted -> reviewed -> approved -> executing -> durably completed
```

A user request to “streamline” does not authorize the system to cross permission, consent, publication, financial, deletion, or external side-effect boundaries automatically.

# Reliability and release requirements map

Streamlining can increase risk when a shorter path triggers external effects faster. Apply resilient distributed-system practices where the episode crosses services, queues, retries, or side effects.

## Required engineering behaviors

| Concern | Operational requirement | Reference |
|---|---|---|
| Retry safety | Classify transient/permanent/unknown-result failures; use bounded retry, backoff/jitter where appropriate; reconcile before repeating unknown outcomes | [AWS Builders' Library — Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) |
| Idempotency | Give repeated requests a stable identity and ensure they do not duplicate side effects | [Google Cloud — Idempotency](https://cloud.google.com/discover/idempotency) |
| Staged rollout | Start with limited exposure, monitor primary and guardrail outcomes, halt on regression | [Google SRE Workbook — Canarying releases](https://sre.google/workbook/canarying-releases/) |
| Rollback-first design | Make rollback/compensation and operational ownership explicit before broad release | [Google SRE Book — Service best practices](https://sre.google/sre-book/service-best-practices/) |
| Feature-flag portability | Use a governed, vendor-neutral abstraction when appropriate; own lifecycle and cleanup | [OpenFeature](https://openfeature.dev/) |
| Authentication UX and security | Support usable, phishing-resistant, password-manager-compatible authentication according to current policy; do not weaken security to remove steps | [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html) and [Authenticator requirements](https://pages.nist.gov/800-63-4/sp800-63b/authenticators/) |

## Release proof rule

A local pass proves only the local check. Distinguish:

- code/static correctness;
- test-environment workflow behavior;
- staged production technical health;
- real-world task outcome;
- human usability improvement.

Each requires different evidence.

# Source index

Use primary and authoritative sources first. Mature design systems and specialist research are pattern evidence, not binding standards unless adopted by the product.

## International standards

- [ISO 9241-11:2018 — Usability: Definitions and concepts](https://www.iso.org/standard/63500.html)
- [ISO 9241-210:2019 — Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)
- [ISO 9241-110:2020 — Interaction principles](https://www.iso.org/standard/75258.html)
- [ISO 9241-115:2024 — Conceptual, interaction, interface, and navigation design](https://www.iso.org/standard/80773.html)
- [ISO 9241-161:2025 — Visual user-interface elements](https://www.iso.org/standard/85790.html)
- [ISO 9241-171:2025 — Software accessibility](https://www.iso.org/standard/86308.html)
- [ISO 9241-222:2026 — Self-assessment of human-centred design approach](https://www.iso.org/standard/88373.html)

## W3C accessibility

- [Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/)
- [WCAG2Mobile 2.2](https://www.w3.org/TR/wcag2mobile-22/)
- [WCAG2ICT 2.2](https://www.w3.org/TR/wcag2ict-22/)
- [Understanding Redundant Entry](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html)
- [Understanding Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)
- [Understanding Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum)
- [Understanding Accessible Authentication (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html)

## Public-service design and measurement

- [GOV.UK — What good services look like](https://www.gov.uk/service-manual/design/introduction-designing-government-services)
- [GOV.UK — How user research improves service design](https://www.gov.uk/service-manual/user-research/how-user-research-improves-service-design)
- [GOV.UK — Form structure](https://www.gov.uk/service-manual/design/form-structure)
- [GOV.UK — Services for government users](https://www.gov.uk/service-manual/design/services-for-government-users)
- [GOV.UK — Usability benchmarking](https://www.gov.uk/service-manual/measuring-success/usability-benchmarking-a-website-or-whole-service)
- [GOV.UK — Measuring completion rate](https://www.gov.uk/service-manual/measuring-success/measuring-completion-rate)
- [GOV.UK Design System](https://design-system.service.gov.uk/)

## Human factors and UX research

- [Nielsen Norman Group — Interaction cost](https://www.nngroup.com/articles/interaction-cost-definition/)
- [Nielsen Norman Group — Information scent](https://www.nngroup.com/articles/information-scent/)
- [Nielsen Norman Group — Recognition and recall](https://www.nngroup.com/articles/recognition-and-recall/)
- [Nielsen Norman Group — Progressive disclosure](https://www.nngroup.com/articles/progressive-disclosure/)
- [Nielsen Norman Group — System status](https://www.nngroup.com/articles/visibility-system-status/)
- [Nielsen Norman Group — Response times](https://www.nngroup.com/articles/response-times-3-important-limits/)
- [Center Centre/UIE — Three-click rule study](https://articles.centercentre.com/three_click_rule/)
- [NASA — Task Load Index](https://www.nasa.gov/human-systems-integration-division/nasa-task-load-index-tlx/)
- [AHRQ — Cognitive walkthrough](https://digital.ahrq.gov/health-it-tools-and-resources/evaluation-resources/workflow-assessment-health-it-toolkit/all-workflow-tools/cognitive-walkthrough)
- [Shneiderman — Direct manipulation](https://www.cs.umd.edu/users/ben/papers/Shneiderman1983Direct.pdf)

## Forms and commerce research

- [Baymard — Checkout fields and perceived effort](https://baymard.com/blog/checkout-flow-average-form-fields)
- [Baymard — Explain required phone fields](https://baymard.com/blog/explain-phone-number-field)
- [Baymard — Postal-code auto-detection and fallback](https://baymard.com/blog/zip-code-auto-detection)

## Platform and design-system guidance

- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines)
- [Apple — Settings](https://developer.apple.com/design/human-interface-guidelines/settings)
- [Apple — Progress indicators](https://developer.apple.com/design/human-interface-guidelines/progress-indicators)
- [Apple — Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)
- [Atlassian Design System — Modal dialog](https://atlassian.design/components/modal-dialog)
- [Atlassian Design System — Dynamic table](https://atlassian.design/components/dynamic-table)
- [Atlassian Design System — Empty state](https://atlassian.design/components/empty-state)
- [Atlassian Design System — Inline edit](https://atlassian.design/components/inline-edit/inline-editable-textfield)
- [Google — Web Vitals](https://web.dev/articles/vitals)
- [Google — RAIL](https://web.dev/articles/rail)

## AI and risk

- [Microsoft — Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/)
- [Microsoft — Designing loops, not paths](https://microsoft.design/articles/designing-loops-not-paths/)
- [Google PAIR Guidebook](https://pair.withgoogle.com/guidebook/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/)

## Engineering, experimentation, and release

- [Google SRE — Canarying releases](https://sre.google/workbook/canarying-releases/)
- [Google SRE — Service best practices](https://sre.google/sre-book/service-best-practices/)
- [AWS Builders' Library — Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- [Google Cloud — Idempotency](https://cloud.google.com/discover/idempotency)
- [OpenFeature](https://openfeature.dev/)
- [Microsoft Experimentation Platform — Safe velocity](https://exp-platform.com/Documents/2019%20TongXiaSumitBhardwajPavelDmitrievAleksanderFabijan_Safe-Velocity-ICSE-SEI.pdf)
- [Microsoft Experimentation Platform — Metric interpretation pitfalls](https://exp-platform.com/Documents/2017-08%20KDDMetricInterpretationPitfalls.pdf)
- [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html)

# Maintenance rules

Review this reference when:

- WCAG, ISO 9241, NIST authentication/AI, platform HIG, or Core Web Vitals guidance changes;
- the skill adds a new domain such as voice, spatial, automotive, clinical, or safety-critical control;
- a cited URL becomes unavailable or materially changes scope;
- a pattern is promoted from hypothesis to standing guardrail;
- a standing guardrail proves context-dependent in repeated valid cases.

When updating:

1. prefer official standards, primary research, and first-party guidance;
2. record publication/version date for standards;
3. distinguish normative requirement from advisory guidance;
4. remove superseded editions when a current edition replaces them, while preserving migration notes when needed;
5. do not copy long copyrighted passages—summarize the operational implication and link the source;
6. keep product-specific findings out of this file;
7. keep the actionable rule in the skill or pattern catalog and use this file as its evidence basis.
