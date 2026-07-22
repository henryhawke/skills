# Adaptive Orchestration

## Contents

1. Audit state machine
2. Proof-obligation vectors
3. Expected value of information
4. Agent portfolio construction
5. Independence and adversarial quorum
6. Machine-checkable shard format
7. Convergence rules

## 1. Audit state machine

Run Opium as a closed-loop evidence system:

1. **Snapshot:** bind the audit to repository and environment provenance.
2. **Enumerate:** compile atomic edicts and required proof-obligation cells.
3. **Hypothesize:** record `H_done`, `H_gap`, and decisive falsifiers.
4. **Schedule:** rank uncovered or conflicting cells by expected value of information (EVI).
5. **Gather:** dispatch bounded agents or run decisive validations.
6. **Ingest:** merge observations into the ledger without automatically changing dispositions.
7. **Adjudicate:** root agent resolves evidence, contradictions, and confidence ceilings.
8. **Attack:** fresh agents try to falsify high-impact decisions using independent methods.
9. **Converge:** stop only when further work cannot materially change a verdict within the authorized evidence universe.
10. **Emit:** validate the ledger and render the report contract.

Re-enter scheduling whenever a contradiction appears, the repository snapshot changes, or a check proves partial rather than total.

### Full versus degraded mode

`FULL` means the canonical source inventory is exhausted, every applicable edict has a proof vector, every required audit wave or equivalent method completed, and the latest-ten evidence universe is exhausted within stated access. `DEGRADED` is a legitimate bounded audit under a hard resource, time, tool, credential, hardware, or access cap.

In degraded mode:

- record the cap and the exact uninspected universe;
- use “discovered edicts” and “inspected paths,” never an implied global denominator;
- preserve high-confidence local findings that have direct evidence;
- cap negative/exhaustive and full-completion claims;
- omit adversarial quorum claims for waves that did not run;
- produce a continuation queue ranked by EVI;
- never relabel missing external evidence as implementation work.

## 2. Proof-obligation vectors

Represent each edict as the subset of these cells that its finish line requires:

| Cell | Question |
| --- | --- |
| `CONTRACT` | Is the requirement authoritative, atomic, internally consistent, and not superseded? |
| `MOUNT` | Is the behavior registered, enabled, built, deployed in the relevant inventory, and reachable from an approved entrypoint? |
| `IMPLEMENT` | Does current source implement the required happy path across applicable layers? |
| `NEGATIVE` | Do malformed, unauthorized, offline, blocked, expired, duplicate, and partial-failure paths fail correctly? |
| `LIFECYCLE` | Are cleanup, teardown, deletion, cancellation, account switch, restart, and retry semantics complete? |
| `SECURITY` | Are auth, RLS/grants, storage, privacy propagation, secrets, and abuse boundaries closed? |
| `TEST` | Does a focused current test observe the meaningful outcome without mocking away the claim? |
| `CANDIDATE` | Is proof bound to a clean exact candidate and CI/build artifact? |
| `LIVE` | Is the required approved target, archive, device, canary, scheduler, or operational behavior observed? |

Each cell has one state:

- `SATISFIED`: evidence reaches the required class.
- `UNSATISFIED`: evidence shows the obligation is not met.
- `UNKNOWN`: applicable but not currently provable.
- `NA`: not required for this edict/finish line.

Record evidence and counterevidence per cell. Derive the edict disposition only after the vector is complete. This prevents a passing unit test from hiding absent mounting or live proof.

## 3. Expected value of information

Score candidate investigations on a small ordinal scale:

```text
EVI = (impact × uncertainty × verdict_leverage × independence_bonus) / cost
```

- `impact` (1–5): user harm, privacy/security, data loss, release blocking, or architectural blast radius.
- `uncertainty` (1–4): disagreement, weak provenance, missing layer, stale evidence, or tool truncation.
- `verdict_leverage` (1–3): likelihood that the result changes a completion dimension, critical path, or edict disposition.
- `independence_bonus` (1–2): new source/method vs correlated repetition.
- `cost` (1–5): time, tool expense, setup, credentials, hardware, or external dependency.

Do not pretend the arithmetic is probabilistic. It is a scheduling heuristic. Override it for mandatory safety gates, cheap decisive checks, or dependency prerequisites, and record why.

For each consequential edict, write:

```text
H_done: strongest defensible completion hypothesis
Falsify_done: cheapest observation that would disprove it
H_gap: strongest defensible remaining-work hypothesis
Falsify_gap: cheapest observation that would show it is stale/superseded/already complete
Next_probe: highest-EVI evidence action
```

## 4. Agent portfolio construction

Build assignments from uncovered proof cells, then pack adjacent cells by runtime locality. A good assignment has:

- a bounded path, service, data domain, or evidence source;
- explicit edict IDs and proof cells;
- one primary question and its opposing hypothesis;
- a defined search universe and pagination rule;
- a unique verification method;
- an output budget and machine-checkable return shape;
- no authority to edit repository or external state.

