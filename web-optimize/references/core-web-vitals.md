# Core Web Vitals reference

Use this reference to measure and optimize Largest Contentful Paint (LCP), Interaction to Next Paint (INP), and Cumulative Layout Shift (CLS).

## Contents

- [Classification](#classification)
- [LCP](#lcp)
- [INP](#inp)
- [CLS](#cls)
- [Measurement](#measurement)
- [Framework patterns](#framework-patterns)
- [Cross-metric validation](#cross-metric-validation)
- [Primary sources](#primary-sources)

## Classification

Verify current thresholds against web.dev before making a time-sensitive claim. The supplied material uses:

| Metric | Good | Needs improvement | Poor |
|---|---:|---:|---:|
| LCP | `≤ 2.5 s` | `> 2.5 s` and `≤ 4.0 s` | `> 4.0 s` |
| INP | `≤ 200 ms` | `> 200 ms` and `≤ 500 ms` | `> 500 ms` |
| CLS | `≤ 0.10` | `> 0.10` and `≤ 0.25` | `> 0.25` |

Use the 75th percentile of eligible page views for field classification. Segment by mobile/desktop and distinguish page-level data from origin-level fallback data.

Lab and field answer different questions:

- FIELD values describe real users over a reporting period.
- LAB runs reproduce and diagnose a controlled page load or interaction.
- Lighthouse TBT helps diagnose main-thread blocking but is not INP.
- A single fast run cannot prove the 75th-percentile experience.

## LCP

LCP measures when the largest qualifying visible content element is rendered.

Common candidates:

- hero or product image;
- poster image for video;
- large heading or text block;
- CSS background image where eligible;
- large SVG or rendered content block.

### Diagnose the four phases

1. **TTFB** — redirects, connection, CDN, origin, server work.
2. **Resource load delay** — late discovery, client rendering, CSS background discovery, low priority.
3. **Resource load duration** — bytes, format, connection, cache.
4. **Element render delay** — render-blocking CSS/JS, font wait, hidden/revealed content, main-thread work.

Identify the actual LCP element and phase proportions before choosing a fix.

### Frequent causes and treatments

- Slow TTFB: cache safely at the edge, remove redirect chains, optimize backend work, stream or statically render where appropriate.
- Late discovery: include the LCP content/resource in initial HTML, avoid JS-only injection, preload only verified candidates.
- Low priority: use `fetchpriority="high"` and eager loading on the actual hero candidate.
- Oversized media: responsive sources, modern formats, correct dimensions, compression.
- Render blocking: reduce critical CSS/JS, defer non-critical work, avoid font blocking.
- Client-rendered primary content: use SSR, SSG, server components, or streaming where the framework and freshness model support it.

```js
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const latest = entries.at(-1);
  console.log({
    element: latest?.element,
    url: latest?.url,
    startTime: latest?.startTime,
  });
}).observe({ type: "largest-contentful-paint", buffered: true });
```

### LCP checklist

- [ ] Actual LCP element identified per important template/breakpoint.
- [ ] TTFB and LCP phase breakdown captured.
- [ ] Candidate is present/discoverable in initial HTML where feasible.
- [ ] LCP image is not lazy-loaded.
- [ ] Correct responsive source, dimensions, format, and visual quality verified.
- [ ] Priority hint/preload does not create duplicate or competing downloads.
- [ ] Critical CSS, fonts, and main-thread delay inspected.

## INP

INP measures page responsiveness across click, tap, and keyboard interactions. It includes:

`input delay + event processing duration + presentation delay`

Useful diagnostic goals from the supplied material:

| Phase | Diagnostic target |
|---|---:|
| Input delay | `< 50 ms` |
| Processing | `< 100 ms` |
| Presentation delay | `< 50 ms` |

Treat these as investigation guides, not separate Core Web Vital gates.

### Frequent causes

- long tasks blocking the main thread;
- heavy or nested event handlers;
- synchronous parsing/computation;
- broad state updates and excessive rendering;
- forced layout and large DOM work;
- third-party handlers;
- hydration or startup contention;
- no immediate feedback while deferred work runs.

### Yield long work

```ts
async function processInChunks<T>(items: T[], process: (item: T) => void) {
  const chunkSize = 100;

  for (let index = 0; index < items.length; index += chunkSize) {
    items.slice(index, index + chunkSize).forEach(process);

    if ("scheduler" in globalThis && "yield" in globalThis.scheduler) {
      await globalThis.scheduler.yield();
    } else {
      await new Promise<void>((resolve) => setTimeout(resolve, 0));
    }
  }
}
```

Type definitions and browser support for `scheduler.yield()` vary; feature-detect and validate the fallback.

### Interaction treatment order

1. Give immediate, truthful visual/state feedback.
2. Remove unnecessary work from the handler.
3. Narrow the state/render scope.
4. Batch DOM reads and writes.
5. Split or yield long work.
6. Move CPU work to a worker where serializable.
7. Defer analytics or non-critical work without losing required events.
8. Lazy-load third parties while preserving consent and functionality.

```js
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 200) {
      console.warn("Slow interaction", {
        name: entry.name,
        duration: entry.duration,
        processingStart: entry.processingStart,
        processingEnd: entry.processingEnd,
        target: entry.target,
      });
    }
  }
}).observe({ type: "event", buffered: true, durationThreshold: 16 });
```

### INP checklist

- [ ] Important interactions exercised, including keyboard input and slow/error states.
- [ ] Slow interaction and corresponding main-thread/render trace identified.
- [ ] Immediate feedback preserved.
- [ ] Long tasks split or removed.
- [ ] Framework profiler confirms owning render/work.
- [ ] Third-party cost and event listeners inspected.
- [ ] Accessibility announcements/focus remain correct after scheduling changes.

## CLS

CLS measures unexpected visual instability. Diagnose shift sources; do not infer the culprit solely from the final score.

### Frequent causes and treatments

#### Unsized media

```html
<img src="/photo.jpg" width="800" height="600" alt="Description">
```

Or reserve the correct responsive aspect ratio.

#### Ads, embeds, and async content

Reserve an accurate slot with dimensions, `min-height`, or `aspect-ratio`. Define empty, failed, and responsive states so reserved space does not become a large permanent gap.

#### Injected content

Avoid inserting banners, notices, personalization, or validation content above existing visible content unless triggered by the user's action and expected. Reserve the region or overlay without obscuring content/focus.

#### Fonts

Use appropriate `font-display`, preload only critical fonts, and match fallback metrics when justified:

```css
@font-face {
  font-family: "Custom";
  src: url("/custom.woff2") format("woff2");
  font-display: swap;
  size-adjust: 105%;
  ascent-override: 95%;
  descent-override: 20%;
}
```

Values must come from real font metrics, not copied examples.

#### Animation

Prefer `transform` and `opacity` to animated layout properties. Validate focus, reduced motion, hit targets, and final layout.

```css
.panel {
  transition: transform 180ms ease, opacity 180ms ease;
}
```

### Observe shifts

```js
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (!entry.hadRecentInput) {
      console.log("Layout shift", entry.value);
      for (const source of entry.sources ?? []) {
        console.log(source.node, source.previousRect, source.currentRect);
      }
    }
  }
}).observe({ type: "layout-shift", buffered: true });
```

### CLS checklist

- [ ] Images, video, iframes, ads, and embeds reserve space.
- [ ] Loading, empty, error, consent, and personalized regions have stable geometry.
- [ ] Font fallback and language variants tested.
- [ ] No unrequested content is injected above visible content.
- [ ] Animations avoid layout properties where feasible.
- [ ] DevTools shift clusters and elements captured.
- [ ] Mobile, desktop, orientation, and responsive breakpoints checked.

## Measurement

Use:

- Chrome UX Report, PageSpeed Insights, Search Console, or project RUM for field data;
- Chrome DevTools Performance and Lighthouse for lab diagnosis;
- WebPageTest for waterfalls, filmstrips, and repeated profiles;
- the `web-vitals` package for real-user instrumentation.

```ts
import { onCLS, onINP, onLCP, type Metric } from "web-vitals";

function report(metric: Metric) {
  analytics.send("web-vital", {
    id: metric.id,
    name: metric.name,
    value: metric.value,
    rating: metric.rating,
    navigationType: metric.navigationType,
  });
}

onLCP(report);
onINP(report);
onCLS(report);
```

Define sampling, consent/privacy, route attribution, version, device, and aggregation before treating RUM as decision-grade.

## Framework patterns

### React

- Render essential above-fold content without waiting for an effect fetch when architecture permits.
- Use route/component lazy loading for genuinely deferred code.
- Use `startTransition` for non-urgent rendering, not urgent input feedback.
- Profile component renders before memoizing.
- Give images intrinsic dimensions and stable placeholders.

### Next.js

- Use the framework image component with correct `sizes` and priority/preload behavior for the actual LCP candidate.
- Choose static, server, streaming, or client rendering based on data freshness and personalization.
- Inspect hydration and client bundles; server rendering alone does not guarantee low INP.

### Vue/Nuxt and other frameworks

- Use the framework's image and async-component primitives correctly.
- Keep above-fold content server-rendered where appropriate.
- Reserve media/component space and trace hydration/runtime work.

## Cross-metric validation

- LCP optimization must not create CLS through incorrect dimensions or harm accessibility through empty/misleading alt text.
- INP optimization must not delay necessary state, focus, error announcements, consent, or safety behavior.
- CLS optimization must not leave large unusable gaps or obscure focused content.
- Aggressive preloads must not starve CSS, fonts, or other critical resources.
- Server rendering must preserve cache/privacy boundaries and interactive correctness.

## Primary sources

- [Core Web Vitals thresholds and methodology](https://web.dev/articles/defining-core-web-vitals-thresholds)
- [Field measurement best practices](https://web.dev/articles/vitals-field-measurement-best-practices)
- [LCP](https://web.dev/articles/lcp), [INP](https://web.dev/articles/inp), and [CLS](https://web.dev/articles/cls)
