---
name: "task-management"
description: "Use for coordinating development tasks, breaking down features into implementation steps, managing dependencies between tasks, tracking progress, and integrating with Task Master AI and Linear for project management."
---

# Task Management & Orchestration

You break ambiguous work into concrete, shippable units. Each task has a clear definition of done, and you track dependencies so nothing blocks silently.

## When to use
- Break down a feature request into implementation tasks
- Coordinate multi-step implementations
- Track progress across a development cycle
- Identify parallelizable work
- Integrate with Task Master AI or Linear for tracking

## Task Breakdown Protocol

### 1. Understand the Goal
- What does the user actually need to accomplish?
- What's the definition of done?
- Are there constraints (deadline, existing code, compatibility)?

### 2. Decompose into Shippable Units
Each task should be:
- **Independently testable** — can be verified without other tasks
- **Small enough** to complete in one session
- **Clear on dependencies** — explicitly lists what must be done first

### 3. Order by Dependencies
```
Task A: Create database table + RLS        (no deps)
Task B: Create Edge Function endpoint       (depends on A)
Task C: Create Dart repository + model      (depends on A)
Task D: Create Riverpod provider            (depends on C)
Task E: Create UI widget                    (depends on D)
Task F: Wire into navigation                (depends on E)
```

### 4. Identify Parallelism
Tasks B and C above can run in parallel (both depend on A, not on each other).

## Task Master AI Integration

### Daily Workflow
```bash
task-master next                              # What should I work on?
task-master show <id>                         # Full details
task-master set-status --id=<id> --status=in-progress
# ... do the work ...
task-master update-subtask --id=<id> --prompt="implementation notes"
task-master set-status --id=<id> --status=done
task-master next                              # What's next?
```

### Creating Tasks from a Feature Request
```bash
# Write the feature as a mini-PRD, then parse it
task-master parse-prd path/to/feature.md --append

# Analyze complexity to determine subtask depth
task-master analyze-complexity --research --from=<first-new-id> --to=<last-new-id>

# Expand into subtasks
task-master expand --id=<id> --research
```

### Tracking Implementation Progress
```bash
# Log what worked and what didn't (persists across sessions)
task-master update-subtask --id=<id> --prompt="Tried approach X, hit issue Y. Switching to Z."
```

## Linear Integration

### Syncing with Linear
- Issues are tracked in Linear workspace (project HNRY)
- Use `list_issues`, `get_issue`, `save_issue` via Linear MCP
- Commit messages reference issues: `fix: resolve HNRY-42`
- PR descriptions auto-link to Linear issues

### Status Mapping
| Task Master | Linear | Meaning |
|---|---|---|
| `pending` | Backlog | Not started |
| `in-progress` | In Progress | Currently working |
| `done` | Done | Verified complete |
| `blocked` | Blocked | Waiting on external factor |

## Estimation Rules
- Don't give time estimates — they're always wrong and create false expectations
- Instead, communicate: scope (small/medium/large), dependencies, and risks
- If asked for estimates, redirect to: "Here's what needs to happen, and here's what could go wrong"

## Quality Gates (Before Marking Done)
1. Code compiles without warnings (`flutter analyze` shows 0 issues)
2. Existing tests still pass
3. New behavior has been manually verified
4. No debug/temporary code left in
5. Changes follow established architecture patterns
