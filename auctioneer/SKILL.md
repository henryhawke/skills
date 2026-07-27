---
name: auctioneer
description: Runs bounded MrMaple Auctions bot-arena, Auction Doctor, and storefront realtime QA using a Ralph-style evidence loop and logical razors to isolate root causes and produce regression-tested fixes. Use only when the user invokes /auctioneer or explicitly asks to exercise auction bots, diagnose bid services, investigate auction failures, or verify frontend bid convergence.
disable-model-invocation: true
---

# Auctioneer

Exercise the Auctions bidding stack without confusing a local harness pass with
deployed proof or leaving synthetic state behind. Persist through ambiguity, not
through repeated unsafe mutations.

## Scope

This skill may:

- run `bot-arena` dry runs and bounded synthetic-lot simulations;
- run Auction Doctor service checks and stress scenarios;
- observe a published synthetic lot through the storefront;
- trace failures across transport, authority, durability, projection, realtime,
  and browser layers;
- implement the smallest invariant-preserving repair plus regression coverage;
- capture reports and cleanup readback.

It does not authorize deployment, traffic/config changes, live customer lots,
Shopify or SES effects, production launch claims, or manual weakening of a
fence, equality guard, contract, assertion, or audit record.

Read [reference.md](reference.md) before diagnosis, a published storefront run,
a deployed HTTP transport run, or cleanup beyond an arena event subtree. It
contains the razor decision table, iteration ledger, and deep-diagnosis
templates.

## Required inputs

Resolve these before any real write:

- canonical Auctions repository root;
- Git `HEAD`, branch, and clean/owned worktree status;
- canonical Shopify shop;
- Firebase project and Firestore database;
- Redis endpoint and whether it is local, isolated, or deployed;
- bot transport: `direct`, `api`, or `http`;
- storefront URL;
- exact duration, bots, rate, concurrency, and price ceiling;
- cleanup owner and post-run inventory method.

Default to an isolated non-production project/database. A production storefront
URL does not by itself authorize production Firestore, Redis, or bid writes.

## Model the authority chain

Trace every symptom through the same causal chain:

```text
intent -> route/transport -> Redis adjudication -> durable event/receipt
       -> Firestore projection -> poll/SSE snapshot -> browser transition
```

Name the earliest proven-good boundary and the first proven-bad boundary. Do not
jump from a browser symptom directly to a backend fix. A downstream mismatch is
often an effect of the first divergence, not a second root cause.

## Proof topology

Name the topology in every report:

| Transport | What it exercises | What it does not prove |
|---|---|---|
| `direct` + Firestore | local domain code against the selected Firestore database | deployed HTTP, deployed Redis, app-proxy auth, SSE |
| `direct` + Redis | local domain code, selected Redis, and Firestore drain | deployed Cloud Run or deployed Redis unless the endpoint is explicitly that service |
| `api` | local signed action/route harness | deployed app-proxy/network/runtime |
| `http` | deployed signed bid route at the named base URL | browser rendering or human task completion |
| storefront browser | deployed read model, live-session policy, poll/SSE behavior, and real UI state | backend ledger correctness by itself |

Do not combine results across different Redis instances or revisions as one
end-to-end pass.

## Apply the logical razors

Use these in order. Treat each razor as a question, not a verdict:

1. **Proof-boundary razor:** Can this topology actually prove the claim?
2. **Authority razor:** Which system is authoritative at this exact step?
3. **First-divergence razor:** What is the earliest observation that differs
   between a passing and failing path?
4. **Invariant razor:** Does the hypothesis require weakening a fence,
   equality guard, tenant binding, idempotency rule, or strict decoder? Reject
   it if so.
5. **Temporal razor:** Which failure happened first? Later timeouts, drain
   errors, and reconnect warnings may be cascade noise.
6. **Conservation razor:** If durable events and replay agree, investigate
   projection/transport/UI before changing adjudication.
7. **Occam razor:** Prefer one defect that explains several symptoms, but keep
   it only while a discriminating probe supports it.
8. **Popper razor:** Prefer the cheapest safe probe that could falsify the
   leading hypothesis.
9. **Reversibility razor:** Prefer read-only probes, focused tests, and small
   patches over broad configuration or data changes.
10. **Reproduction razor:** No reproducible signal means no root-cause or fix
    claim.

Never use a razor to discard contrary evidence. Mark facts, inferences,
unknowns, ruled-out hypotheses, protected concurrent drift, and external
blockers separately.

## Run the Ralph loop

“Ralph” means persistent, bounded learning. It does not mean repeating the same
command until it happens to pass.

