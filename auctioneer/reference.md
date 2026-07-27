# Auctioneer diagnostic reference

Read this file for published storefront tests, deployed HTTP tests, and cleanup
design. Use it during every Ralph iteration when the symptom spans more than one
authority layer.

## Iteration ledger

Create one compact entry per iteration:

```text
Iteration:
Pinned HEAD / branch:
Owned files / concurrent drift:
Topology and endpoints:
Write bounds / cleanup owner:

Symptom:
Violated invariant:
Smallest red signal:
Earliest proven-good boundary:
First proven-bad boundary:

Facts:
Inferences:
Unknowns:
Ruled out:
External blockers:

Ranked hypotheses:
1.
2.
3.

Chosen probe:
Why this probe has the best information gain:
One variable changed:
Result / artifact:
What was eliminated or localized:

Regression added:
Repair and changed files:
Focused verification:
Original reproduction:
Negative/invariant verification:
Cleanup readback:
Next decision:
```

Do not rewrite an old entry after the result changes. Append the next iteration
so the causal path remains auditable.

## Hypothesis scoring

Rank hypotheses with a lightweight score rather than intuition alone:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Evidence fit | contradicts a fact | explains part | explains all current facts |
| First-divergence fit | downstream only | boundary-adjacent | exactly at boundary |
| Safety relevance | cosmetic | degraded | threatens authority/invariant |
| Probe information | ambiguous | eliminates one cause | separates several causes |
| Probe cost/risk | mutation/high cost | bounded integration | read-only/focused test |

Favor strong evidence, boundary fit, and information gain. Favor lower
cost/risk when scores are otherwise close. Do not turn the score into fake
certainty; record the counter-evidence beside each leading hypothesis.

## Razor decision table

| Noise pattern | Razor | First move |
|---|---|---|
| UI changes but says reconnecting | Proof boundary | Split poll convergence from SSE admission |
| Several failures after one exception | Temporal | Preserve and inspect the first exception |
| Ledger correct, browser wrong | Conservation | Inspect projection, snapshot acceptance, and transport |
| Projection wrong, durable events correct | Authority | Diff reducer output against persisted projection |
| Redis and Firestore disagree | Invariant | Stop writes; inspect fence, watermark, lease, and drain |
| Only stress run fails | Contrast | Compare first passing and failing operations, not averages |
| A fix requires lowering a threshold | Invariant | Reject it; determine whether the system or threshold contract is wrong |
| Many plausible causes remain | Popper | Run the probe that gives different outcomes for the top causes |
| Failure disappears on retry | Reproduction | Preserve raw artifacts and recreate a minimal deterministic signal |
| Cleanup says success but artifacts remain | Authority | Compare the cleanup manifest with exact post-readback |
| Process reports complete but stays alive | Temporal | Capture active handles after final report |

## First-divergence worksheet

For a single bid, record the same operation identity at each layer:

| Layer | Required evidence |
|---|---|
| Intent | bidder, lot, amount, idempotency key, request hash |
| Route | authenticated shop/actor, parsed request, response envelope |
| Redis | decision, sequence, version, fence, lot state, outbox identity |
| Durability | accepted event, receipt, request binding, committed sequence |
| Projection | price, leader, count, version, viewer/public row |
| Realtime | authority admission, SSE frame identity, reconnect reason |
| Poll | snapshot source, sequence/version, acceptance decision |
| Browser | DOM state, bid-control state, message, transition time |

Compare a passing and failing bid at the earliest layer that has comparable
facts. Once divergence is found, inspect its immediate writer and decoder before
searching farther downstream.

## Evidence classes

| Class | Minimum binding |
|---|---|
| Local dry run | Git SHA, command, local environment, report |
| Local integration | Git SHA, exact Firestore/Redis endpoints, command, report |
| Deployed read-only | immutable revision, URL, environment/config readback |
| Deployed mutation | revision, shop/project/database, approval window, bounds, cleanup owner |
| Browser | URL, account state, viewport, initial/intermediate/final DOM facts |
| Provider | provider identity, allowlist, acceptance/readback |
| Launch | all required candidate/environment/rehearsal/sign-off evidence |

Never promote one class into another.

## Storefront observation sheet

Record:

```text
Event:
Lot:
Browser URL:
Observed at:
Initial current bid / count / version:
Realtime message:
Bid control enabled:

Bot start:
Intermediate 1:
Intermediate 2:
Bot end:
Final current bid / count / version:

Reload used:
SSE evidence:
Poll fallback evidence:
Console errors:
Ledger result:
Cleanup result:
Hub after cleanup:
```

