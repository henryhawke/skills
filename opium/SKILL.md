---
name: opium
description: "Deep, repository-wide completion auditing that reconciles a project's canonical manifest, plans, status, and audit records with current source, tests, migrations, CI, deployment, and device evidence. Use when the user invokes /opium or $opium, asks whether a codebase is complete, requests exhaustive gap or readiness analysis, wants the latest ten verification runs audited for totality, or needs an evidence-backed critical path for exactly what remains."
---

# Opium

Determine what is genuinely complete, what only appears complete, and the smallest exact critical path to the user's intended finish line. Optimize for warranted confidence, exhaustive traceability, and useful next actions—not a theatrical certainty percentage.

Before starting an audit, read [adaptive-orchestration.md](references/adaptive-orchestration.md), [audit-method.md](references/audit-method.md), and [report-contract.md](references/report-contract.md) completely. Apply repository-local `AGENTS.md` files and canonical project skills as higher-specificity constraints.

## Non-negotiable behavior

- Operate read-only unless the user separately authorizes implementation. Do not turn an audit request into fixes, commits, external writes, deployments, or messages.
- Preserve the dirty worktree. Record existing changes and submodule/gitlink state; never clean, reset, stage, or overwrite them.
- Separate specification completeness, source integration, local validation, candidate/CI proof, deployed-target proof, and physical-device or operational proof. Never collapse them into one “done” claim.
- Treat source, tests, graphs, documentation, CI, and historical records as different evidence classes. A plan is intent; a passing test is bounded evidence; a file's presence is not reachability; a historical pass is not proof for the current tree.
- Cite every consequential finding with a repository-relative path and line, symbol, command result, artifact/run identifier, or explicit unavailable-evidence note.
- Mark unknowns and unverified external state explicitly. Do not use “nothing found” as proof of absence unless the searched universe is defined and exhaustively covered.
- Do not create a one-off audit Markdown file in the repository unless the user asks and the repository's documentation policy permits it. Deliver the audit in the final response by default.

## Phase 0: Freeze the question and provenance

1. Capture repository root, current time/time zone, branch, `HEAD`, upstream relation, dirty paths, staged paths, untracked paths, submodules/gitlinks, and available toolchain versions relevant to validation.
2. Read root and nested instructions. Read the documentation manifest if one exists, followed by current status/audit documents and any project-local validation or rollout skills they identify.
3. Resolve the finish line. If the user does not name one, audit all completion dimensions independently instead of asking:
   - contract/specification closure;
   - implemented and runtime-reachable behavior;
   - local/source validation;
   - clean candidate and CI binding;
   - deployment/remote-target state;
   - device, canary, or operational proof.
4. State the audit boundary and exclusions. Include vendored repositories, gitlinks, generated code, infrastructure, migrations, mobile platforms, and remote systems only when the manifest or runtime architecture makes them part of the finish line.
5. Start a task plan. Keep synthesis owned by the root agent.
6. Create a temporary audit workspace outside the repository. Resolve this skill's folder and run `scripts/audit_ledger.py init --repo <repo> --out <temp>/ledger.json`. Keep agent shards and intermediate ledgers there; never put secrets, raw credentials, or prohibited project documentation in them.
7. Preflight available disk, temporary-directory writability, required binaries, credentials/targets, and expected validation cost before launching expensive checks. The ledger snapshot records free disk. Less than 1 GiB is a warning floor, not a universal requirement; use each project profile's actual needs and classify infrastructure exhaustion as blocked evidence rather than a repository test failure.
8. Choose `FULL` or `DEGRADED` audit mode. Use `FULL` by default. Use `DEGRADED` only for a hard time/token/tool/concurrency cap or inaccessible canonical universe; state the cap, preserve provisional denominators, and never emit a full-completion claim.

The ledger snapshot fingerprint binds all findings to `HEAD`, tracked changes, untracked-file content hashes, and submodule state. Recompute it after each wave. If the repository changes, identify the changed paths, invalidate affected observations, and re-verify them. Use graph change-detection tools at the beginning and end when available and blast radius matters.

## Phase 1: Compile the edict

Build an atomic requirement ledger before judging completion.

1. Establish source precedence from repository instructions. In the absence of a project-specific rule, use:
   - safety/security/release gates and explicit current status;
   - mounted runtime, registered handlers, current migrations/policies, and live configuration;
   - canonical manifest-owned product/API/testing documentation;
   - accepted plans and decision records;
   - historical audits, issue prose, comments, and commit messages.