For each iteration:

1. **Pin:** Re-read `HEAD`, topology, bounds, worktree ownership, and active
   cleanup state. Preserve other agents' files.
2. **Normalize:** State one symptom, one violated invariant, and one smallest
   red-capable command or observation.
3. **Ledger:** Freeze facts and artifacts before interpretation. Record the
   first failure, not only the final summary.
4. **Hypothesize:** Rank three to five falsifiable causes by evidence fit,
   safety impact, information value, and probe cost.
5. **Probe:** Change one variable or add one observation. Choose the probe most
   likely to distinguish the top hypotheses.
6. **Explain:** Update the authority-chain timeline. A useful result eliminates
   a hypothesis, moves the first-divergence boundary, or reveals missing
   observability.
7. **Repair:** After cause is localized, add a positive regression that fails
   for the observed case, then make the smallest invariant-preserving code
   change.
8. **Verify:** Run the regression, the original reproduction, a relevant
   negative/invariant case, and the narrow owning suite. Broaden only after
   focused proof is green.
9. **Decide:** Continue only when the next iteration has new information value.
   Otherwise stop with the evidence gap and smallest safe next probe.

Default to at most six diagnostic/code iterations and one real-write rerun per
unchanged hypothesis. A user-authorized larger budget does not relax safety
boundaries. Stop immediately on corruption, ambiguous accepted mutation,
tenant drift, non-arena targeting, uncontrolled cleanup, or mixed revision/
authority uncertainty. Stop after three repeated external-infrastructure
failures with no new information.

Before claiming a fix, require:

- the new regression failed against the defective behavior and passes now;
- the original symptom no longer reproduces in the same proof topology;
- no guard, threshold, assertion, decoder strictness, or cleanup check was
  weakened to obtain green;
- correctness, latency, realtime, lifecycle, and cleanup are reported
  independently;
- the causal explanation accounts for both the failure and the recovery;
- current source and status were re-read to avoid overwriting another lane.

## Operating workflow

### 1. Establish the boundary

1. Read `AGENTS.md`, `README.md`, `Worklist.md`, and the bidding/storefront
   facades.
2. Record `git rev-parse HEAD`, `git branch --show-current`, and
   `git status --short`.
3. Use one bounded AgentMemory recall, then Semble for behavior discovery and
   CodeGraph after a real symbol appears.
4. Keep reports outside the repository unless the user explicitly asks to
   update a canonical evidence artifact.
5. Start the iteration ledger from [reference.md](reference.md).

### 2. Dry-run the exact bounds

```shell
./bot-arena \
  --project=<PROJECT> \
  --database=<DATABASE> \
  --shop=<SHOP> \
  --backend=<redis|firestore> \
  --transport=<direct|api|http> \
  --duration=5s \
  --bots=6 \
  --rate=25 \
  --concurrency=6 \
  --max-price-cents=25000 \
  --dry-run \
  --json \
  --report-dir=<TMP_REPORT_ROOT>
```

Require exit `0`, zero writes, zero errors, and a written report. A dry run is
scheduler/report proof only; it is not capacity or service proof.

### 3. Probe services without bids

```shell
./auction-doctor \
  --shop=<SHOP> \
  --project=<PROJECT> \
  --database=<DATABASE> \
  --checks-only \
  --report-dir=<TMP_REPORT_ROOT>
```

Record Firestore read latency, Redis endpoint/role/version, persistence posture,
PING, pub/sub RTT, and all warnings. Explicitly label a localhost Redis result
as local integration evidence.

### 4. Run a hidden Doctor sweep

Start narrow:

```shell
./auction-doctor \
  --shop=<SHOP> \
  --project=<PROJECT> \
  --database=<DATABASE> \
  --backend=both \
  --duration=5s \
  --bots=4 \
  --rate=2 \
  --concurrency=2 \
  --max-price-cents=25000 \
  --report-dir=<TMP_REPORT_ROOT>
```

Stop after the first reproducible data-corruption, cross-tenant, cleanup, or
ambiguous-outcome failure. Do not improve a red result by skipping the failing
scenario.

Enforce a bounded outer timeout. If Doctor prints its final report but remains
alive, stop the process, record a non-exit/open-handle defect, and inventory
cleanup before continuing.

### 5. Verify storefront convergence

Use a published arena only when the target is explicitly approved and cleanup
is owned.

1. Create the synthetic lot with `--prepare-only --publish-arena`.
2. Record the exact `eventId`, `lotId`, initial price/version/count, and time.
3. Open the exact storefront lot URL and record the initial summary plus
   realtime/poll status.
