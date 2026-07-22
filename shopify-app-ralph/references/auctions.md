# Auctions fast path

Use only when the current repository is the standalone Auctions app. Verify
these facts against current files before relying on them.

## Current routing handles

- `package.json`:
  - `bun run dev` wraps `shopify app dev` with server instrumentation.
  - `bun run dev:faux-auctions` supplies bounded faux storefront Lots and then
    runs the same Shopify development flow.
- `shopify.app.toml`:
  - `[build] automatically_update_urls_on_dev = true`
  - `[app_proxy] prefix = "apps"`, `subpath = "auctions"`,
    `url = "/apps/auctions"`
- `extensions/auction-storefront/shopify.extension.toml` declares a theme app
  extension.
- Its Liquid blocks and loader use the relative `/apps/auctions` root, so a
  development store can route storefront requests through the CLI dev tunnel.

Open `https://<selected-dev-store>/apps/auctions` or the theme-extension preview
URL from Shopify CLI. Do not point extension code directly at localhost and do
not deploy Cloud Run for ordinary dev-store iteration.

## Surface-specific checks

- Storefront UI: run the affected `test:storefront` slice and any owning
  snapshot/live-session generator check, then use the in-app Browser.
- Embedded admin: run the affected `test:admin` family and use the embedded app
  preview.
- Domain/bidding/backend: follow the repository change-routing table and run the
  narrowest owning suite before browser integration.
- Generated storefront assets: run the owning generator and keep source plus
  generated output together.

Faux mode is suitable for layout and read-path iteration; it is not deployed
proof and does not authorize Shopify, Firestore, Redis, SES, Scheduler, or other
external mutations.
