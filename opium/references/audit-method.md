# Opium Audit Method

## Contents

1. Evidence ladder and confidence ceilings
2. Coverage accounting
3. Edict extraction
4. Deep audit heuristics
5. Latest-ten totality tests
6. Agent result contract
7. Stop conditions

## 1. Evidence ladder and confidence ceilings

Use the strongest applicable evidence level for each claim:

| Level | Evidence | What it can prove |
| --- | --- | --- |
| E0 | Missing, ambiguous, or contradictory | Nothing; retain as unknown or contradiction |
| E1 | Plan, issue, comment, commit prose, historical summary | Intent or a lead only |
| E2 | Current source/config/migration/static analysis | Presence and bounded static behavior |
| E3 | Focused tests run on the exact tree | Tested behavior within the test oracle and environment |
| E4 | Clean candidate build and CI artifacts bound to the exact commit | Reproducible candidate/source validation |
| E5 | Approved target, archive, device, canary, or operational evidence | Only the exact live/physical behavior observed |

Apply ceilings, not optimistic averages:

- A dirty or unidentified tree cannot receive high candidate/release confidence.
- Doc-only or commit-message-only claims stay low confidence.
- Source/static checks cannot prove deployment, RLS on a target, signed archives, physical permissions, push delivery, scheduler execution, or two-account device flows.
- A passing test with mocks cannot outrank the boundary it mocks.
- A skipped prerequisite creates an evidence hole even when the surrounding command exits zero.
- Historical evidence loses current-proof value after relevant code, config, migrations, toolchains, credentials, targets, or release inputs change.
- An unresolved critical contradiction or unknown caps the affected completion dimension at low confidence.

Use confidence bands (`HIGH`, `MEDIUM`, `LOW`) with reasons. If a numeric score helps ranking, never present it without numerator, denominator, weights, and ceiling conditions.

## 2. Coverage accounting

Report these separately:

- **Edict disposition coverage:** applicable atomic edicts with a verified status / total applicable edicts.
- **Implementation trace coverage:** edicts traced across every applicable runtime layer / applicable edicts.
- **Validation coverage:** edicts with current acceptance evidence on the audited tree / applicable edicts.
- **Latest-ten provenance coverage:** recent runs with complete command/tree/environment/result provenance / runs found, and runs found / 10.
- **Independent verification coverage:** critical/high claims reviewed by at least two independent paths / total critical/high claims.
- **Unknown count:** unresolved edicts, external gates, truncated searches, inaccessible logs, and unverified subprojects.

Weight priority by harm and critical-path importance, not file count. Never let many low-risk complete rows hide one release-blocking unknown.

## 3. Edict extraction

Convert prose into falsifiable rows. Example:

> “Private sends must be online-only and never queue coordinates.”

Split into at least:

1. Private send refuses while offline.
2. Refusal produces explicit user-facing state.
3. Refusal writes no pending send queue entry.
4. Send requests contain no coordinates.
5. Analytics/logging/notifications also contain no coordinates.
6. Focused tests prove refusal and non-persistence.

For each row, define the observation that would disprove it. This converts a checklist into a falsification program.

Add derived edicts for:

- input validation and malformed states;
- unauthenticated, unauthorized, blocked, deleted, expired, and stale identities;
- retries, duplicate delivery, cancellation, and partial failure;
- sign-out, account switch, deletion, backgrounding, and app restart;
- cache, queue, temporary file, signed URL, token, listener, and subscription teardown;
- migration ordering, rollback compatibility, grants, policies, triggers, and quotas;
- registration/mounting/build/deploy inventory and feature flags;
- accessibility, localization, error copy, loading/empty states, and reduced-motion behavior;
- privacy propagation through requests, storage, logs, analytics, notifications, and third parties.

## 4. Deep audit heuristics

### Bidirectional closure

- **Contract -> code:** every edict maps to implementation and proof.
- **Code -> contract:** every mounted route, handler, job, table, RPC, flag, external call, and product-visible string maps back to an allowed contract.
- Investigate orphan code and orphan contract rows separately.

### Reachability and registration

- Trace from actual entrypoints, not filenames.
- Compare route registries, handler/action maps, deploy inventories, scheduled jobs, feature flags, dependency injection, providers, platform build settings, and deep-link normalizers.
- Find source that is present but unmounted, and parked code that remains reachable indirectly.
- Verify background, retry, notification-tap, universal-link, compatibility-alias, and cold-start paths.

### Cross-layer agreement

- Compare models, serializers, repositories, RPC signatures, Edge validation, migrations, RLS/grants, storage paths, and test fixtures field by field.
- Look for nullable/required drift, enum drift, renamed fields, default-value disagreement, error-envelope mismatch, pagination mismatch, and ownership ambiguity.
- Verify generated code is current and checked by drift detection.

### Symmetry and lifecycle

- Pair create/delete, subscribe/unsubscribe, start/stop, sign-in/sign-out, account A/account B, enable/disable, success/failure, online/offline, foreground/background, grant/revoke, save/remove, retry/dead-letter, and migration/cleanup.
- State surviving its owner is a likely privacy or correctness defect.
- Check async results are fenced to the initiating account/session and cannot repopulate purged state.

### Security and privacy

- Trace identity and authorization at every trust boundary; UI gating is never authorization.
- Compare handler auth, service roles, RLS, grants, RPC `SECURITY DEFINER`, object paths, signed URL scope/TTL, webhook verification, admin provenance, and deletion behavior.
- Search requests, serialization, logs, analytics, notifications, caches, queues, crash reports, and map/network payloads for prohibited sensitive fields.
- Verify failure closes access rather than falling back to a broader read/write path.