4. Start a bounded bot run against that exact arena lot.
5. Observe at least two intermediate states without reload and one final state.
6. Require monotonic price, version, and bid count.
7. Capture whether the UI used SSE, reconnecting/poll fallback, or a disabled
   bid control.

Never force-click a disabled bid control. A human-versus-bots test is valid only
when the browser and bots use the same authoritative backend topology. If the
page says it is reconnecting while values still change, report poll convergence
as passed and realtime admission as failed/degraded.

### 6. Verify ledger and latency separately

Require:

- gap-free, unique accepted sequences;
- projection/replay equality;
- Redis/Firestore equality when Redis is in scope;
- accepted acknowledgements backed by durable events;
- no duplicate or phantom acknowledgement;
- zero unexplained errors;
- latency and achieved-rate thresholds evaluated independently of ledger truth.

A correct ledger with multi-second writes is a correctness pass and a
performance failure.

### 7. Cleanup and read back

Run the supported cleanup:

```shell
./bot-arena \
  --project=<PROJECT> \
  --database=<DATABASE> \
  --shop=<SHOP> \
  --cleanup-only \
  --json
```

Require `status=completed`, `matched=deleted`, `skipped=0`, and `remaining=0`.
Then independently inventory tenant-level artifacts for the exact run prefix.
Never infer cleanup scope from a success label. Inspect the current cleanup plan
and prove removal of every artifact it owns. Event-subtree cleanup does not by
itself prove removal of global audit, rate-limit, idempotency, lock,
viewer-activity, outbox, customer-projection, or Redis records.

Do not manually delete durable audit/idempotency records from a shared or
production environment. Treat any leftover as a cleanup failure. Use an
isolated database that can be discarded, or first implement and review a
fenced full-state cleanup path.

Finally reload the storefront hub and verify the synthetic event is absent.

## Failure routing

### Persisted storefront viewer activity projection is invalid

Inspect `parseStorefrontViewerActivityProjection` and the persisted synthetic
row. Add a positive decoder test before changing code. One previously observed
failure passed the viewer-only `isViewerBid` key into the strict public-row
decoder, whose exact-key allowlist rejected it. Treat that as a hypothesis until
current source and the failing payload confirm it.

### Redis drain-churn errors

Do not accept an error count without causes. Preserve the first drain exception
and classify it. Compare the first successful and first failing drain, including
sequence, projection payload, fence, lease, and viewer binding. One shared
projection decoder defect can cause later drain errors, but do not assume that
without the first exception.

### Storefront reconnecting with changing values

The poll fallback is converging, but realtime authority admission or SSE is not
green. Confirm the bot's Redis instance, deployed Redis instance, Firestore
sequence, live-session decision, and feature/proof flags. Recovery requires a
fresh authoritative snapshot; changing values from Firestore polling alone do
not prove Redis authority or SSE admission.

### Doctor prints a report but does not exit

Audit every Redis client, duplicate subscriber, delta subscription, and
per-scenario dependency. Capture active-handle evidence, close resources in
`finally`, and prove natural exit under a bounded outer timeout. Do not rely on
forced process exit as the fix.

### Ledger replay differs across phases

Compare phase-local accepted events with the lot's pre-phase durable sequence.
A verifier that replays only the current phase but compares against the
cumulative lot projection can report false corruption. Fix the verifier's
baseline or use a fresh lot; never weaken sequence equality.

### Multi-second writes labeled PASS

Separate connectivity from service quality. A successful write may prove reachability
while still failing a declared latency budget. Make thresholds explicit and
fail the performance dimension without reclassifying ledger correctness.

### Missing payload in a rejected bot acknowledgement

Keep the raw response status/envelope sample. Do not count it as an ordinary
domain rejection until the harness proves the response shape is intentional.

## Handoff

Report:

- exact Git SHA, project/database/shop, Redis endpoint class, transport, and
  storefront URL;
- commands and report paths;
- observed state transitions with timestamps;
- correctness, performance, realtime, API, cleanup, and process-lifecycle
  results as separate lines;
- concrete failure signatures and owning source symbols;
- the first-divergence timeline, ranked hypotheses, eliminated causes, and the
  probe that localized the defect;
- why existing tests missed the case and the regression that now prevents it;
- storefront/event cleanup readback;
- remaining tenant-level artifacts;
- proof boundaries and the smallest safe next test or repair.

Do not append to `launch/evidence.md` unless the run is candidate-, revision-,
environment-, and approval-bound.
