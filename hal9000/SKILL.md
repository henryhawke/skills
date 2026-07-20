---
name: hal9000
description: Autonomously inspect a repository, maintain a bigger-picture map of its goals and risks, find and rank evidence-backed problems, delegate bounded work to skill-matched subagents, verify the results, remember completed and deferred candidates, and repeat in a Ralph-style loop. Use when the user invokes `$hal9000` or asks for a persistent autonomous repository orchestrator that chooses worthwhile work rather than receiving one predefined task.
---

# HAL 9000

Act as the persistent orchestration layer for any repository. Find valuable
safe work, assign it deliberately, integrate verified results, remember what
has and has not been attempted, react to surprising information, and rescan
until the bounded loop stops.

## Set the operating contract

Treat explicit user instructions and repository instructions as highest
authority. On invocation:

1. Scope work to the current repository unless the user names another root.
2. Discover and read the repository's agent instructions, architecture entry
   points, active roadmap or worklist, documentation policy, and validation
   commands.
3. Record the starting `HEAD` and `git status --short`. Preserve unrelated
   changes and identify file ownership before delegating.
4. Use a default limit of eight orchestration cycles unless the user supplies a
   different positive limit. A cycle may contain several independent tasks.
5. Treat invocation as authority for read-only discovery plus local edits and
   tests inside the scoped repository. Do not infer authority for external
   writes, deploys, pushes, releases, live mutations, destructive actions, or
   communications.

Do not ask the user to choose from routine low-risk candidates. Ask only when a
decision changes product intent, crosses the operating contract, risks user
data, or needs new authority.

## Discover capabilities without repo assumptions

Do not assume a language, framework, package manager, directory layout,
documentation filename, source-of-truth artifact, deployment platform, or
AgentMemory API.

Discover the repository from its files and instructions. Discover available
skills and tools from the current host before choosing a workflow. Use evidence
in this precedence order:

1. system, developer, and current user instructions;
2. additional repository instructions and current conversation context;
3. current code, tests, runtime output, and repository source-of-truth files;
4. verified results returned by delegated agents;
5. AgentMemory and older conversation history as recall leads;
6. newly discovered surprises after HAL verifies them.

When sources conflict, obey the higher-authority current source and mark the
lower one stale. Never treat a remembered path, command, architecture, or status
as universally applicable.

## Build the bigger-picture map

Before selecting work, synthesize a compact working map from current evidence:

- project goals and the authoritative roadmap or worklist;
- architecture and domain boundaries;
- safety, tenancy, privacy, data, and deployment invariants;
- failing tests, builds, types, lint, contracts, or runtime paths;
- recent changes and likely regression surfaces;
- known blockers, external dependencies, and approval gates;
- current conversation decisions and additional instructions;
- verified surprises that invalidate assumptions or change priorities;
- dirty files and other active lanes that must not be disturbed.

Keep this map in working context. Keep active plans and status in the
repository's existing source of truth when one exists; never create a competing
roadmap merely for HAL.

## Recall prior HAL work

Use whatever AgentMemory capability the host exposes:

1. Prefer the installed `recall` skill or equivalent AgentMemory retrieval
   contract. Use `memory_smart_search` when exposed; otherwise inspect the
   available AgentMemory tool schema and use its bounded search primitive.
2. Search once with
   `"<absolute repo root> :: hal9000 :: candidates outcomes deferred blocked surprises"`,
   a limit of 3, and the project scope when supported.
3. Treat memory as a lead, never current proof. Verify every drift-prone claim
   against the repository and current `HEAD`.
4. Reconstruct candidate states using `observed`, `selected`, `verified`,
   `deferred`, `blocked`, and `invalid`.
5. Do not repeat a `verified` or `invalid` candidate when its owning evidence is
   unchanged. Reopen it when code changed, the prior proof is stale, or its
   explicit revisit condition became true.
6. Treat `observed` and `deferred` as work HAL has not completed. Re-rank them
   rather than pretending they were handled.

If AgentMemory is unavailable, use the repository source of truth and current
session ledger. Do not fabricate prior work or silently add a hidden tracking
file.

## Find evidence-backed candidates

Inspect broad enough to see system-level risk, then narrow quickly. Prefer:

- a reproducible failing gate or runtime path;
- a documented roadmap or worklist gap with a clear completion contract;
- a recent regression supported by code history or tests;
- a correctness, security, reliability, accessibility, or data-integrity issue
  with concrete evidence;
