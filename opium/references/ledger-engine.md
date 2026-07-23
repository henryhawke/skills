# Opium Ledger Engine

Use `scripts/audit_ledger.py` as the deterministic evidence boundary for an
Opium audit. Keep working payloads and ledgers in the temporary audit workspace,
not in the audited repository.

The engine uses only Python's standard library. Schema version `1` remains the
wire format for ledgers and agent shards. Engine version `2` adds stricter
validation, transactional mutations, richer summaries, and fingerprint version
`3`.

## Lifecycle

Run commands in this order:

```text
init
-> seed-edicts
-> validate-shard / merge-shard
-> add-check-evidence
-> adjudicate
-> validate
-> summary
```

Inspect the installed command and enum contract when generating payloads:

```shell
python scripts/audit_ledger.py schema
```

### Initialize

```shell
python scripts/audit_ledger.py init \
  --repo /absolute/repository \
  --out /temporary/audit/ledger.json
```

Initialization records:

- exact Git root, branch, `HEAD`, upstream, and ahead/behind counts when present;
- porcelain-v2 status;
- separate tracked, staged, and unstaged binary-diff hashes;
- content hashes for every reported untracked file;
- initialized and unavailable submodule state;
- Git/tool errors and free disk;
- one deterministic snapshot fingerprint.

Fingerprint version changes invalidate older ledgers intentionally. Reinitialize
instead of rewriting a historical fingerprint.

### Seed the bounded edict universe

```shell
python scripts/audit_ledger.py seed-edicts \
  --ledger /temporary/audit/ledger.json \
  --input /temporary/audit/edicts.json
```

Seed once. Include a non-empty finish line, source boundary, atomic edicts,
acceptance evidence, all nine proof cells, and an acyclic dependency graph.
Use `manifest_entries_total: 0` when no manifest exists. A final `FULL` ledger
requires an explicit total, equal read count, and exhausted canonical sources.

### Preflight and merge shards

Validate each shard against the ledger before merge:

```shell
python scripts/audit_ledger.py validate-shard \
  --ledger /temporary/audit/ledger.json \
  --shard /temporary/audit/shard.json \
  --json
```

Then merge:

```shell
python scripts/audit_ledger.py merge-shard \
  --ledger /temporary/audit/ledger.json \
  --shard /temporary/audit/shard.json
```

The engine rejects:

- stale snapshot fingerprints;
- unknown edicts and out-of-scope observations;
- multiple observations for the same edict cell within one run;
- malformed or evidence-free satisfied/unsatisfied claims;
- conflicting check and lead identifiers;
- duplicate run or observation identifiers.

Merge assigns stable observation IDs such as `run-id:obs:1`. Use those IDs in
root adjudication. A failed merge leaves the in-memory and on-disk ledger
unchanged.

### Add check evidence

```shell
python scripts/audit_ledger.py add-check-evidence \
  --ledger /temporary/audit/ledger.json \
  --input /temporary/audit/checks.json
```

Keep only timezone-aware, orderable executions in `checks`. Put prose claims or
runs without timestamps/tree bindings in `undated_check_leads`. The engine
sorts newest first, retains the latest ten unique records, verifies referenced
edict IDs, and treats `TOTAL` as execution totality rather than a synonym for
`PASS`.

### Adjudicate

```shell
python scripts/audit_ledger.py adjudicate \
  --ledger /temporary/audit/ledger.json \
  --input /temporary/audit/decisions.json
```

Require a reason, complete obligation vector, and valid same-edict observation
references for each decision. Apply all decisions atomically. If any decision
is invalid, apply none.

For critical/high `VERIFIED_COMPLETE`, record at least:

1. a current implementation/source method;
2. a focused validation, candidate, runtime, or live method;
3. a fresh adversarial/falsification method.

Distinct labels without materially independent evidence do not satisfy the
method contract.

### Validate and summarize

```shell
python scripts/audit_ledger.py validate \
  --ledger /temporary/audit/ledger.json \
  --repo /absolute/repository \
  --json

python scripts/audit_ledger.py summary \
  --ledger /temporary/audit/ledger.json
```

Pass `--repo` for final validation so repository drift is detected. Validation
returns exit `0` when no errors exist and exit `2` for invalid input or ledger
state. Warnings preserve usable results while naming confidence ceilings.

Summary reports:

- disposition and risk counts;
- proof-cell states;
- per-dimension dispositions;
- edict, implementation-trace, validation, high-risk quorum, and latest-ten
  coverage ratios with explicit numerators and denominators;
- remaining edict IDs, contradictions, unknowns, and check totality;
- a conservative `ready_for_full_completion_claim` boolean and exact reasons
  it remains false.

Treat the readiness boolean as a final consistency guard, not a substitute for
the report contract or root judgment.

## JSON safety and durability

The engine rejects duplicate JSON keys, `NaN`/infinite values, non-object root
payloads, and files larger than 16 MiB. Mutating commands validate a deep copy
and replace the ledger only after the whole operation succeeds. File writes use
same-directory temporary files, `fsync`, and atomic replacement.

## Verification

Run both layers:

```shell
python scripts/audit_ledger.py self-test
python -m unittest -v scripts/test_audit_ledger.py
```

The smoke test verifies the packaged CLI workflow. The regression suite covers
fingerprint drift, JSON safety, shard scope, transaction rollback, dependency
cycles, high-risk quorum, latest-ten ordering, final-scope rules, and summary
accounting.