2. Extract every normative or status-bearing statement: `must`, `shall`, `required`, acceptance criteria, active/parked/removed scope, exclusions, invariants, release gates, and “done when” clauses.
3. Split conjunctions into atomic edicts. Give each an ID and record:
   - requirement and completion dimension;
   - authoritative source path/line and precedence;
   - expected owning layers or paths;
   - observable acceptance evidence;
   - risk/severity and dependencies.
4. Record contradictions instead of silently choosing. Resolve them only through declared precedence and current source verification.
5. Add implementation-derived obligations that plans often omit: error paths, authorization, teardown, account switching, migration ordering, retries/idempotency, offline behavior, privacy logging, accessibility, generated-source parity, and parked-surface fail-closure.
6. Give each edict a proof-obligation vector rather than one premature status. Mark the applicable cells for contract consistency, mount/reachability, implementation, failure/negative behavior, lifecycle/teardown, security/privacy, focused tests, candidate/CI, and live/device evidence. See [adaptive-orchestration.md](references/adaptive-orchestration.md).

Bound the edict universe before assigning a denominator:

- Inventory every manifest entry and canonical source first; record entries read/total and exclusions in the ledger.
- Pass 1 extracts explicit completion, safety, privacy, release, active/parked, and acceptance edicts.
- Pass 2 adds only obligations logically necessary to make Pass 1 true across the architecture; label them `DERIVED` and cite the parent edict.
- Deduplicate equivalent requirements while retaining every source locator. Give stable IDs derived from canonical source identity and atomic requirement, not mutable row order.
- Exclude examples, aspirations, superseded/historical sections, and optional improvements from the applicable denominator unless current authority makes them requirements.
- In `DEGRADED` mode, call the discovered count `n discovered edicts`, never `n total edicts`, until the canonical source inventory is exhausted.

Write the bounded edict inventory to a temporary seed JSON and run `scripts/audit_ledger.py seed-edicts --ledger <temp>/ledger.json --input <temp>/edicts.json` before dispatching evidence shards. Seed dispositions as `UNASSESSED`; agents propose proof-cell states but never own final status.

Do not use the manifest as a file checklist. It is a registry and policy surface; each referenced contract must be tested against the implementation it claims to govern.

## Phase 2: Reconstruct the latest-ten check ledger

Interpret a “check” as one independently executed validation command, profile, workflow job, target probe, archive/device run, or formally recorded audit—not an individual test case and not a commit.

1. Discover the project's authoritative check sources in this order:
   - immutable local evidence artifacts or machine-readable run manifests;
   - CI/workflow runs bound to a commit;
   - canonical current status/audit ledgers;
   - project validation logs with timestamps and commands;
   - commit/PR prose only as a lead, never as proof of a pass.
2. Select the latest ten unique completed runs by execution time, not by textual order. Do not invent missing dates. If fewer than ten provable runs exist, report the exact number and the evidence-source gap.
3. For each run, capture command/profile, start/end time when known, exit result, exact commit/tree and dirty state, environment/target, suites and counts, skips/xfails/warnings, log completeness, artifact provenance, edict coverage, and freshness.
4. Audit “completed in totality” by checking that the declared profile actually ran every constituent command, every command reached a terminal result, logs are not truncated, no prerequisite or credential converted failure into skip, artifacts belong to the named tree, and success did not mask allowed failures.
5. Map every run to edict IDs. Identify repeated checks that create the illusion of coverage while entire completion dimensions remain untested.
6. Put undated or merely reported check claims in `undated_check_leads`, not the ordered ten. Preserve their evidence and what they allegedly covered, but do not infer execution order from document position, commit date, or surrounding prose.
7. When a run has a known tree, diff that tree to the audit snapshot. Map changed paths through ownership/call-impact evidence to determine which edict proofs remain valid and which are invalidated. Evidence decays by relevant change and environment drift, not age alone.

Import root-reconciled check evidence with `scripts/audit_ledger.py add-check-evidence --ledger <temp>/ledger.json --input <temp>/checks.json`; do not hand-edit the chronological and undated collections.

Never promote local/source checks into remote, deployment, archive, device, security-rotation, or operational proof.

## Phase 2.5: Schedule by uncertainty reduction

Do not assign agents by directory alone. Calculate which unanswered proof obligation has the highest expected value of information: impact × uncertainty × verdict leverage × evidence-independence, divided by inspection cost. Use the result to order agent shards and validation commands.