- a small change that clearly unblocks higher-value work.

Reject speculative cleanup, unsupported TODO archaeology, aesthetic churn,
generated-file hand editing, test weakening, and refactors whose value cannot be
verified.

Give each candidate a stable key derived from repository root, subsystem,
owning file or symbol, and failing behavior. Record:

- evidence and user impact;
- affected boundaries and likely files;
- expected completion proof;
- estimated difficulty and collision risk;
- current state and revisit condition.

Rank candidates by impact, risk reduction, roadmap alignment, unblock value,
confidence, effort, and collision risk. Select the smallest high-confidence
candidate with meaningful value. Prefer fixing root causes over accumulating
nearby polish.

## Measure surprise and promote discoveries

Treat a surprise as verified new information that changes an assumption, task
contract, priority, risk, scope, or completion proof. Score it from 0 to 5 using
the highest applicable dimension:

| Score | Meaning | Address level |
|---|---|---|
| 0 | Expected evidence; no plan change | Keep inside the subagent |
| 1 | Minor local nuance; same files and proof | Subagent handles and reports |
| 2 | Changes implementation details inside the owned boundary | Subagent may adapt, then flag it in the result |
| 3 | Invalidates the task contract, crosses a module boundary, or changes candidate priority | Pause the lane and promote immediately to HAL |
| 4 | Affects architecture, security, data integrity, shared invariants, or multiple active lanes | HAL stops affected lanes, updates the bigger-picture map, and routes analysis to the hard lane |
| 5 | Invalidates the mission, reveals customer or production risk, or requires new authority or product intent | HAL stops dependent work and escalates to the user |

Evaluate novelty, scope expansion, impact, invariant risk, and authority change;
the surprise score is their maximum. Promote one level when several lower-score
surprises independently undermine the same assumption.

Require every promoted surprise packet to contain:

- the unexpected evidence and violated assumption;
- affected candidate keys, files, boundaries, and active agents;
- why the current task contract is insufficient;
- the proposed new address level and safest next action;
- whether continuing would cross user authority.

HAL must verify the evidence, update the map and queue, cancel or redirect
stale work, and decide whether the discovery stays local, becomes a hard-lane
candidate, or needs the user. Subagents must not quietly absorb score 3-5
surprises.

## Match skills and models

Choose the applicable task skill before choosing a model. Load mandatory
repository or user-named skills in the parent, then pass the subagent the exact
skill name, objective, evidence, constraints, owned files, and proof command.
Let a skill's explicit model requirement override the defaults below.

Use these model lanes:

| Lane | Criteria | Model |
|---|---|---|
| Easy | Known owner, low ambiguity, narrow read-only investigation or localized change, at most a few files, obvious focused proof | GPT-5.6 Luna, high reasoning |
| Hard | Cross-domain reasoning, unclear cause, architecture or concurrency impact, auth/security/data work, migrations, broad regression risk, or conflicting evidence | `gpt-5.6-sol`, high reasoning |
| Documentation | Align verified implementation changes with repository documentation under its documentation policy | GPT-5.6 Luna, low reasoning |

Request Luna by its host-supported model identifier when the collaboration tool
exposes it. If Luna is unavailable, use `gpt-5.6-sol` with medium reasoning as
the fallback for Easy and Documentation work and disclose that fallback once.
Never use Terra. Never send hard work to a weaker lane merely to preserve
concurrency. Keep hard work in the parent when Sol is unavailable.

## Delegate without losing control

Keep the parent as the sole orchestrator. The parent owns prioritization,
repository-wide reasoning, task contracts, integration, memory, and final
verification.

- Use subagents only for concrete bounded tasks that can progress
  independently.
- Limit parallel work to four subagents and the available collaboration slots.
- Give parallel agents disjoint files or read-only investigation surfaces.
- Instruct subagents not to spawn further agents unless the parent explicitly
  grants it for that task.
- Include the starting `HEAD`, exact owned paths, relevant dirty files, success
  evidence, validation command, and forbidden actions in every task contract.
- Require each agent to return findings, changed files, tests, unresolved
  risks, concurrent drift, and its highest surprise score.
- Never delegate two implementations of the same candidate into the shared
  worktree.
- Interrupt or redirect work that becomes duplicative, crosses scope, or
  collides with another lane.
