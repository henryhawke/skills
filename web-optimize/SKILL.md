---
name: web-optimize
description: Audit, diagnose, prioritize, implement, and validate total web quality across performance, Core Web Vitals (LCP, INP, CLS), accessibility and WCAG 2.2, technical and on-page SEO, and browser best practices. Use for requests to audit or optimize a website, page, route, storefront, or web app; improve Lighthouse or PageSpeed results; speed up loading or interactions; fix layout shifts; review keyboard, screen-reader, contrast, forms, or ARIA behavior; inspect crawlability, metadata, canonicals, sitemaps, structured data, or international SEO; or produce an evidence-backed remediation plan spanning these areas.
---

# Web Optimize

Audit the whole page experience, connect each finding to precise evidence, and optimize the highest-impact root causes without confusing code inspection, lab measurements, field data, deployed behavior, or hypotheses.

## Reference map

Read only the references needed for the requested scope:

- Read [references/performance.md](references/performance.md) for loading, rendering, network, assets, caching, JavaScript, fonts, images, third parties, and runtime work.
- Read [references/core-web-vitals.md](references/core-web-vitals.md) whenever LCP, INP, CLS, PageSpeed, Lighthouse performance, or page experience is in scope.
- Read [references/accessibility.md](references/accessibility.md) for every user-facing audit or change; it covers WCAG 2.2, automated checks, and required manual testing.
- Read [references/seo.md](references/seo.md) for public/indexable pages, metadata, crawl controls, canonicals, sitemaps, structured data, mobile SEO, and internationalization.
- Read [references/best-practices.md](references/best-practices.md) for security-adjacent browser checks, modern platform practices, console/runtime health, permissions, and misleading UX.

For a comprehensive audit, read all five.

## Choose the operating mode

| Mode | Use when | Permission boundary | Required result |
|---|---|---|---|
| **Audit** | Review, diagnose, benchmark, or recommend | Inspect and measure only | Evidence-backed findings, proof limits, and ranked plan |
| **Optimize** | Fix or improve the site | Modify only the authorized repository/surfaces | Coherent fixes plus focused regression checks |
| **Validate** | Verify a candidate or claimed improvement | Do not expand the change | Same-condition before/after evidence and remaining uncertainty |

Combine modes only when the request authorizes them. An audit request does not authorize code changes, deployment, Search Console changes, dependency upgrades, or production configuration changes.

## Preserve proof boundaries

Label material evidence:

- **CODE** — current repository, configuration, generated markup, bundle, or asset evidence.
- **LAB** — controlled synthetic run such as Lighthouse, DevTools, axe, or WebPageTest.
- **FIELD** — real-user data such as CrUX, RUM, or Search Console, with period and percentile.
- **MANUAL** — reproducible keyboard, screen-reader, zoom, reflow, motion, visual, or interaction observation.
- **RUNTIME** — browser/network behavior observed in the named environment.
- **EXTERNAL** — an official standard or primary documentation.
- **HYPOTHESIS** — plausible cause or expected improvement not yet verified.
- **UNKNOWN** — evidence unavailable.

Never treat one class as another:

- Code that looks optimized is not measured performance.
- A local Lighthouse run is not field data or deployed proof.
- Lighthouse accessibility is not a WCAG conformance determination.
- A passing automated check does not prove keyboard or assistive-technology usability.
- A lab improvement does not prove an immediate CrUX or Search Console change.
- A recommendation is not an implemented or validated fix.

## Workflow

### 1. Frame scope and success

Record:

- target URL, route, repository, build, commit, and environment;
- public, authenticated, personalized, localized, or device-specific variants;
- representative page templates and the reason each is included;
- mobile/desktop viewport, network/CPU conditions, cache state, and test count;
- available source, runtime, provider, lab, field, analytics, and search data;
- user-requested thresholds, budgets, WCAG target, browser support, and business-critical journeys;
- whether the task is audit-only, implementation, or validation.

If scope is broad, sample by distinct templates and critical journeys rather than claiming site-wide coverage from one URL. Report exclusions.

### 2. Establish a reproducible baseline

Prefer the strongest available evidence:

1. FIELD data for real-user Core Web Vitals and search/indexing status.
2. Repeated LAB and RUNTIME measurements for diagnosis.
3. MANUAL accessibility and interaction testing.
4. CODE inspection to identify owning files and likely root causes.

Record tool/version, date, device profile, throttling, cache state, URL, run count, aggregation, and raw artifact path or result identifier. Use the median for noisy lab timing unless the tool or user specifies another method. Preserve outliers and explain exclusions.

When thresholds or platform guidance may have changed, retrieve current primary documentation before asserting exact numbers. Treat generic resource budgets as starting heuristics unless the project has adopted them as gates.

### 3. Run all applicable audit lanes

#### Performance

Inspect the critical rendering path, server response, compression and protocols, dependency chains, render-blocking resources, preloads/preconnects, JavaScript parse/execute cost, CSS, images, fonts, caching, third parties, long tasks, layout work, and production bundle behavior.

Measure Core Web Vitals plus useful diagnostic metrics. Do not optimize a metric in isolation when the change can harm another lane—for example, do not lazy-load the LCP image, preload speculative assets, remove semantics to reduce DOM size, or delay consent/security behavior without authorization.

#### Core Web Vitals

