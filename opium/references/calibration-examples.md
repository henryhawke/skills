# Opium Calibration Examples

Use these examples only to resolve recurring classification ambiguity. Apply the audited repository's own finish line and evidence rules first.

## 1. Passing local tests do not prove release readiness

**Evidence:** focused tests pass on the current dirty tree; no clean candidate, CI artifact, deployment identity, or target readback is available.

**Classify:** local validation may be complete for the covered edicts. Candidate/CI and target/deployment remain `BLOCKED_UNVERIFIED` or incomplete as appropriate. Do not say “launch-ready.”

## 2. Present source is not mounted behavior

**Evidence:** a handler exists and has unit tests, but no route registry, job schedule, dependency-injection binding, build inventory, or caller reaches it.

**Classify:** `IMPLEMENT` may be `SATISFIED`; `MOUNT` is `UNSATISFIED` or `UNKNOWN`. The edict is not `VERIFIED_COMPLETE`.

## 3. A reported pass without provenance is not a latest-ten run

**Evidence:** a status document says “full validation passed,” but supplies no execution time, immutable run ID, complete log, tree binding, or target.

**Classify:** store it as an `undated_check_lead`. Do not place it in chronological rows 1–10 or use it as current E3/E4 proof.

## 4. Absence requires a bounded universe

**Evidence:** one semantic search returns no match, while generated code, configuration, migrations, and a gitlink were not indexed.

**Classify:** `UNKNOWN`, with the excluded universes named. Do not claim the behavior or obligation is absent repository-wide.

## 5. Prompt adaptation is not audit execution

**Request:** “Rewrite this completion-audit prompt for this repository using $opium.”

**Classify:** `PROMPT_ONLY`. Return a complete ready-to-paste prompt tailored with verified repository facts. Do not run the audit, modify the target repository, or present speculative findings.

## 6. Proof-only work is not implementation work

**Evidence:** current source and focused tests close an edict, but the required approved-target or device observation is unavailable.

**Classify:** keep the code edict separate from the missing E5 proof. Create a proof-only remaining-work packet with the required authority, target, and observation; do not recommend code changes without contrary implementation evidence.

## 7. Tailored prompts preserve repository tool policy

**Evidence:** the target repository's `AGENTS.md` requires initializing a structural index when absent, while a generic audit template says “never create analysis caches.”

**Classify:** the repository-specific instruction wins. Write a conditional, scoped cache rule that permits the required initialization, records its coverage, and handles generated artifacts according to repository policy. Do not copy the contradictory generic prohibition into the tailored prompt.