Changing price/count without reload proves client convergence, but not SSE. A
visible reconnect warning means the realtime path remains degraded even when
polling succeeds.

## Artifact inventory

For the exact synthetic `eventId` and `lotId` prefixes, inventory at least:

- `auctionEvents` and descendants;
- `auctionAdminAudit`;
- `auctionBidRateLimitBuckets`;
- `auctionBidWriteIdempotency`;
- `auctionBidWriteLocks`;
- `auctionStorefrontViewerActivities`;
- outbox and secondary-effect obligations;
- customer-lot/account projections;
- version clocks and receipts;
- Redis lot state, sequence, outbox, lease, and pub/sub-related keys.

Report counts by collection and Redis key family. Do not dump private customer
data or secrets.

## Known diagnostic lessons

### Strict viewer decoder

Strict decoders turn privacy and schema boundaries into executable contracts.
When a valid viewer row fails, compare its exact keys with the public subset
passed to the nested decoder. A previously observed failure allowed
`isViewerBid` to remain in a public-row-shaped object, causing the public exact
key allowlist to reject it. Confirm the current payload before applying that
repair.

The positive regression shape is:

```ts
expect(parseStorefrontViewerActivityProjection(validViewer, expected))
  .toEqual(validViewer);
```

Keep negative tests for privacy expansion, extra keys, and binding drift. Do not
make the public decoder accept viewer-only fields.

### Cleanup scope

Cleanup proof has two parts: the planned manifest and independent post-readback.
Recursive deletion of an event document proves only the event/lot subtree.
Exact run-bound cleanup may also own side collections, but it must fence every
query by shop plus run/event/lot identity and report skipped or ambiguous rows.
Prefer an isolated disposable database until every synthetic artifact family
has an owned, reviewed deletion path.

### Latency interpretation

Measure separately:

- Firestore read probe;
- bid acknowledgement;
- Redis outbox drain;
- Redis delta receipt;
- browser-visible convergence.

Multi-second bid acknowledgement or fanout is a performance failure even when
the ledger eventually converges. Localhost Redis PING does not explain deployed
Cloud Run-to-Redis performance.

For contention, retain per-operation rows and compare:

- base Firestore writes without bot contention;
- adjudication time;
- lock/transaction wait;
- durable acknowledgement time;
- outbox drain and projection time;
- browser convergence time.

Do not infer the slow layer from end-to-end p95 alone.

### API topology

`direct` and `api` use current local source. `http` exercises the deployed
route only when signed with the correct app-proxy secret and pointed at the
actual deployed base URL. A browser on `mrmaple.com` and local direct bots can
observe the same Firestore projection while still using different Redis
authorities; label that as a mixed-topology test.

### Cross-phase ledger verification

A lot reused across phases has a cumulative durable sequence. A phase-local
verifier must either replay from the phase's starting event/sequence or seed its
expected state from the durable pre-phase baseline. Comparing only new events
with the cumulative projection creates a false corruption signal. Preserve
strict equality; correct the observation window.

### Realtime recovery

Poll convergence and realtime recovery are different contracts. A reconnecting
client may continue receiving Firestore projections while Redis authority is
unavailable. Require the same authoritative backend topology, a fresh accepted
snapshot, and an explicit live-session transition before enabling bidding.

### Process lifecycle

When a tool prints its final report but does not exit, the report is not process
success. Capture active handles or likely resource owners, then inspect Redis
clients/subscribers, Firestore clients, timers, streams, and per-scenario
dependencies. Prove natural exit; a forced `process.exit()` only hides leaks.

## Fix-quality review

Before accepting a repair, answer:

1. Which exact invariant was violated?
2. Which fact localized the first divergence?
3. Which alternative explanations were falsified?
4. Did the regression fail on the defective behavior?
5. Does the patch repair the owner of the invariant instead of a downstream
   symptom?
6. Were strictness, fences, thresholds, and cleanup checks preserved?
7. Does the original reproduction now pass in the same topology?
8. What evidence remains local-only, mixed-topology, deployed, or unproven?
9. Why did existing tests miss the case?
10. What is the smallest next probe if any uncertainty remains?

## Stop conditions

Stop immediately for:

- any non-arena lot or real customer bidder identity;
- price, duration, rate, concurrency, or target boundary breach;
- Redis/Firestore sequence mismatch;
- ambiguous accepted mutation;
- tenant-scope violation;
- viewer projection corruption;
- incomplete event cleanup or unexpected side artifacts;
- deployed service/revision uncertainty;
- three repeated external infrastructure failures.
