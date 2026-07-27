# Performance reference

Use this reference for page-load, network, rendering, bundle, asset, caching, third-party, and runtime-performance work.

## Contents

- [Measurement and budgets](#measurement-and-budgets)
- [Critical rendering path](#critical-rendering-path)
- [JavaScript and CSS](#javascript-and-css)
- [Images](#images)
- [Fonts](#fonts)
- [Caching](#caching)
- [Runtime performance](#runtime-performance)
- [Third parties](#third-parties)
- [Validation checklist](#validation-checklist)
- [Primary sources](#primary-sources)

## Measurement and budgets

Measure before prescribing. Capture cold and warm behavior where relevant, repeat noisy lab tests, and pair synthetic diagnosis with field data when available.

Useful diagnostic targets from the supplied audit material:

| Metric | Good starting target | Evidence note |
|---|---:|---|
| TTFB | `< 800 ms` | Diagnose origin, CDN, redirects, and connection time separately |
| FCP | `< 1.8 s` | Lab diagnostic, not a Core Web Vital |
| TBT | `< 200 ms` | Lab proxy for main-thread blocking, not field INP |
| Speed Index | `< 3.4 s` | Lab visual-progress diagnostic |

Treat these supplied resource budgets as initial heuristics, not universal pass/fail rules:

| Resource | Starting budget |
|---|---:|
| Total page transfer | `< 1.5 MB` |
| Compressed JavaScript | `< 300 KB` |
| Compressed CSS | `< 100 KB` |
| Above-fold images | `< 500 KB` |
| Fonts | `< 100 KB` |
| Third-party transfer | `< 200 KB` |

Replace heuristics with repository-owned budgets based on audience devices, network conditions, page purpose, cache state, and current baseline. Track transfer size and decoded/execute cost separately.

## Critical rendering path

### Server and document

Inspect:

- redirects, DNS, TLS, origin response, CDN/edge behavior, and document TTFB;
- server rendering versus client-only discovery of primary content;
- Brotli or gzip for compressible text;
- HTTP/2 or HTTP/3 support where the hosting stack provides it;
- HTML caching rules appropriate to personalization and authentication;
- early hints or streaming only when supported and measured.

Do not cache private or user-specific HTML publicly.

### Connection and priority hints

Add hints only for verified critical resources:

```html
<link rel="preconnect" href="https://cdn.example.com" crossorigin>
<link
  rel="preload"
  href="/hero-1280.avif"
  as="image"
  type="image/avif"
  fetchpriority="high"
>
```

- Preconnect only to origins used early enough to benefit.
- Preload only resources required for the current route and viewport.
- Match `crossorigin`, `type`, media, and responsive-image attributes so the preload is reusable.
- Avoid double downloads and priority competition.

### CSS delivery

- Inline only genuinely critical, route-specific CSS when measurement justifies the complexity.
- Load non-critical styles without breaking no-script behavior.
- Avoid `@import` dependency chains.
- Remove unused CSS only after verifying dynamic classes, variants, and CMS content.
- Prefer source-level splitting over post-build deletion.

```html
<style>/* Small above-the-fold critical rules */</style>
<link rel="preload" href="/styles.css" as="style" onload="this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/styles.css"></noscript>
```

Validate Content Security Policy compatibility before using inline event attributes or styles.

## JavaScript and CSS

### Script loading

```html
<script defer src="/app.js"></script>
<script async src="/independent-analytics.js"></script>
<script type="module" src="/app.mjs"></script>
```

- Use `defer` for ordered scripts that need the parsed DOM.
- Use `async` only for independent scripts.
- Modules are deferred by default.
- Keep essential above-fold content in initial HTML where feasible.

### Split by user need

```tsx
const HeavyChart = React.lazy(() => import("./HeavyChart"));

async function loadPremiumTools() {
  const { PremiumTools } = await import("./PremiumTools");
  return PremiumTools;
}
```

Split at routes, infrequent features, and heavy components. Check that fragmentation does not create long request chains or repeated vendor chunks.

### Imports and dead code

```ts
// Prefer a narrow import when the package supports it.
import debounce from "lodash/debounce";
```

Verify tree-shaking configuration, package `sideEffects`, barrel exports, polyfills, source-map settings, and browser targets against the actual build. Inspect production output; source appearance alone does not prove the bundle.

## Images

### Format and responsive delivery

| Format | Typical use |
|---|---|
| AVIF | Photos where encode/decode/browser support and quality are acceptable |
| WebP | Broad modern photo fallback |
| PNG | Lossless graphics or transparency when modern alternatives do not fit |
| SVG | Logos, icons, and vector illustrations |

```html
<picture>
  <source
    type="image/avif"
    srcset="/hero-480.avif 480w, /hero-960.avif 960w, /hero-1440.avif 1440w"
    sizes="(max-width: 700px) 100vw, 60vw"
  >
  <source
    type="image/webp"
    srcset="/hero-480.webp 480w, /hero-960.webp 960w, /hero-1440.webp 1440w"
    sizes="(max-width: 700px) 100vw, 60vw"
  >
  <img
    src="/hero-960.jpg"
    srcset="/hero-480.jpg 480w, /hero-960.jpg 960w, /hero-1440.jpg 1440w"
    sizes="(max-width: 700px) 100vw, 60vw"
    width="1440"
    height="810"
    alt="Meaningful description"
    fetchpriority="high"
    loading="eager"
  >
</picture>
```

- Give the LCP image eager/high priority only when it is actually the LCP candidate.
- Lazy-load below-fold images and iframes.
- Supply intrinsic dimensions or `aspect-ratio`.
- Size sources to rendered dimensions and device density.
- Preserve meaningful alt text; use `alt=""` for decorative images.
- Validate crop, art direction, sharpness, and transfer cost across breakpoints.

## Fonts

```css
@font-face {
  font-family: "Custom";
  src: url("/fonts/custom-latin.woff2") format("woff2");
  font-display: swap;
  font-weight: 100 900;
  unicode-range: U+0000-00FF;
}
```

- Prefer WOFF2 and subset only when language coverage is preserved.
- Preload only fonts used in critical visible text.
- Use a compatible fallback stack.
- Consider variable fonts when one file replaces multiple used weights.
- Measure `swap` versus `optional`; neither is automatically correct.
- Use `size-adjust`, `ascent-override`, and related metrics only after matching the real fallback and validating legibility/CLS.

## Caching

Typical policy:

```text
# HTML that must revalidate
Cache-Control: no-cache

# Content-hashed static asset
Cache-Control: public, max-age=31536000, immutable

# Unhashed public asset
Cache-Control: public, max-age=86400, stale-while-revalidate=604800
```

- Match policy to mutability, privacy, invalidation, and CDN behavior.
- Content-hash immutable assets.
- Do not cache personalized API responses publicly.
- Verify actual response headers and repeat-request behavior.
- Add service workers only with a versioning, invalidation, offline, and recovery design; a naïve cache-first handler can serve stale app code or private content.

## Runtime performance

### Avoid layout thrashing

Batch DOM reads before writes:

```js
const heights = elements.map((element) => element.offsetHeight);
elements.forEach((element, index) => {
  element.style.height = `${heights[index] + 10}px`;
});
```

### Schedule work intentionally

- Keep event handlers short and provide immediate visual feedback.
- Break long work into chunks and yield to the browser.
- Use workers for CPU-heavy work that does not need direct DOM access.
- Use `requestAnimationFrame` for visual updates.
- Use idle time only for work that can safely wait.
- Debounce high-frequency events when delaying the response is acceptable.
- Virtualize large lists when DOM size and rendering are measured bottlenecks.
- Prefer `content-visibility: auto` only after validating focus, find-in-page, accessibility, and intrinsic sizing.

In React, profile before adding `memo`, `useMemo`, or `useCallback`; memoization adds comparison and maintenance cost and does not fix unstable architecture by itself.

## Third parties

Inventory every third-party script by owner, purpose, route, transfer, main-thread cost, privacy/consent requirement, failure behavior, and user value.

Use:

- async/deferred loading where semantics permit;
- route or interaction-based loading;
- facades for media/widgets;
- server-side alternatives for essential metadata;
- explicit timeout and degraded states;
- removal only after confirming no required traffic or business function.

```html
<div class="video-facade" data-video-id="abc123">
  <img src="/thumbnails/abc123.jpg" alt="Video title">
  <button type="button" aria-label="Play Video title">Play</button>
</div>
```

Do not delay consent, fraud, security, accessibility, or legally required behavior merely to improve a score.

## Validation checklist

- [ ] Record baseline and candidate under the same URL, build, device, network, CPU, and cache conditions.
- [ ] Inspect the waterfall and initiator chains, not only aggregate scores.
- [ ] Confirm LCP resource discovery and priority.
- [ ] Confirm no duplicate preload/download.
- [ ] Confirm production transfer, parse, compile, and execute cost.
- [ ] Confirm responsive images and fonts across breakpoints/languages.
- [ ] Confirm caching with actual response headers and repeat requests.
- [ ] Replay key interactions and inspect long tasks/renders.
- [ ] Recheck accessibility, SEO rendering, consent, and error behavior after delivery changes.
- [ ] Keep local, deployed, lab, and field proof separate.

## Primary sources

- [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/)
- [Lighthouse performance scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring/)
- [web.dev performance guidance](https://web.dev/explore/fast)