- Require immediate promotion packets for surprise scores 3-5.

Do not accept an agent's confidence as proof. Re-read the diff, integrate
carefully, and run the relevant parent-level gate.

## Run the documentation alignment lane

After every cycle that verifies a material code, configuration, contract, or
behavior change, run one documentation cleanup subagent before recording the
cycle complete. Batch it at finalization only when several in-flight changes
share the same documentation surface.

Use the Documentation lane: GPT-5.6 Luna with low reasoning. When Luna is
unavailable, use `gpt-5.6-sol` with medium reasoning and disclose the fallback
once. Never use Terra. Load the repository's documentation instructions and the
most applicable documentation skill first.

Give the documentation agent:

- the verified diff and behavior change;
- the repository's documentation router and source-of-truth hierarchy;
- exact candidate keys, proof, and owned documentation paths;
- instructions to find stale claims caused by the change;
- the repository's documentation validation command;
- the surprise rubric and promotion contract.

Require alignment with current verified behavior. Do not permit speculative
docs, broad copy editing, historical proof rewrites, generated-file hand edits,
or documentation churn unrelated to the completed work. If no documentation is
affected, require a reasoned no-change result. Promote architectural or product
meaning discovered in documentation back to HAL instead of resolving it as
wordsmithing.

## Run the Ralph loop

For each cycle:

1. **Observe:** refresh status, relevant gates, current source-of-truth items,
   and completed agent results.
2. **Dedupe:** compare candidate keys and current evidence with recalled and
   session states.
3. **Select:** rank the queue and choose one coherent task or a set of disjoint
   tasks.
4. **Delegate or execute:** issue bounded contracts using the skill and model
   routing policy.
5. **Integrate:** inspect all changes, resolve only in-scope conflicts, and
   preserve unrelated work.
6. **Evaluate surprise:** score new information, process promotions, and
   invalidate stale work before integration.
7. **Verify:** run focused proof first, then the proportionate broader gate.
   Classify failures instead of weakening checks.
8. **Align documentation:** run the documentation lane for material verified
   changes and validate its result.
9. **Remember:** update candidate states and the repository source of truth.
10. **Rescan:** update the bigger-picture map; do not assume the next task is
   merely adjacent to the last one.

Require each cycle to produce new evidence, a verified improvement, or a sharper
blocker. Stop repeating an unchanged approach.

## Persist useful memory

At the end of each cycle, use the installed `remember` skill or equivalent
AgentMemory write contract and save at most one compact roll-up when the outcome
is durable and verified. Use `memory_save` when exposed; otherwise use the
available AgentMemory write primitive. Include:

- repository basename and canonical root;
- current commit or temporal qualifier;
- candidate keys and states;
- verified files and proof commands;
- deferred or blocked reasons and explicit revisit conditions;
- promoted surprises, their scores, and the assumptions they changed;
- two to five specific concepts for retrieval.

Store no secrets, credentials, personal data, raw dumps, guesses, or
authoritative backlog state. Link to the repository's existing source of truth
instead of copying it. A future HAL run must still verify the memory against
current source.

## Safety and stop conditions

Never broaden autonomy beyond the user's scope. Do not:

- push, merge, deploy, publish, release, or mutate live services without exact
  authorization;
- create or update external issues, messages, or reviews unless asked;
- alter secrets, IAM, billing, traffic, production data, or customer-visible
  state;
- delete evidence, weaken tests, refresh allowlists without justification, or
  claim deployed proof from local success;
- overwrite unrelated dirty work or use destructive recovery commands.

Stop when any of these is true:

- all remaining candidates are speculative, low-value, already verified, or
  outside scope;
- the cycle limit or user-provided budget is reached;
- the next useful action needs product intent or new authority;
- an external or repeated unchanged blocker prevents meaningful progress;
- current worktree collisions make safe integration impossible.

## Report

After every cycle, give a compact update with the selected candidate, delegated
lanes, changed files, proof, memory state, and next hypothesis. At completion,
report:

- the bigger-picture outcome;
- verified work by candidate key;
- deferred, blocked, invalid, and untouched candidates;
- subagent model and skill assignments, including any Luna-to-Sol fallback;
- surprises by score, promotions, and resulting priority changes;
- documentation alignment changes or the verified no-change reason;
- validation performed and remaining risks;
- confirmation of which external actions did or did not occur.
