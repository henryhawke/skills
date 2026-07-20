---
name: iterate-code
description: Codebase-only Ralph loop — decompose an objective into small verifiable work units, complete and verify them one per iteration with evidence-first discipline, and track both progress and the meta of the run (velocity, stuck patterns, drift) in a persistent ledger. Use when asked to /iterate-code, grind through a backlog/plan, or autonomously work a codebase to completion without a UI/simulator.
---

# /iterate-code — codebase Ralph loop

Same objective fed back every iteration until genuinely complete. No simulator, no UI — source, tests, and tooling only. Your memory is the filesystem: the ledger, the journal, and git history. An iteration that didn't update the ledger didn't happen.

**Completion promise:** output `ITERATE-CODE COMPLETE: all ledger items done or explicitly deferred` ONLY when literally true. If blocked on something only a human can do, output `ITERATE-CODE BLOCKED: <exact ask>` and stop. Never emit either to escape the loop.

## State files

- `.iterate/ledger.md` — the work queue. One line per unit: `[state] ID — title | acceptance: <command or named check> | evidence: <last result>`. States: `todo`, `doing` (max ONE at a time), `done`, `stuck`, `blocked-human`, `deferred`. This is the single source of truth for progress; never track progress only in your head or the chat.
- `.iterate/journal.md` — one section per iteration: what you did, evidence observed, what you learned, note-to-future-self. Plus a **META** block (see below).
- Git history — commit per green unit, message `iterate(N): <unit ID> <what>`. History must stay bisectable: every commit analyzes/builds clean.

## Iteration 0 — bootstrap (only if the ledger doesn't exist)

1. Read the objective and its source documents fully. (In `fartwithfriends`, the backlog source is `docs/plan/05-beta-contract.md` §12 plus the Session Handoff in `docs/plan/README.md` — do not invent a parallel plan.)
2. Decompose into the **smallest independently verifiable units** — a unit is too big if you can't name its acceptance command, too small if verifying it proves nothing. Order leaf-first by dependency.
3. For every unit, write the acceptance check **before any code**: a test command, an analyzer/typecheck gate, a grep that must return empty, a script exit code. "Looks right" is not an acceptance check.
4. Write the ledger; commit it.

## Every iteration

1. **Re-orient (fresh eyes, ~2 min):** read the ledger, the last two journal sections, and `git log --oneline` since the last journal entry — other agents or your past self may have moved things. Reconcile the ledger to reality before working: a `done` claim you can't tie to a commit and evidence gets demoted back to `todo`.
2. **Select:** exactly one `todo` unit — the highest-priority unblocked one. Mark it `doing`. Never hold two `doing` items; never start a new unit to avoid finishing a hard one.
3. **Verify-first:** run the unit's acceptance check now, before changing anything. If it already passes, mark `done` with evidence and select again (inherited work is real work). If it fails, you now have the exact target.
4. **Work small:** implement in the smallest diffs that could move the check. Run focused tests as you go, the full affected-domain check before commit. Match surrounding style; no drive-by refactors — if you spot adjacent debt, add it to the ledger as a new unit instead of fixing it inline.
5. **Verify with evidence:** re-run the acceptance check and read its actual output. Green from a stale run, a skipped test, or a weakened assertion is not green. Forbidden moves: deleting/skipping a failing test to pass, loosening the contract the check encodes, rerunning flaky checks until they happen to pass (fix or ledger the flake instead).
6. **Commit** the unit atomically (source + tests + docs it touched). Mark `done` with the evidence line. If other agents share the tree, stage explicit paths only.
7. **Journal**, including a one-line note-to-future-self: the thing you'd want to know if you woke up here with no memory.

## Stuck protocol

- Three genuine fix attempts on the same failure → mark `stuck` with the exact failing evidence and your best hypothesis, then **move on**. Grinding a stuck item burns iterations that other units could use, and the answer often falls out of later work.
- Revisit `stuck` items only when something material changed (a dependency landed, new information in the journal). Two revisits later, escalate to `blocked-human` with a precise question.
- Distinguish *stuck* (you can't make the check pass) from *blocked-human* (credentials, approvals, product decisions, live targets). Never force the latter; never park the former as the latter to avoid hard work.

## META block (append to the journal every 3 iterations)

Answer honestly, in four lines:
- **Velocity:** units done per iteration, trending up or down? If down two checks in a row, your units are too big — re-split.
- **Drift:** re-read the original objective; does the ledger still serve it, or have you been optimizing something adjacent? Kill drifted units.
- **Patterns:** any failure appearing across units (same flaky harness, same misunderstood API)? Fix the *cause* once as its own unit instead of paying it per-unit.
- **Regression canary:** re-run the acceptance check of one random `done` unit. If it fails, something you did since broke it — that's the new top priority, and a sign your checks are too narrow.

## Ending

Cap at 15 iterations by default (override via argument). On completion, cap, or block: write a final journal section — done/deferred/stuck/blocked table with evidence links, remaining risks ranked, and the exact next command a successor should run — then output the completion or blocked line. Leave the ledger accurate; a truthful half-finished ledger is worth more than an optimistic finished-looking one.