Prefer one fresh subagent per logical assignment to reduce context correlation. Reuse an agent only for a tightly scoped follow-up on its existing evidence. Respect the runtime concurrency limit by dispatching sequential waves; logical assignment count is not simultaneous agent count.

Size the portfolio by unique proof obligations, not repository prestige or a fixed agent quota:

- small/narrow: 3–6 logical assignments;
- medium: 8–14 logical assignments;
- large, multi-service, or high-risk: 14–24 logical assignments.

Start at the low end and expand only while high-EVI uncovered cells remain. Within the selected portfolio, use these approximate allocations:

- **35–50% primary mapping:** contracts, runtime boundaries, data domains, tests, and check history.
- **20–30% cross-layer closure:** call paths, lifecycle, security/privacy, generated/config/deploy agreement.
- **20–25% adversarial falsification:** done skeptic, gap skeptic, temporal skeptic, test skeptic, negative-space miner.
- **10–15% independent verification:** critical/high adjudication and sampled medium/low completion claims.

The ranges and percentages are guidance, not completion criteria. Reallocate toward uncertainty hotspots. Never duplicate a shard because an earlier agent was merely concise; ask a focused follow-up instead.

Follow user and repository model policy. Inherit the parent model by default; use only currently advertised overrides, and reserve stronger permitted reasoning for high-risk adjudication or adversarial verification. Record the actual model/effort and any substitution. Never weaken the shard definition or proof requirements because the model changed.

## 5. Independence and adversarial quorum

Count two observations as independent only when they differ materially in evidence source or method, for example:

- direct source trace vs executed focused test;
- client-to-handler call path vs database/RLS authorization trace;
- local clean candidate vs CI artifact attestation;
- registered inventory enumeration vs negative reachability search;
- source implementation proof vs fresh adversarial counterexample search.

Two agents quoting the same status paragraph are one evidence path. Two semantic searches over the same index are correlated. Graph results and current source verification are related but distinct only when the source is actually opened and inspected.

Quorum for critical/high `VERIFIED_COMPLETE`:

1. direct current implementation evidence;
2. applicable focused validation or stronger live evidence;
3. a fresh falsification attempt that found no contradiction within a stated exhaustive universe.

Quorum for critical/high `MISSING` or `CONTRADICTED`:

1. authoritative edict proof;
2. bounded exhaustive absence/current contradictory behavior proof;
3. supersession and alternate-implementation check.

## 6. Machine-checkable shard format

Agents should write or return JSON shaped like:

```json
{
  "schema_version": 1,
  "agent_run": {
    "id": "wave-a-private-send",
    "snapshot_fingerprint": "sha256...",
    "model": "advertised model actually used",
    "reasoning_effort": "actual effort or inherited",
    "scope": ["edict:E-001:IMPLEMENT", "path:lib/..."],
    "method": "source_trace",
    "exclusions": [],
    "tool_limits": []
  },
  "observations": [
    {
      "edict_id": "E-001",
      "cell": "IMPLEMENT",
      "proposed_state": "SATISFIED",
      "claim": "Concise falsifiable claim",
      "evidence": [{"kind": "source", "locator": "lib/file.dart:42", "note": "What this proves"}],
      "counterevidence": [],
      "disconfirmation": "Strongest reason this could be wrong",
      "confidence": "HIGH"
    }
  ],
  "checks": [],
  "undated_check_leads": [],
  "unknowns": []
}
```

Use one observation per edict cell. An agent may propose; only the root adjudicates. Evidence locators must be precise and must say what they prove. `tool_limits` must record truncation, stale indexes, missing credentials, inaccessible targets, unpaged results, or parser gaps.

Latest-ten check entries use:

```json
{
  "id": "stable run/job identifier",
  "executed_at": "ISO-8601 or UNKNOWN",
  "profile": "command/workflow/profile",
  "tree": "commit and dirty state",
  "target": "local/CI/target/device",
  "result": "PASS|FAIL|CANCELLED|UNKNOWN",
  "totality": "TOTAL|PARTIAL|INVALID_FOR_CLAIM|PROVENANCE_UNKNOWN",
  "skips": [],
  "warnings": [],
  "edict_ids": [],
  "evidence": []
}
```

## 7. Convergence rules

Continue when any of these is true:

- an applicable proof cell is `UNKNOWN` without an explicit external blocker;
- critical/high evidence lacks an independent method or adversarial pass;
- two credible observations conflict;
- latest-ten ordering or totality may change with accessible evidence;
- a high-EVI safe probe remains;
- repository snapshot changed after evidence collection;
- a tool result was truncated and supports an exhaustive/negative claim.

Stop when:

- all applicable cells are adjudicated;
- remaining unknowns are genuinely inaccessible or outside authorized scope;
- all critical/high quorums are met;
- the latest-ten universe is exhausted or its boundary is explicit;
- the next safe probe has low verdict leverage and would duplicate existing evidence;
- the validated ledger can generate every required report section.

Record the stop reason. “Many agents agree” and “agent budget exhausted” are not evidentiary convergence; the latter is a disclosed coverage limit.