### Data and migration integrity

- Read append-only migrations in order. Check function redefinitions, policy replacement, grants after replacement, trigger lifecycle, constraints, indexes, cleanup jobs, storage policies, and deploy ordering.
- Prove current schema state, not just the intent of the latest migration.
- Inspect idempotency, leases, fencing, retry limits, dead letters, quotas, and concurrent mutation paths.

### Tests and validation skepticism

- Confirm the test executes the mounted production path and asserts the meaningful outcome.
- Identify mocks that bypass serialization/auth/RLS/storage/platform behavior.
- Inspect skipped, excluded, quarantined, flaky-retried, expected-failure, snapshot-only, count-only, and compile-only checks.
- Compare test names with assertions; a named behavior is not evidence if no assertion observes it.
- Look for duplicate tests that inflate counts without broadening edict coverage.
- Confirm every validation profile command ran and the wrapper propagates non-zero exits.
- Apply a counterfactual oracle test: would this test still pass if the implementation returned a constant, skipped authorization, ignored teardown, or never mounted the feature? If yes, it does not prove the named edict.

### Temporal and provenance attacks

- Bind evidence to commit SHA, dirty diff, submodule/gitlink SHA, build configuration, dependency lockfiles, migration inventory, target ID, and relevant credentials/flags.
- Diff each evidenced tree to the audit snapshot and map changed paths to edicts using current ownership/call-impact evidence. Re-run or downgrade only the affected proof cells; do not discard unrelated strong evidence merely because it is old.
- Distinguish “passed once,” “passes current local tree,” “passes clean candidate,” “CI-bound,” “deployed,” and “device-proven.”
- Treat copied counts and prose summaries as pointers until raw evidence corroborates them.
- Keep undated reported passes outside the chronological latest-ten ledger. Store them as leads until an execution timestamp or immutable run identifier supplies orderable provenance.

### Tool and environment integrity

- Compare graph/index branch and HEAD metadata to the live Git snapshot before structural reliance, and re-check after an index refresh.
- Record graph parser coverage; docs, scripts, configs, generated sources, migrations, gitlinks, or languages absent from the index remain separate universes.
- Preflight disk, temp space, tools, dependencies, credentials, target access, simulator/device access, and network requirements before validation.
- Classify ENOSPC, missing tool, unavailable credential, inaccessible target, or runner outage as an evidence-infrastructure blocker. Do not call the repository check failed unless its assertions actually ran and failed.

### Negative space and semantic drift

- Search for forbidden/legacy vocabulary, compatibility aliases, stale environment keys, old route names, TODO/FIXME/HACK markers, no-op handlers, placeholder values, broad catches, ignored futures, disabled tests, and unowned configuration.
- Search both exact terms and semantic equivalents. Use exhaustive literal searches only when the universe is appropriate and report truncation or exclusions.
- Compare documentation examples and scripts with current command names and runtime configuration.

### Completion heuristics

High-information warning signs include:

- more documentation detail than executable acceptance evidence;
- a large passing-test count paired with few boundary or failure-path assertions;
- “active” code behind an unmounted route/flag or absent deploy inventory;
- “parked” behavior whose table/job/alias still permits writes;
- a success wrapper that tolerates skips, missing tools, or missing credentials;
- current source claims supported only by older commit/candidate artifacts;
- cleanup without account fencing, or create without delete/expiry;
- tests added in the same change that restate implementation internals;
- repeated audit prose whose original logs are missing;
- a repository called complete while remote target, archive, device, or credential gates remain unknown.

## 5. Latest-ten totality tests

For each discovered run, answer:

1. Is it a real completed execution or only a planned/reported command?
2. What exact tree, dirty state, dependencies, subprojects, target, device, and configuration did it test?
3. Did the wrapper execute every declared constituent check?
4. Did each constituent reach a terminal state with captured exit status?
5. Were any checks skipped, allowed to fail, retried, quarantined, filtered, or silently omitted?
6. Are logs complete and artifacts cryptographically or structurally bound to the run?
7. Did environment or credential absence reduce the scope?
8. Which edicts and completion dimensions did the run actually cover?
9. What relevant changes occurred afterward?
10. What conclusion is this run incapable of supporting?

Classify each run `TOTAL`, `PARTIAL`, `INVALID_FOR_CLAIM`, or `PROVENANCE_UNKNOWN`.

## 6. Agent result contract

Require every shard to return compact structured findings:

```text
SCOPE: owned paths, edict IDs, exclusions
COVERAGE: inspected universe, pagination, tool/index limitations
FINDINGS:
- ID | status | severity | claim
  evidence: path:line / symbol / command / artifact
  counterevidence: ...
  implication: ...
  next proof or fix: ...
UNKNOWNS: unavailable evidence and why
DISCONFIRMATION: strongest reason this shard may be wrong
```

Reject findings with no evidence, vague “looks good” language, unbounded absence claims, or recommendations that do not name an acceptance test.

## 7. Stop conditions

Stop expanding the audit only when:

- every applicable edict has one disposition;
- every critical/high claim has independent verification;
- every repository/runtime boundary has an owner and coverage record;
- contradictions are resolved or explicitly retained;
- the latest-ten ledger is exhausted or its missing provenance is reported;
- safe decisive validations have run or are named as blocked;
- further inspection is duplicative and would not change a disposition or confidence ceiling.

Do not stop merely because many agents agree. Correlated agents reading the same incomplete evidence are one evidence path, not many.