- Prioritize evidence that could change a blocker, contradiction, release verdict, or critical-path dependency.
- Prefer a new evidence method over another agent repeating the same search.
- Quarantine nice-to-have improvements that are neither canonical edicts nor necessary derived obligations. Opium audits required completion; it does not inflate “remaining” with speculative perfectionism.
- Maintain paired hypotheses for consequential rows: `H_done` and `H_gap`, with the cheapest decisive falsifier for each.
- Recalculate priorities after every wave. Stop launching duplicate low-value shards even when the nominal agent target has not been reached; explain the convergence decision.

## Phase 3: Deploy the audit mesh

Use subagents aggressively when the runtime provides them. Target 18–24 bounded logical assignments for a medium or large repository, dispatched in waves at the maximum safe concurrency. Scale down only for a genuinely small repository or a hard runtime/budget limit; disclose the reduction and resulting coverage limitation.

Every assignment must own unique edict cells or provide a genuinely independent verification method. Never spawn agents merely to inflate the count. Track assignments and observations in the temporary audit ledger.

### Model selection

- Inspect the subagent tool's advertised model overrides.
- Prefer `gpt-5.3-codex-spark` (or the runtime's exact advertised 5.3 Codex Spark identifier) for fast evidence-gathering and adversarial audit shards.
- If Spark is unavailable and the runtime advertises it, use `gpt-5.6-luna` with medium reasoning effort as the preferred fallback.
- Never pass an unadvertised model identifier. If neither Spark nor Luna is advertised, inherit an allowed model and disclose the substitution in the final confidence limits.
- Give each agent minimal task-local context, the relevant edict IDs, explicit owned paths/boundaries, and the required result schema. Avoid leaking the root agent's conclusions.
- Require the agent to echo the audit snapshot fingerprint. Reject or re-run results bound to a different snapshot.

### Wave A: independent evidence shards

Assign non-overlapping ownership across the repository's real boundaries. Cover at least:

- canonical contracts and contradiction extraction;
- latest-ten check provenance and totality;
- runtime entrypoints, routing, reachability, and parked/legacy surfaces;
- client/UI/state and accessibility;
- repositories, network boundaries, offline/cache teardown;
- backend actions, auth, validation, and error envelopes;
- database migrations, RLS/grants/RPCs, storage, and data lifecycle;
- privacy, abuse/safety, secrets, and fail-closed behavior;
- notifications, links, jobs, webhooks, and external integrations;
- tests, generated code, build profiles, CI, deployment, release, and device evidence;
- gitlinks/subprojects and documentation drift.

For an unusually large monorepo, split each boundary by service or edict group. For the Fart With Friends repository, use the exact active/parked surfaces and validation profiles named by `AGENTS.md`, `docs/MANIFEST.md`, `CURRENT_STATUS.md`, and `CURRENT_AUDIT.md` rather than inventing generic categories.

### Wave B: adversarial cross-checkers

After Wave A, dispatch fresh agents with raw artifacts and no intended answer:

1. **Done skeptic:** try to falsify all high-impact “verified complete” rows.
2. **Gap skeptic:** try to falsify claimed remaining work as stale, superseded, or already implemented.
3. **Coverage miner:** find edicts, layers, generated outputs, platforms, and negative space no shard covered.
4. **Temporal skeptic:** attack freshness, candidate binding, dirty-tree contamination, historical evidence, and latest-ten ordering.
5. **Boundary skeptic:** trace cross-layer, auth, lifecycle, failure, symmetry, and account-switch paths.
6. **Test skeptic:** identify assertions that do not prove runtime behavior, skipped prerequisites, weak mocks, and unexecuted profiles.

### Wave C: high-risk verification

Assign independent verification for every critical/high remaining item, contradiction, privacy/security boundary, destructive lifecycle, deployment claim, and negative/exhaustive claim. Use dedicated graph auditor/verifier profiles when available. Require exhaustive pagination and explicit parser/index/tool limitations for absence or dead-code conclusions.

The root agent must reconcile disagreements against current source and raw evidence. Do not average conflicting agent opinions or paste agent summaries into the final report unverified.

Require each agent to return the machine-checkable shard shape documented in [adaptive-orchestration.md](references/adaptive-orchestration.md), plus a short human synopsis. Merge shards with `scripts/audit_ledger.py merge-shard`; never let a shard directly overwrite the root edict disposition. The merge stores observations, while the root adjudicates them.

## Phase 4: Trace every edict through reality

For each edict, follow the full applicable chain:

`intent -> mounted entrypoint -> controller/provider -> domain/repository -> transport/handler -> database/storage/external boundary -> failure and teardown paths -> focused test -> candidate/live evidence`

- Use Semble first to locate where a behavior is implemented, then open the returned file/line directly. Do not repeat the discovery with grep.
- Use codebase-memory graph tools for architecture, symbol relationships, call paths, and change impact. Before trusting graph results, compare its branch/HEAD metadata and included file universe with the live repository snapshot. On the first structural query, check project/index status when the tool supports it. Treat indexing as an analysis-cache write: perform it only when repository instructions require it or the user's audit authority reasonably includes local analysis caching. After indexing, re-check live-HEAD parity. If parity still fails or docs/scripts/config are excluded, fall back to current source for those universes and forbid graph-backed exhaustive claims. Treat graph output as an index and verify consequential claims in current source.
- Use exhaustive literal search only for renamed symbols, forbidden vocabulary, route/action registries, TODO markers, configuration, or every occurrence of a known literal.
- Inspect both positive reachability and negative space: unmounted code, registered-but-unwrapped handlers, UI-only stubs, migrations without callers, tests for dead paths, active labels on parked code, and parked code reachable through aliases or background jobs.
- Verify platform/config/build inclusion. Source-only code does not become product behavior merely because it compiles.

Classify every edict as exactly one of:

- `VERIFIED_COMPLETE`: acceptance evidence closes every applicable layer on the audited tree.
- `PARTIAL`: meaningful implementation exists, but one or more required layers or acceptance proofs are absent.
- `MISSING`: required implementation or proof is absent.
- `CONTRADICTED`: current behavior conflicts with the authoritative contract.
- `BLOCKED_UNVERIFIED`: verification requires unavailable credentials, target, hardware, authority, or external state.
- `OUT_OF_SCOPE`: explicitly excluded from this finish line.
- `SUPERSEDED`: an authoritative later decision removed or replaced the edict.

An edict may be `VERIFIED_COMPLETE` only when every applicable proof-obligation cell is satisfied. For critical/high rows, require at least two independent evidence methods and a fresh adversarial attempt to disprove completion. Independently sample at least 10% of medium/low “complete” rows to detect systematic reviewer error.

## Phase 5: Attack the provisional answer

Apply every relevant heuristic in [audit-method.md](references/audit-method.md). At minimum perform:

- contract-to-code and code-to-contract bidirectional coverage;
- happy/failure/teardown/account-switch symmetry;
- active-versus-parked reachability analysis;
- auth/RLS/storage/deletion and privacy-data-flow closure;
- migration/deploy/config/generated-code ordering checks;
- duplicate implementation and semantic drift checks;
- test-oracle, skip, mock, and candidate-binding attacks;
- stale-evidence and negative-space searches;
- dependency and critical-path analysis for remaining work.

Run safe, repository-approved validation profiles that materially distinguish competing conclusions. Tie every result to the exact tree and environment. Do not run live mutations, deploy, rotate credentials, contact people, or alter production under an audit-only invocation.

After reconciling observations, write root-owned decisions to a temporary JSON and run `scripts/audit_ledger.py adjudicate --ledger <temp>/ledger.json --input <temp>/decisions.json`. Then run `scripts/audit_ledger.py validate --ledger <temp>/ledger.json --repo <repo>` and `scripts/audit_ledger.py summary --ledger <temp>/ledger.json`. Resolve every validation error; disclose warnings. Recompute the repository fingerprint and downgrade or re-run evidence if the snapshot changed.

## Phase 6: Synthesize the completion verdict

Use [report-contract.md](references/report-contract.md) exactly. Lead with the outcome and the finish-line distinction. Include:

1. completion verdict by dimension, never one blended percentage alone;
2. edict coverage and unresolved unknowns;
3. the latest-ten check ledger and totality verdicts;
4. verified completed capabilities;
5. contradicted, partial, missing, and blocked edicts;
6. an ordered remaining-work dependency graph/critical path;
7. implementation-ready work packets with owner paths, exact acceptance evidence, dependencies, and risk;
8. disagreements, stale evidence, tool/index limits, and confidence ceilings.

Only say “nothing remains” when every applicable edict is traced, all required evidence classes are current for the exact candidate, high-risk done claims survive independent falsification, the latest-ten ledger is complete, and no unknown or external gate remains. Otherwise state precisely what prevents that conclusion.

In `DEGRADED` mode, render the bounded report variant from [report-contract.md](references/report-contract.md): lead with usable provisional findings, label every denominator as discovered/sample coverage, omit claims about untouched universes, and provide the exact continuation plan required to reach `FULL` mode.
