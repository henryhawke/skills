# Shopify development preview

Use this reference to decide which URL is authoritative during the loop.

## Development routing

`shopify app dev` selects a development store, serves the app backend, creates
external networking through Shopify CLI's reverse proxy/tunnel, and watches
supported extensions. When development URL updates are enabled, the app URL
change is isolated to the selected development store.

For an app proxy, prefer a relative `url` in `shopify.app.toml`:

```toml
[app_proxy]
prefix = "apps"
subpath = "example"
url = "/apps/example"

[build]
automatically_update_urls_on_dev = true
```

During `shopify app dev`, Shopify prepends the development app URL/tunnel to the
relative proxy endpoint. The storefront continues requesting
`https://<dev-store>/<prefix>/<subpath>`; Shopify forwards that request to the
local app. This preserves Shopify's app-proxy signature and storefront context.

Theme app extensions are included in the development preview and their local
changes are watched. Use the extension preview or Dev Console link emitted by
the CLI. If a block or app embed is absent, add/enable it on the development or
preview theme only.

## Readiness and URLs

Keep these surfaces distinct:

| Surface | Use |
|---|---|
| Localhost app URL | Server readiness and backend diagnostics |
| CLI tunnel URL | Shopify-to-local transport; do not treat as production |
| Embedded app preview | Admin UI and authenticated app navigation |
| Dev-store app-proxy URL | Storefront integration, signatures, and customer context |
| Theme-extension preview | Liquid, extension assets, app blocks, and app embeds |
| Production app or Cloud Run URL | Out of scope unless separately authorized |

An HTTP redirect, 401, or 403 can prove that a local server is listening. It
does not prove the requested feature works. Complete browser validation through
the preview appropriate to the feature.

## Limits and failure routing

- Development URL changes do not make the local build active on other stores.
- App-proxy prefix/subpath values can be customized by merchants and are
  effectively installation-bound. Use the actual installed storefront path.
- A direct localhost storefront request does not reproduce Shopify app-proxy
  signing or Liquid/theme behavior.
- If the app preview is connected but the storefront still reaches production,
  verify the selected development store, relative proxy `url`, automatic dev URL
  updates, active CLI preview, and installed app-proxy path before considering
  any deploy.
- Never publish the preview theme as part of an iteration loop.

Official references:

- https://shopify.dev/docs/apps/build/cli-for-apps/test-apps-locally
- https://shopify.dev/docs/apps/build/online-store/app-proxies
- https://shopify.dev/docs/api/shopify-cli/app/app-dev
