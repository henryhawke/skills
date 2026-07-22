---
name: sisyphus
description: Continuously diagnoses and fixes CI, build, and deployment failures one candidate at a time, then commits, pushes to the deployment branch, and monitors each authorized attempt until the requested remote deployment is green or genuinely blocked. Use when the user invokes Sisyphus or asks to keep fixing GitHub Actions, Cloud Build, Cloud Run, or a similar deployment without retry churn; a local branch or local pass is never the terminal result.
---

# Sisyphus

Continuously drive authorized release candidates from the newest concrete
failure to terminal deployed proof. Do not retry an unchanged candidate and do
not stop at a local commit, holding branch, pull request, image, or zero-traffic
revision.

## Establish the contract

Before changing state, record:

- the target repository, branch, environment, and deployment workflow;
- what the user authorized: local edits, commits, pushes, deploys, secrets,
  provider changes, or traffic changes;
- the terminal condition, such as CI green, build green, revision promoted,
  health green, or provider proof complete;
- any retry limit. When the user says one attempt, permit exactly one external
  build submission for each distinct pushed candidate.

A request to keep fixing failures authorizes persistence, not unrelated
mutations. Stop for credentials, provider changes, IAM grants, production data
writes, or broader deployment authority that the user did not grant.

## Interpret continuous authorization

When the user says "continuously," "keep fixing until green," "get a working
Cloud Run build," or equivalent:

- treat local edits, commits, sequential fast-forward pushes to the identified
  deployment branch, and deployments triggered by its checked-in workflow as
  authorized;
- if the repository and workflow make the deployment branch and environment
  unambiguous, proceed without pausing to ask again;
- keep manual traffic commands, provider mutations, secrets, IAM, production
  data, and unconfigured environments approval-gated;
- remain in the loop after each terminal failure: capture it, fix it locally,
  publish one distinct candidate, and monitor again.

A temporary isolated checkout or `codex/` branch is an implementation detail.
It is not a handoff or stop condition. Reconcile and publish its validated
commit to the authorized deployment branch unless a remote movement, protected
branch rule, missing credential, or user instruction blocks that action.

## Protect the checkout

1. Read repository instructions and inspect `git status --short`.
2. Pin `HEAD`, the remote target, and the files owned by this task.
3. Preserve unrelated dirty changes. In a shared or heavily dirty checkout, use
   an isolated worktree based on the intended remote commit.
4. Re-read status before broad gates, staging, rebasing, or pushing.
5. Stage explicit paths only. Never use a broad stage command in a shared
   checkout.

Do not switch or clean a shared dirty checkout merely to publish. Commit in the
isolated checkout, fetch the real remote, prove a fast-forward, and push that
exact commit from the isolated checkout.

Keep local proof, remote CI proof, build proof, deployed proof, provider proof,
and external sign-off separate.

## Start from the newest failure

Inspect the newest run for the exact candidate. Capture:

- workflow run and job IDs;
- build ID and candidate commit;
- failing step, exit code, and the smallest useful log excerpt;
- current deployed revision and traffic baseline.

Classify the failure before editing:

- source regression;
- generated artifact or contract drift;
- configuration, secret, IAM, or provider state;
- infrastructure or transient failure;
- concurrent branch movement or unrelated change.

Do not speculate from an older failure after a newer candidate exists. Do not
submit another build merely to discover an error that can be reproduced
locally.

## Rehearse locally

1. Reproduce the failing command or closest production-equivalent artifact.
2. Fix the smallest coherent cause. Do not weaken tests, contracts, refusal
   gates, tenancy, idempotency, or security checks.
3. Run the narrowest affected test immediately.
4. Broaden to the repository-required type, lint, contract, build, generated
   artifact, and domain gates.
5. If another failure appears locally, fix it before pushing.
6. Record exact commands, results, and changed files.

Treat unavailable integrations separately from source failures. A local pass is
not deploy proof.

## Publish one candidate

Immediately before committing or pushing:

1. Fetch the remote target and compare it with the pinned base.
2. If the remote moved, preserve concurrent work and replay only this task's
   commits. Never force-push unless the user explicitly requested it.
3. Review the staged diff and path list.
4. Commit with a message that explains the failure fixed and the release impact.
5. Push once to the actual deployment branch. A local-only or non-deploying
   branch does not satisfy this step unless the user explicitly requested PR
   validation instead of a deployment.
6. Confirm that exactly one deployment workflow and one external build
   submission correspond to the candidate.

If a workflow fails before submitting a build, record that distinction. Do not
count a validation-only failure as a Cloud Build attempt.

## Monitor to a terminal result

Follow the candidate continuously through:

1. CI validation;
2. build submission;
3. image build and immutable digest;
4. zero-traffic candidate creation when supported;
5. candidate health and dependency readiness;
6. indexes, queues, schedulers, secrets, and release-resource readback;
7. traffic promotion;
8. post-promotion observation;
9. terminal workflow status.

Send concise progress updates during long waits. Prefer direct build logs over
repeated UI polling when they expose the active step sooner.

On failure:

1. Capture the new exact error and confirm whether traffic stayed on the prior
   healthy revision or rollback succeeded.
2. Do not rerun the same candidate.
3. Return to local rehearsal with the new failure.
4. Publish a new commit only after the fix and required gates pass.
5. Continue the same loop immediately. A progress report is not a handoff.

On success, independently read back the deployed revision, commit label, image
digest, traffic percentage, health/readiness status, and required resource
state. Do not rely only on a green workflow badge.

## Secrets and credentials

- Never print, commit, or include secret values in logs or handoffs.
- Use masked CI secret channels and the platform's secret manager.
- Verify secret presence, version, access, and binding without echoing content.
- Do not invent credentials or grant broad IAM to make a pipeline pass.
- Provision, rotate, or bind a secret only when the user authorized that exact
  environment mutation.

## Stop conditions

Stop when:

- the full terminal contract is proven;
- the next action needs new authority or user-controlled credentials;
- the failure is an external provider or infrastructure blocker that cannot be
  resolved safely;
- the same approach has failed unchanged and no new evidence supports another
  attempt.

Do not stop or claim success merely because source tests pass, a local branch is
clean, a pull request exists, an image builds, or a revision exists at zero
traffic. When continuous execution was requested, yield a final handoff only
after deployed proof succeeds or a genuine stop condition is evidenced.

## Handoff

Report:

- final outcome and exact candidate commit;
- workflow run ID and conclusion;
- build ID and number of submissions;
- deployed revision, image digest, traffic, health, and readiness;
- resource readback such as indexes, queues, and schedulers;
- commit-to-path ledger;
- local and remote gates run;
- current `HEAD` versus remote target;
- preserved unrelated work;
- any remaining provider action or sign-off.

Keep secret values out of the report.

## Example triggers

- "Fix each new GitHub Actions error, push the fix, and follow one Cloud Build
  submission until Cloud Run is healthy."
- "Keep repairing the deployment until green, but never retry an unchanged
  candidate."
- "Continuously push distinct fixes to main and monitor Cloud Run until the new
  revision is healthy."
