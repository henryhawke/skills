# SEO reference

Use this reference for technical SEO, on-page structure, structured data, mobile rendering, and international targeting. Separate what the code declares from what search engines actually crawl, index, and display.

## Contents

- [Evidence boundary](#evidence-boundary)
- [Crawlability and indexability](#crawlability-and-indexability)
- [Canonicalization and sitemaps](#canonicalization-and-sitemaps)
- [On-page signals](#on-page-signals)
- [Structured data](#structured-data)
- [Mobile and page experience](#mobile-and-page-experience)
- [International SEO](#international-seo)
- [Validation checklist](#validation-checklist)
- [Primary sources](#primary-sources)

## Evidence boundary

This skill can directly inspect technical and on-page implementation. It cannot prove:

- rankings or ranking-factor weights;
- traffic, impressions, clicks, or conversions;
- indexing or crawl frequency;
- backlink authority;
- content quality, intent fit, or keyword demand;
- Search Console status;

unless the corresponding provider/analytics/content evidence is available.

Avoid static percentage claims about ranking factors. Core Web Vitals and page experience matter, but relevance, content, links, locale, competition, and many other systems affect search results.

## Crawlability and indexability

### robots.txt

```text
User-agent: *
Allow: /

Disallow: /admin/
Disallow: /private/

Sitemap: https://example.com/sitemap.xml
```

Check:

- exact host/protocol and environment;
- important CSS/JS/image resources are not unintentionally blocked;
- private paths do not rely on robots.txt for security;
- robots directives match canonical URL policy;
- staging/test hosts are protected without leaking into production.

Robots blocking can prevent crawling but does not guarantee removal from an index.

### Robots meta and headers

```html
<meta name="robots" content="index,follow,max-image-preview:large">
```

Inspect rendered HTML and `X-Robots-Tag` response headers. Flag `noindex` only when the page is intended to be indexable. Test authenticated, preview, filter, pagination, and error variants separately.

### Renderability

- Inspect server response and rendered DOM.
- Confirm meaningful primary content and links are available to supported crawlers.
- Avoid important content that appears only after fragile client effects or interaction.
- Check status codes, redirect chains, soft-404 behavior, and canonical targets.

## Canonicalization and sitemaps

### Canonical URLs

```html
<link rel="canonical" href="https://example.com/products/blue-widget">
```

Check:

- self-referencing canonical on primary pages where appropriate;
- absolute normalized URL;
- status `200` and indexability of target;
- consistency with redirects, internal links, hreflang, and sitemap;
- query/filter/pagination behavior based on actual duplication and discovery needs;
- no cross-environment or wrong-locale canonical.

A canonical is a signal, not an access-control mechanism or guaranteed outcome.

### XML sitemaps

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2026-07-24</lastmod>
  </url>
</urlset>
```

- Include canonical, indexable URLs only.
- Use truthful `lastmod`.
- Keep each sitemap within the current protocol limits; the supplied baseline is 50,000 URLs or 50 MB uncompressed.
- Use sitemap indexes for larger sets.
- Validate fetchability, status, content type, and environment.
- Provider submission/status requires provider evidence.

### URL structure

Prefer readable, stable, lowercase HTTPS URLs with hyphens and minimal unnecessary parameters. Do not rewrite stable URLs solely to meet an arbitrary character count; migration, redirects, links, canonicals, and traffic history can outweigh cosmetic gains.

## On-page signals

### Titles

```html
<title>Blue Widgets for Outdoor Displays | Example Store</title>
```

- Make titles unique, descriptive, concise, and aligned with visible content.
- Put the primary topic early when natural.
- Use a consistent brand pattern.
- Treat the supplied `50–60` character range as a snippet-writing heuristic, not a hard audit gate; display depends on width and Google can generate title links from multiple sources.
- Avoid boilerplate, keyword repetition, and mismatches with the primary visual heading.

### Meta descriptions

```html
<meta
  name="description"
  content="Compare durable blue widgets for outdoor displays, with dimensions, finishes, shipping details, and 30-day returns."
>
```

- Make important pages unique, accurate, and useful.
- Treat the supplied `150–160` character range as a writing heuristic, not a guaranteed display length.
- Do not fabricate offers, ratings, inventory, or claims.
- Search engines may generate another snippet.

### Headings and document structure

- Give the page a clear primary heading/topic.
- Use meaningful hierarchy without skipping levels for styling alone.
- Keep titles, visible headings, breadcrumbs, and content aligned.
- Multiple `<h1>` elements are not automatically a search failure; flag them when they create ambiguous structure or template/content errors.

### Images

- Use descriptive filenames when practical.
- Provide contextual alt text for meaningful images and empty alt for decorative images.
- Use responsive, compressed formats and intrinsic dimensions.
- Lazy-load below-fold images, not the likely LCP image.
- Keep important images discoverable and accessible.

### Internal links and breadcrumbs

- Use descriptive anchor text that predicts destination.
- Link important pages from relevant crawlable pages.
- Fix verified broken links.
- Avoid orphan pages and excessive faceted URL generation.
- Use visible breadcrumbs where they help users; structured breadcrumbs must match the visible hierarchy.

## Structured data

Use JSON-LD when appropriate. The markup must describe visible, truthful page content and follow the current search feature's required/recommended properties.

Common types from the supplied material:

- `Organization` / `WebSite`;
- `Article`;
- `Product` with truthful offers and ratings;
- `FAQPage` where the current search feature and content qualify;
- `BreadcrumbList`.

Minimal breadcrumb example:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blue Widgets",
      "item": "https://example.com/products/blue-widgets"
    }
  ]
}
</script>
```

Validate:

- JSON syntax and schema type;
- current Google rich-result requirements where Google eligibility is claimed;
- URLs, currency, price, availability, ratings, author, publisher, and dates against visible/source-of-truth data;
- variant/localized page consistency;
- no hidden, misleading, duplicate, or stale markup.

Passing a validator establishes syntactic/eligibility checks, not that a rich result will appear.

## Mobile and page experience

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

Check:

- responsive viewport and layout;
- readable text without forced horizontal scrolling;
- touch-target size/spacing using the accessibility criteria;
- equivalent mobile content, metadata, structured data, canonicals, and hreflang;
- mobile Core Web Vitals and rendering;
- intrusive interstitials;
- lazy-loaded content remains discoverable and usable.

Do not duplicate accessibility target-size rules as a separate arbitrary SEO failure.

## International SEO

```html
<link rel="alternate" hreflang="en" href="https://example.com/page">
<link rel="alternate" hreflang="es-MX" href="https://example.com/es-mx/page">
<link rel="alternate" hreflang="x-default" href="https://example.com/page">
```

Verify:

- valid language/region codes;
- self and reciprocal alternate links;
- canonical/hreflang agreement;
- every alternate is indexable and resolves successfully;
- language declarations match content;
- locale routing does not force crawlers/users incorrectly;
- translated titles, descriptions, headings, alt text, and structured data.

## Validation checklist

### Critical

- [ ] HTTPS and expected status codes.
- [ ] Important pages crawlable and not unintentionally `noindex`.
- [ ] Canonical targets correct and indexable.
- [ ] Production robots/sitemap do not reference another environment.
- [ ] Primary content renders and internal links are discoverable.

### High

- [ ] Unique, accurate titles and useful descriptions.
- [ ] Sitemap contains canonical indexable URLs and truthful `lastmod`.
- [ ] Mobile content/metadata parity.
- [ ] Core Web Vitals classified with available evidence.
- [ ] Structured data matches visible source-of-truth content.

### Additional

- [ ] Clear heading/content hierarchy.
- [ ] Descriptive internal links and useful breadcrumbs.
- [ ] Images have correct alt, dimensions, responsive delivery, and loading priority.
- [ ] International alternates reciprocal and canonical-consistent.
- [ ] Broken links, redirect chains, soft 404s, and faceted duplicates checked.

Useful primary tools:

- Google Search Console for actual crawl/index/search evidence;
- URL Inspection and Rich Results Test;
- Schema.org validator;
- PageSpeed Insights and CrUX for page experience;
- a crawler for representative/site-wide URL evidence.

Report provider status only when the provider was actually queried.

## Primary sources

- [Google Search Essentials](https://developers.google.com/search/docs/essentials)
- [Crawling and indexing documentation](https://developers.google.com/search/docs/crawling-indexing)
- [Structured data documentation](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Schema.org](https://schema.org/)
