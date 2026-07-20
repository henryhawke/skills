---
name: iterate
description: Ralph-style simulator iteration loop — build the app, drive every screen/flow in the iOS Simulator (signup, sign-in, friends, sends, listen/reaction, map, saved, profile, settings), screenshot and evaluate each against the product contract, fix the worst finding, rebuild, and repeat until the checklist is genuinely green. Use when asked to /iterate, iterate on screens/UX in the simulator, or visually polish the app end to end.
---

# /iterate — simulator iteration loop

You are entering a Ralph-Wiggum-style loop: the same objective is fed back to you every iteration until it is **genuinely complete**. Your memory between iterations is the filesystem: the journal, the screenshots, and git history. Read them before doing anything.

**Objective:** every flow in the manifest runs end-to-end in the iOS Simulator, every screen passes its evaluation criteria, and the full checklist has been green for **two consecutive iterations**.

**Completion promise:** you may output `ITERATE COMPLETE: all manifest flows green twice` ONLY when that statement is unequivocally true. Never output it to escape the loop. If you are blocked, output `ITERATE BLOCKED: <reason>` with exactly what a human must do, and stop.

## State (create on first iteration, read on every one)

- `.iterate/journal.md` — append one section per iteration: number, build SHA, flows run, per-screen verdicts, findings (severity-ordered), what you fixed, what's next. This file is your memory; write it as if the next iteration is a stranger.
- `.iterate/shots/<iter>/<flow>-<screen>.png` — screenshot evidence per screen per iteration. Never commit shots containing real personal data.
- `.iterate/checklist.md` — the living pass/fail matrix (flows × criteria). Green-twice is measured here.

## Preflight (every iteration, cheap)

1. `xcode-select -p` and `xcrun simctl list devices available` must succeed. If Xcode/simctl is unusable, output `ITERATE BLOCKED: no usable Xcode on this host` — do not fake it with widget tests.
2. `flutter doctor -v` shows an iOS toolchain; `flutter analyze --no-pub` is clean before you build (fix or stop if not — never iterate on a broken tree).
3. **Target safety:** the app must point at an attested **non-production** Supabase target. Never run this loop against production. Use disposable test accounts (see `lib/core/scripts/create_test_users.dart` in FWF); never type real credentials into the simulator.
4. Boot two simulators for two-account flows: `xcrun simctl boot "iPhone 16" ; xcrun simctl boot "iPhone 16 Plus"` (any two available devices). Install with `flutter run -d <udid> --profile` or `flutter build ios --simulator && xcrun simctl install <udid> <app>`.
5. Check `git status --short` — other agents may be working this tree. Never sweep their files into your commits.

## Driving the UI (tier in this order)