Classify LCP, INP, and CLS using current field thresholds at the 75th percentile when field data exists. Diagnose the metric into actionable phases and identify the actual element, interaction, task, or shift source. Use TBT as an INP diagnostic proxy in load-only lab tools, not as field INP.

#### Accessibility

Target the requested conformance level; default to WCAG 2.2 A and AA for an audit, without making a legal-compliance claim. Combine automated checks with keyboard, focus, zoom/reflow, reduced-motion, content, form/error, and representative screen-reader testing. Prefer native semantics; verify name, role, state, focus order, and announcements for custom widgets.

#### SEO

Separate crawlability, indexability, canonicalization, rendering, on-page signals, structured-data eligibility, mobile behavior, and international targeting. Inspect representative rendered pages as well as templates/config. Do not infer rankings, traffic, backlinks, indexing, or Search Console status without their data.

#### Best practices

Check HTTPS and mixed content, browser/runtime errors, vulnerable or deprecated behavior, security headers in context, production source maps and debug exposure, permission prompting, intrusive interstitials, misleading actions, doctype/charset, CORS failures, and dependency health. Escalate suspected security vulnerabilities to an appropriate security workflow rather than claiming exploitability from a generic quality audit.

### 4. Correlate findings into root causes

Deduplicate symptoms that share an owner. Examples:

- One unoptimized hero asset can drive page weight, LCP, responsive-image, CLS, and image-SEO findings.
- A client-rendered primary heading can affect LCP, crawl rendering, focus restoration, and no-JavaScript resilience.
- A heavy third-party widget can affect main-thread responsiveness, permissions, layout shifts, and privacy expectations.
- A custom non-semantic control can affect keyboard access, accessible naming, INP, and automation reliability.

Preserve each affected domain in the finding, but recommend one coherent root-cause fix and a cross-domain validation plan.

### 5. Prioritize

Use severity first, then evidence confidence, affected traffic/journey, expected benefit, effort, risk, and reversibility.

| Severity | Meaning |
|---|---|
| **Critical** | Active security exposure, essential journey unusable, important content unintentionally non-indexable, or complete blocking failure with strong evidence |
| **High** | Poor Core Web Vital on important traffic, major WCAG A/AA barrier, severe runtime failure, or broad crawl/canonical defect |
| **Medium** | Material performance opportunity, partial accessibility barrier, SEO quality defect, or standards issue with bounded impact |
| **Low** | Minor optimization, resilience improvement, or maintainability issue with limited user impact |

Do not manufacture a numeric score or expected millisecond/traffic gain. Use tool-estimated savings only when the tool, conditions, and limitations are named.

### 6. Implement only authorized fixes

For each fix:

1. Trace the owning source, callers, generated output, and deployment boundary.
2. Choose the smallest coherent change that addresses the verified root cause.
3. Preserve semantics, security, privacy, consent, content accuracy, responsive behavior, and existing business logic.
4. Add or update focused tests where the repository supports them.
5. Avoid unrelated refactors, dependency churn, and score-chasing.
6. Rebuild or regenerate derived assets only through the repository's source-of-truth workflow.

### 7. Validate under comparable conditions

Re-run the affected automated, runtime, and manual checks under the same conditions as the baseline. Run enough samples to avoid presenting noise as improvement. Validate adjacent lanes when a change crosses concerns:

- LCP image changes: LCP, responsive sizing, CLS, alt semantics, visual quality, and caching.
- Interaction changes: INP/long tasks, keyboard behavior, focus, announcements, and error recovery.
- metadata/schema changes: rendered head, canonical URL, robots directives, schema validator, and route variants.
- font changes: render timing, visual stability, legibility, localization, and fallback behavior.

Report local/candidate/deployed/field evidence separately. State what remains unverified.

## Output contract

Lead with the outcome and use this structure:

1. **Outcome and scope** — what was audited or changed, representative surfaces, environment, and exclusions.
2. **Proof boundary** — evidence classes available and missing.
3. **Baseline** — measured metrics and status with conditions; omit unavailable values.
4. **Ranked findings** — use stable IDs and include:
   - severity and affected domain(s);
   - precise URL, interaction, element, request, or `file:line`;
   - evidence and reproduction;
   - user/business/search impact;
   - root cause and source owner;
   - specific fix;
   - validation method and risk.
5. **Domain summary** — Performance, Core Web Vitals, Accessibility, SEO, and Best Practices, using `not tested` rather than invented scores.
6. **Priority plan or changes made** — distinguish recommendations from completed edits.
7. **Validation** — commands/tools/manual scenarios actually run and their results.
8. **Remaining risks and unknowns** — field lag, unavailable accounts, untested devices, route coverage, or deployment gaps.

For a clean audit, explicitly report no verified findings in the audited scope. Do not invent low-value issues to fill every category.

## Final gate

Before responding:

- Verify every finding has concrete evidence and an exact affected surface.
- Verify metric labels, units, percentiles, test conditions, and field/lab distinctions.
- Verify automated accessibility results are paired with manual-test limits.
- Verify SEO claims distinguish code/config from observed crawl/index/search data.
- Verify duplicate symptoms are consolidated around root causes.
- Verify severity reflects impact, not the ease of fixing it.
- Verify implementation stayed within authorization and unrelated dirty work was preserved.
- Verify before/after claims use comparable conditions.
- Verify no deployment, provider, legal-compliance, ranking, or production-success claim exceeds the evidence.
