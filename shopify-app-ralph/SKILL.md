---
name: shopify-app-ralph
description: Run a bounded Ralph-style implementation loop over a Shopify app's backend, embedded admin, app proxy, and theme app extension using `shopify app dev` and the Codex in-app Browser. Use when the user explicitly invokes `$shopify-app-ralph` or asks Codex to iteratively build, debug, or polish Shopify app frontend/backend behavior against a local dev server and development-store preview without waiting for a production or Cloud Run deploy.
---

# Shopify App Ralph

Iterate against one stable goal until its observable completion contract is true,
the bounded iteration limit is reached, or a real blocker needs the user.

## Start or resume the dev server

For Auctions, first inspect the Codex task terminal for a healthy matching dev
session. Reuse it when present. Otherwise, start this exact command
automatically in a persistent PTY from the Auctions repository root:

```shell
bun run dev:faux-auctions -- --store mrmaple-development.myshopify.com
```

Treat `mrmaple-development.myshopify.com` as the known non-production
development store for this workflow. The wrapper still runs `shopify app dev`
while providing the repository's bounded faux Lot reads. Do not start a second
matching session. Continue once the localhost and preview URLs appear. If
Shopify requires interactive authentication, approval, or other human input,
show the prompt and pause for the user.

For other repositories, ask the user to start the repository's Shopify
development command in the Codex task terminal, choose a non-production
development store, leave it running, and tell you when the localhost and preview
URLs appear. Do not start their interactive Shopify CLI process for them.

## Resume only after readiness

1. Read the Codex task terminal output when that surface is available. Do not
   ask the user to paste output already visible there.
2. Record the selected store, localhost app URL, Shopify preview or Dev Console
   URL, app-proxy storefront path, and theme-extension preview link. Never print
   credentials, signed query parameters, cookies, or tokens.
3. Confirm the selected store is a development store or otherwise explicitly
   non-production. Stop before browser interaction if it is the live merchant
   storefront.
4. Resolve this skill's directory and run
   `scripts/wait-for-http.mjs --url <localhost-url>`. Honor repository shell
   conventions around that command. Wait up to five minutes by default. A
   redirect or authentication response proves HTTP readiness; a 5xx does not.
5. If no localhost URL is visible, inspect the latest terminal output once
   more. Ask the user for the URL only when it cannot be discovered.
6. Read [references/shopify-dev-preview.md](references/shopify-dev-preview.md).
   In Auctions, also read [references/auctions.md](references/auctions.md).

Do not begin edits while the dev server is absent, still compiling, or serving
5xx responses.

## Establish the loop contract

Keep the user's task text stable through every iteration. Derive:

- one concrete goal;
- observable browser behavior for frontend work;
- focused automated gates for backend and shared behavior;
- a default limit of 8 implementation iterations unless the user sets another
  positive limit;
- any explicit completion promise.

Never claim a promise or completion condition until all named evidence is true.
Each iteration must produce new evidence, a scoped change, or a sharper failure
classification. Stop instead of repeating an unchanged failed approach.

## Select the proof surface

Use the development-store preview as the integration surface:

- Embedded admin: open the app preview URL emitted by `shopify app dev`.
- Storefront: open the development store's app-proxy path or theme-extension
  preview link, not the production Cloud Run URL.
- Theme app extension: use its development preview. Add or enable its block or
  app embed only on the preview/development theme; never publish a live theme.
- Backend-only changes: use focused tests first, then exercise the smallest
  relevant local/tunneled route. Use the Shopify storefront path when app-proxy
  signature or customer context is part of the behavior.

When app configuration automatically updates development URLs and the app proxy
uses a relative target, `shopify app dev` routes the selected development
store's proxy to the dev tunnel. Theme extension files are watched by the same
dev session. This is the fast path that avoids a Git push and Cloud Run upload.
Treat it as local/dev-store proof only.

## Use the Codex in-app Browser

For every frontend iteration, load and follow the available
`browser:control-in-app-browser` skill. The user explicitly selected the Codex
in-app Browser, so bind the in-app browser directly and do not substitute
Chrome, standalone Playwright, or a headless smoke script.

- Reuse one persistent browser binding and the existing site tab when possible.
- Read the browser's complete documentation before its first action.
- Open the dev-store preview URL and preserve its Shopify authentication.
- If authentication blocks the page, ask the user to sign in in the in-app
  Browser and wait for confirmation.
- Inspect visible UI, DOM-backed state, console errors, and relevant network
  failures. Do not inspect cookies, storage, passwords, or session secrets.
- Check at least one narrow mobile viewport and one common desktop viewport for
  responsive UI work.
- Reload the same page after the Shopify watcher reports the change ready.
  Avoid opening a new tab per iteration.

## Run one iteration

Repeat this sequence:

1. Inspect the exact failing or target state in the browser, test output, or
   local route response.
2. Discover the owning code using the repository's prescribed search routing.
   Read its agent instructions and preserve unrelated dirty changes.
3. Make the smallest coherent frontend/backend change. Do not weaken contracts,
   tests, permissions, tenancy, idempotency, or safety gates.
4. Run the narrowest relevant automated test, type check, generator check, or
   contract check.
5. Read the running dev terminal for rebuild errors. Wait for the local HTTP
   surface again when the server restarted.
6. Reload and exercise the development-store page in the in-app Browser.
   Verify the changed state plus one adjacent regression-sensitive state.
7. Record iteration number, changed files, gate result, browser result, and the
   next hypothesis in working commentary. Keep active project status in the
   repo's canonical artifact when its instructions require that; do not create
   a competing skill-state document.
8. Re-evaluate the completion contract. Continue only when another bounded
   iteration can materially improve the result.

Frontend and backend changes may be in the same iteration only when one behavior
requires both. Otherwise keep the loop narrow.

## Safety boundaries

- Never push, deploy, release an app version, publish a theme, or update Cloud
  Run merely to make the dev preview visible.
- Never run live Shopify mutations, customer-visible actions, provider sends,
  Firestore or Redis writes, Scheduler changes, secrets changes, or traffic
  changes without explicit authority for that exact action and environment.
- Prefer faux/read-only data for visual work. A local server using production
  credentials is not automatically safe to mutate.
- Treat a stopped tunnel, required sign-in, missing store access, or external
  dependency as a blocker after bounded retries; do not spin.
- Keep local tests, dev-store browser proof, deployed proof, and external
  sign-off separate.

## Finish

Stop when the completion contract is genuinely satisfied, the iteration limit
is reached, or a blocker requires user action. Report:

- outcome and iteration count;
- changed files;
- focused automated gates;
- browser paths and viewport/state coverage;
- remaining risks or exact blocker;
- explicit confirmation that no push, deploy, app release, or theme publication
  occurred unless the user separately authorized and requested it.

Do not leave a background dev server or browser watcher that Codex started. The
user-owned `shopify app dev` process may remain running for continued iteration.
