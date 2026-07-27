# Browser and web best-practices reference

Use this reference for the quality areas that sit outside the dedicated performance, accessibility, and SEO lanes.

## Contents

- [Security-adjacent checks](#security-adjacent-checks)
- [Modern platform checks](#modern-platform-checks)
- [Runtime and network health](#runtime-and-network-health)
- [User-experience integrity](#user-experience-integrity)
- [Operational cadence](#operational-cadence)
- [Validation checklist](#validation-checklist)
- [Primary sources](#primary-sources)

## Security-adjacent checks

Inspect:

- HTTPS on documents and subresources;
- mixed active/passive content;
- HSTS suitability and preload implications;
- Content Security Policy presence/effectiveness in context;
- clickjacking protections (`frame-ancestors`, with legacy headers where needed);
- `X-Content-Type-Options: nosniff`;
- referrer and permissions policies based on product needs;
- third-party scripts and integrity/supply-chain controls;
- dependency advisories using repository-approved tooling;
- production source maps, debug endpoints, verbose errors, and exposed secrets.

Do not label generic security headers as direct SEO ranking signals. Do not assert exploitability from header absence alone. Route credible vulnerabilities to a security-specific review with threat, reachability, and deployment evidence.

Source maps are not automatically unsafe: assess whether they expose proprietary code, secrets, internal endpoints, or sensitive implementation details, and whether access is controlled.

## Modern platform checks

- Valid `<!doctype html>`.
- Character encoding declared early (`<meta charset="utf-8">` or header).
- Viewport configured for responsive pages.
- No deprecated APIs such as `document.write` or synchronous XHR on the main thread without a justified compatibility need.
- No obsolete plugins or insecure transport.
- Supported browser targets and polyfills match product policy.
- Progressive enhancement or truthful degraded behavior for essential tasks.
- Cross-origin isolation/CORS/CSP configured intentionally.

Do not recommend replacing an API merely because it is old; verify deprecation, browser support, use, impact, and replacement behavior.

## Runtime and network health

Inspect clean and failure paths for:

- uncaught exceptions and unhandled promise rejections;
- hydration or render mismatches;
- failed resources and unexpected redirects;
- CORS and CSP violations;
- 4xx/5xx API failures;
- mixed content and certificate issues;
- duplicate requests, retry storms, or polling loops;
- stale asset/document version mismatches;
- console warnings tied to real behavior;
- offline, timeout, and third-party failure behavior.

Ignore unrelated development-only warnings only when the audited target is a production build and the proof boundary is explicit.

## User-experience integrity

Check:

- intrusive interstitials, especially on entry and mobile;
- permission requests shown only at a meaningful moment with context;
- notification, location, camera, clipboard, and media behavior;
- buttons and links whose labels accurately predict their effect;
- deceptive countdowns, disguised ads, forced continuity, or false scarcity;
- autoplaying media and unexpected sound;
- download/open-new-window behavior communicated where needed;
- destructive or consequential actions with appropriate review, status, recovery, and idempotency;
- success messages that correspond to a durable outcome;
- loading and skeleton states that do not misrepresent progress.

Performance optimization must not weaken consent, permissions, authentication, fraud controls, safety messages, or auditability.

## Operational cadence

Use cadence only when it fits the product:

### Before deployment

- [ ] Core Web Vitals/performance checks for changed critical templates.
- [ ] No new automated accessibility violations and relevant manual flows replayed.
- [ ] No unexpected console/network errors.
- [ ] HTTPS/mixed-content checks.
- [ ] Metadata, canonical, robots, and structured data for changed public routes.

### Recurring review

- [ ] Field Core Web Vitals trends.
- [ ] Search Console crawl/index enhancements and regressions.
- [ ] Dependency/security advisories.
- [ ] Representative keyboard/screen-reader checks.
- [ ] Third-party cost and ownership.
- [ ] Performance budgets on important templates.

### Periodic deep dive

- [ ] Representative-template Lighthouse/DevTools/WebPageTest runs.
- [ ] RUM distribution and slow-segment diagnosis.
- [ ] WCAG manual audit with representative assistive technologies.
- [ ] Crawl/canonical/structured-data review.
- [ ] Content and keyword research only when separately scoped and evidenced.

## Validation checklist

- [ ] Production-like build and named environment used.
- [ ] HTTPS and mixed-content behavior observed.
- [ ] Response headers captured rather than inferred from config.
- [ ] Console and network checked through important success/error journeys.
- [ ] Deprecated/vulnerable behavior confirmed reachable before prioritization.
- [ ] Permission prompts tested at the moment they appear.
- [ ] Interstitials checked on mobile and entry routes.
- [ ] Labels, consequences, status, and recovery verified for consequential actions.
- [ ] No secrets or personal data copied into reports.
- [ ] Security suspicions clearly separated from verified vulnerabilities.

## Primary sources

- [Lighthouse documentation](https://developer.chrome.com/docs/lighthouse/)
- [MDN HTTP security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Security)
- [W3C Permissions](https://www.w3.org/TR/permissions/)