1. **Deterministic:** Flutter `integration_test` targets driven via `flutter test integration_test/<flow>_test.dart -d <udid>` — prefer these for flows that already have them; add thin ones when a flow is undrivable otherwise.
2. **Exploratory:** [Maestro](https://maestro.mobile.dev) if installed (`maestro test <flow>.yaml`) — tap by visible text/semantics; keep flow YAMLs in `.iterate/flows/`.
3. **Primitives:** `xcrun simctl io <udid> screenshot <path>` (evidence), `xcrun simctl openurl <udid> <deeplink>` (routes/short links), `xcrun simctl push <udid> <bundle-id> payload.json` (notification taps), `xcrun simctl status_bar`/`location` (clean shots, journal location fixtures), Settings app for permission resets (`xcrun simctl privacy <udid> reset all <bundle-id>`).
4. Airplane-mode flows: use `xcrun simctl status_bar ... --dataNetwork hide` for visuals but test real refusal by pointing the app at an unreachable host or toggling the Mac network — verify the app's explicit refusal state, not just the icon.

## Flow manifest (FartWithFriends default)

When run in the fartwithfriends repo, the contract is `docs/plan/05-beta-contract.md` (plus the overrides section in `docs/plan/02-frontend-screen-plan.md`) — read both before iteration 1. Flows, in order:

1. **Fresh signup** — auth → consent → onboarding (Fart Tag, privacy education, local rehearsal) → completes with zero friends and no camera/mic OS prompts during onboarding.
2. **Welcome fart** — arrives as a real Inbox row + notification on the fresh account; clearly labeled house sender; reaction capture absent on it.
3. **Sign-in / session** — sign out, sign back in, account switch between the two test accounts; no stale account data flashes.
4. **Friends** — search (min 2 chars), send request from account A, accept on account B, invite link path, blocked-users surface.
5. **Send** — record via center button, one-recipient chooser (recent friends first), send; **no map-posting option anywhere**; no location prompt ever in this flow.
6. **Offline refusal** — attempt a send with no connectivity: immediate explicit refusal, nothing queues, no fake success.
7. **Incoming** — notification tap → Incoming: tap **Listen** (no camera), then hold **Listen + React** (camera consent → capture → preview sole-hero → effects → send); verify backgrounding discards; verify sender never sees any listen-without-reaction trace.
8. **Reaction card + Fart Back** — sender watches the clip, plays original audio, Fart Backs; the reply lands as a new Incoming.
9. **Journal Map** — first `/map` visit triggers the location permission ask (and only there); after granting, a new send records a pin; map shows own history full-bleed; empty states honest; Settings "Record fart locations" toggle works.
10. **Saved** — save a received fart, direct play/pause on the card, rename, pin, remove.
11. **Profile & Settings** — own profile; other-user profile shows Add Friend/Accept as primary; settings toggles (reaction consent, journal recording, notification prefs incl. "Fun notifications" off → generic previews).
12. **Deep links** — invite link and `/l/<code>` short link land correctly through auth.

## Per-screen evaluation criteria (every screenshot)

- **Contract:** matches its screen contract in `docs/plan/02` + the 05 overrides (journal-only map, listen-only first-class, one recipient, no banned surfaces).
- **Hierarchy (80/20):** one hero per screen; spectacle only at the Fart action, hold gesture, delivery success, reaction preview; lists/settings/errors calm; unselected dock tabs recede.
- **Copy:** approved vocabulary only (Fart Map, Inbox, Listen, Watch, Fart Back, Send Reaction); no `volley`/`drops`/`stink vault`/Bank-economy language; empty states funny and fart-adjacent, not generic.
- **States:** loading, empty, error, offline, permission-denied each reachable and honest; no dead ends without an escape.
- **Accessibility:** 48dp targets, sensible semantics, no clipped text at 200% scale (spot-check one flow per iteration with `xcrun simctl ui <udid> content_size extra-extra-large`), reduced-motion respected.
- **Privacy tells:** camera indicator only when capturing; pin indicator when journal-recording; no coordinates in any network request (spot-check with a proxy or debug log when touching map/send code).

## The loop

Each iteration: **read journal → preflight → build/install → run the manifest (or the subset invalidated by last fix) → screenshot + evaluate → update checklist → pick the worst finding → fix it in source → `flutter analyze` + focused tests → commit (one finding-fix per commit, message `iterate(N): <what>`) → append journal → next iteration.**

Rules:
- Fix the **worst** finding first (crash > contract violation > privacy tell > dead state > copy > polish), one or two per iteration — small verified steps beat big rewrites.
- Re-run a flow after fixing it; never mark green from memory or from a stale screenshot.
- If the same finding survives three fix attempts, stop treating it as yours: journal it as `STUCK`, move on, and surface it in the final report.
- Never "fix" by weakening the contract, deleting the check, or hardcoding simulator-only behavior.
- Respect human gates: anything touching live targets, credentials, TestFlight, or migrations on a shared target is `ITERATE BLOCKED`, not yours to force.
- Default max iterations: 10 (override via argument). On hitting the cap, write a final journal section ranking remaining findings and output the blocked/summary line.
