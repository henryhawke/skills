# Opium Report Contract

## Contents

1. Required order
2. Verdict table
3. Latest-ten ledger
4. Remaining-work packets
5. Confidence statement

## 1. Required order

Lead with a direct outcome in two to four sentences:

- the closest defensible completion claim;
- the finish-line dimensions that are not complete;
- the highest-leverage blocker or contradiction;
- whether the audited tree changed during analysis.

Then report sections in this order:

1. **Completion verdict**
2. **Latest ten checks**
3. **What is verified complete**
4. **What remains**
5. **Critical path**
6. **Contradictions and unknowns**
7. **Confidence and coverage limits**

For `DEGRADED` audits, insert a banner immediately after the lead: `Bounded audit — not a repository-wide completion verdict`. Replace global coverage denominators with discovered/inspected counts, add **Uninspected universe** and **Continuation to full audit**, and do not say the listed remaining work is exhaustive.

Use concise tables where repeated fields make comparison easier. Keep evidence next to the claim it supports. Use clickable absolute local-file links when the client supports them.

Do not omit a required section because its evidence universe is empty; state “none proven” or the exact unavailable-evidence boundary. Keep `UNKNOWN`/`BLOCKED_UNVERIFIED` distinct from `MISSING`: inaccessible proof is not proof that implementation is absent.

## 2. Verdict table

Use one row per finish-line dimension:

| Dimension | Verdict | Strongest evidence | Blocking gap | Confidence |
| --- | --- | --- | --- | --- |
| Contract/specification | Complete/Partial/Missing/Contradicted/Blocked | source | gap | High/Medium/Low |
| Runtime/source | ... | ... | ... | ... |
| Local validation | ... | ... | ... | ... |
| Candidate/CI | ... | ... | ... | ... |
| Target/deployment | ... | ... | ... | ... |
| Device/operations | ... | ... | ... | ... |

Below the table, state:

- edict disposition coverage (`n/N`);
- implementation trace coverage (`n/N`);
- current validation coverage (`n/N`);
- critical/high independent verification (`n/N`);
- unresolved unknown count;
- contradictions count.

Do not average the dimensions into a “percent complete” unless the user explicitly asks. If asked, show the weighting and preserve the dimension table because a single release blocker can dominate hundreds of finished low-risk rows.

## 3. Latest-ten ledger

List newest first:

| # | Executed at | Check/profile | Tree/target | Result | Totality | Edicts covered | Invalidated or missing evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

Rules:

- Include only provable completed runs.
- If fewer than ten exist, keep missing rows out of the table and state `Found n/10` prominently.
- Distinguish pass/fail from totality. A passing wrapper can still be `PARTIAL`.
- Name skips, warnings, absent credentials, missing logs, dirty-tree state, and later invalidating changes.
- Summarize systemic insight after the table: duplicated coverage, untouched dimensions, stale clusters, and whether the ten runs converge on the actual remaining risks.

Follow the ordered table with **Undated reported check leads** when present. These are not rows 1–10. Show the claimed command/result, provenance locator, missing timestamp/run binding, and the proof needed to promote each lead into the chronological ledger.

## 4. Remaining-work packets

Every remaining item must be implementation-ready:

```text
R1 — concise outcome [Critical/High/Medium/Low]
Why it remains: edict IDs and current disposition
Evidence: exact paths/lines, symbols, commands, or missing artifact
Change surface: specific modules/layers; avoid speculative file lists
Dependencies: predecessor item IDs or external prerequisites
Acceptance: exact observable checks needed to move the edict to VERIFIED_COMPLETE
Proof class: E2/E3/E4/E5 required
Confidence: High/Medium/Low and disconfirming evidence
```

Order packets by the real dependency graph:

1. safety/privacy/security and irreversible data risks;
2. requirements or architecture contradictions;
3. foundational schema/API/runtime boundaries;
4. user-visible and lifecycle completeness;
5. validation, candidate, deployment, and device gates;
6. documentation reconciliation and cleanup.

Separate code work from proof-only work. “Rerun tests,” “deploy,” “rotate credentials,” and “perform device smoke” are different work packets with different authority and evidence.

Include a compact critical path such as:

`R1 contract decision -> R2 schema/runtime closure -> R4 focused tests -> R6 clean candidate/CI -> R8 approved target -> R9 physical device -> release verdict`

For work that can proceed in parallel, group packets into waves and name collision boundaries.

## 5. Confidence statement

End the audit itself with:

- strongest warranted claim;
- specific reasons confidence is not higher;
- exact uninspected or inaccessible universes;
- tool/index/parser truncation and pagination status;
- actual model/reasoning assignments, any runtime substitution or governing model restriction that affected coverage, and how many logical agent assignments completed;
- whether the worktree changed during the audit;
- the one next action most likely to change the verdict.

Avoid “near-perfect,” “fully complete,” “all good,” or “nothing else” unless the skill's strict stop condition is met. Prefer: “High confidence for current source closure; low confidence for release readiness because target and device evidence are absent.”

Before sending, verify each verdict row and remaining-work packet against its cited evidence. Every evidence note must say both what it proves and, where easily confused, what stronger evidence class it does not prove.
