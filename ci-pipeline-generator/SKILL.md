---
name: "ci-pipeline-generator"
description: "Generate minimal but complete CI pipelines with explicit quality gates, caching, and failure behavior. Use when Codex needs to author or review GitHub Actions or similar pipelines for linting, typechecking, tests, security checks, or deployment readiness."
---

# CI Pipeline Generator

Treat CI as executable policy. Encode the required jobs, caches, matrices, and gates so the pipeline is fast, reproducible, and intentionally strict.

## Workflow
1. Model the repo shape, package manager, and required quality gates.
2. Choose job boundaries, matrices, and caching strategy deliberately.
3. Encode install, lint, typecheck, test, and security steps with clear failure behavior.
4. Return workflow files, gate explanations, and a skill log.

## Inputs
- Repo type
- Package manager
- Quality gates
- Deploy target if any

## Deliverables
- JSON with `workflow_files`, `gates`, and `skill_log`
- At least one workflow file path and contents

## Quality Gates
- Each gate has a concrete command or step.
- Caching and matrix choices are deliberate, not boilerplate.
- Failure behavior is explicit for security and test gates.
- Workflow stays minimal while remaining complete.

## Prompt Scaffold
```text
SYSTEM
You are a CI/CD engineer.

USER
Inputs:
- Repo type
- Package manager
- Quality gates
- Deploy target if any

Task:
Generate the workflow YAML, explain each gate, and return a skill log in JSON.

Output requirements:
- JSON with `workflow_files`, `gates`, and `skill_log`
- At least one workflow file path and contents
```
