#!/usr/bin/env python3
"""Consolidate marketplace and report-derived skills into the local skills repo."""

from __future__ import annotations

import shutil
from pathlib import Path


REPO_ROOT = Path("/Users/henry/skills")
SOURCE_ROOTS = [
    ("codex", Path("/Users/henry/.codex/plugins/cache/openai-curated")),
    ("claude", Path("/Users/henry/.claude/plugins/marketplaces")),
    ("cursor", Path("/Users/henry/.cursor/plugins/marketplaces")),
    ("cursor-builtin", Path("/Users/henry/.cursor/skills-cursor")),
]
EXCLUDED_NAMES = {
    "example-skill",
    "mind",
}


REPORT_SKILLS = [
    {
        "name": "skill-harvester",
        "title": "Skill Harvester",
        "description": "Extract normalized, evidence-backed skill records from code, diffs, architecture docs, tests, tickets, screenshots, or meeting notes. Use when Codex needs to inventory demonstrated skills, deduplicate capabilities, or emit machine-parseable skill logs.",
        "summary": "Harvest demonstrated capabilities conservatively. Prefer missing a skill over hallucinating one, and attach direct evidence to every retained record.",
        "workflow": [
            "Collect the artifact set and state what kind of evidence each artifact can provide.",
            "Extract skills across frontend, systems, architecture, security, testing, devops, and i18n only when the artifact demonstrates them directly.",
            "Collapse aliases into stable canonical IDs and names before returning output.",
            "Emit a JSON-first `skill_log` with evidence pointers, confidence, gaps, and verification gates.",
        ],
        "inputs": [
            "Context or workstream summary",
            "Artifacts: files, diffs, docs, notes, screenshots, tickets, or logs",
            "Optional canonical naming or taxonomy preferences",
        ],
        "deliverables": [
            "JSON only",
            "`skill_log` with `run_id`, `timestamp`, `skills`, `gaps`, and `quality_gates`",
            "Short JSON `summary` fields instead of prose",
        ],
        "gates": [
            "Every skill has at least one evidence item.",
            "Confidence drops when an assumption is required.",
            "Semantically duplicate skills are merged before output.",
            "Anything unverifiable is labeled as a gap or assumption.",
        ],
        "system_role": "You are a conservative Skill Harvester.",
        "user_task": "Identify demonstrated skills, normalize them, deduplicate them, and return JSON only.",
    },
    {
        "name": "ui-component-spec-build",
        "title": "UI Component Spec Build",
        "description": "Produce a compact component spec plus modular implementation guidance for React or TypeScript UI work. Use when Codex needs to design or build a component, page section, or frontend feature with explicit accessibility, responsiveness, state, testing, and maintainability requirements.",
        "summary": "Drive UI work from a compact contract: define props, states, interactions, accessibility, responsive behavior, tests, and implementation seams before code generation.",
        "workflow": [
            "Start with the component API, states, error states, and loading behavior.",
            "Write an accessibility plan that prefers semantic HTML and only adds ARIA when needed.",
            "Define responsive behavior, state boundaries, and implementation seams.",
            "Return code-file outputs together with tests and a skill log sidecar.",
        ],
        "inputs": [
            "Feature name",
            "Product context",
            "Constraints or existing stack conventions",
        ],
        "deliverables": [
            "Single JSON object",
            "Keys: `spec`, `a11y`, `responsive`, `state`, `tests`, `code_files`, `skill_log`",
            "At least two concrete example tests",
        ],
        "gates": [
            "Semantic-first accessibility plan is explicit.",
            "Loading, empty, error, and success states are covered.",
            "Responsive changes are defined rather than implied.",
            "Implementation stays modular and testable.",
        ],
        "system_role": "You are a senior frontend engineer and UI architect.",
        "user_task": "Build the requested UI surface and return spec, code plan, code files, tests, and a skill log.",
    },
    {
        "name": "accessibility-gate",
        "title": "Accessibility Gate",
        "description": "Run a testable accessibility review with WCAG mapping, keyboard and focus analysis, and semantic or ARIA remediation guidance. Use when Codex needs to audit a page or component and produce a formal accessibility gate instead of generic UX feedback.",
        "summary": "Gate UI work against WCAG 2.2 AA and semantic correctness. Treat ARIA as a sharp tool, justify every usage, and map issues to explicit success criteria when possible.",
        "workflow": [
            "Model keyboard interaction, focus order, and focus visibility.",
            "Inspect semantic structure, names, roles, values, and announcement behavior.",
            "Only recommend ARIA when semantic HTML cannot express the behavior, and list misuse risks when ARIA is necessary.",
            "Return findings, WCAG mapping, remediations, tests, and a skill log.",
        ],
        "inputs": [
            "Artifact under review",
            "Primary user flows",
            "Target conformance level if not WCAG 2.2 AA",
        ],
        "deliverables": [
            "JSON with `findings`, `wcag_map`, `remediations`, `tests`, and `skill_log`",
            "Severity for each finding",
            "Explicit keyboard and screen-reader verification plan",
        ],
        "gates": [
            "Every issue is tied to a behavior, criterion, or stated assumption.",
            "No blanket ARIA recommendations.",
            "Test plan covers keyboard, focus, and assistive technology impact.",
            "Remediation steps are concrete enough to implement.",
        ],
        "system_role": "You are an accessibility gatekeeper.",
        "user_task": "Audit the artifact, map issues to WCAG where possible, and return a JSON remediation plan.",
    },
    {
        "name": "responsive-theming",
        "title": "Responsive Theming",
        "description": "Design responsive layouts, breakpoints, tokens, and preference-aware styling strategies for UI surfaces. Use when Codex needs a responsive or themed UI plan with explicit layout shifts, media-query behavior, and viewport test coverage.",
        "summary": "Prefer fluid layout first, introduce breakpoints only when the content demands it, and make preference-aware styling part of the contract rather than an afterthought.",
        "workflow": [
            "Define the layout strategy with grid or flex decisions, width constraints, and content priorities.",
            "Specify what changes at each breakpoint and why.",
            "Include user-preference handling such as reduced motion, contrast, or color scheme when relevant.",
            "Return a minimal styling strategy and a viewport test matrix.",
        ],
        "inputs": [
            "UI surface",
            "Content types",
            "Device targets or performance constraints",
        ],
        "deliverables": [
            "JSON with `layout_spec`, `breakpoints`, `styles`, `test_matrix`, and `skill_log`",
            "A mobile-first default unless the prompt overrides it",
        ],
        "gates": [
            "Breakpoints explain their behavioral changes.",
            "At least one preference-aware consideration is evaluated when relevant.",
            "Viewport tests cover both layout and interaction regressions.",
            "Styling strategy matches the requested stack.",
        ],
        "system_role": "You are a responsive UI engineer.",
        "user_task": "Produce a responsive layout plan, styling approach, test matrix, and a skill log in JSON.",
    },
    {
        "name": "state-data-orchestration",
        "title": "State Data Orchestration",
        "description": "Design state boundaries, reducers, failure modes, and error-boundary placement for complex UI features. Use when Codex needs to reason about local state, shared state, server data, URL state, optimistic updates, or resilience before implementation.",
        "summary": "Classify state deliberately, define invariants, and make failure handling first-class. Prefer the simplest state model that still scales under the feature’s complexity.",
        "workflow": [
            "Partition state into local UI, shared UI, server or cache, and URL state.",
            "Choose the simplest viable ownership model, escalating to reducers only when complexity warrants it.",
            "Document transitions, invariants, retries, partial rendering, and rollback behavior.",
            "Specify error-boundary placement and return tests together with the orchestration model.",
        ],
        "inputs": [
            "Feature name",
            "Data sources",
            "Concurrency or optimistic update concerns",
        ],
        "deliverables": [
            "JSON with `state_model`, `reducer`, `error_handling`, `tests`, and `skill_log`",
            "Text state diagram or transition table",
        ],
        "gates": [
            "All major state classes are accounted for.",
            "Failure modes have user-facing handling paths.",
            "Reducer actions and transitions are explicit when reducers are used.",
            "Error-boundary placement is justified.",
        ],
        "system_role": "You are a state management architect.",
        "user_task": "Define state boundaries, transitions, resilience patterns, and tests, then return JSON.",
    },
    {
        "name": "performance-budgeter",
        "title": "Performance Budgeter",
        "description": "Create measurable performance budgets, Core Web Vitals targets, and verification plans for web surfaces. Use when Codex needs a concrete performance plan with remediation priorities instead of vague optimization advice.",
        "summary": "Do not claim wins you cannot measure. Define budgets, explain the measurement method, and tie remediation ideas to explicit verification steps.",
        "workflow": [
            "Set budgets for LCP, INP, CLS, and any additional local constraints.",
            "Separate field measurement from lab measurement and state where results should be logged.",
            "Prioritize likely causes and remediation ideas such as code splitting, caching, rendering strategy, or asset changes.",
            "Return a prioritized action plan with verification steps.",
        ],
        "inputs": [
            "Page or flow under analysis",
            "Known bottlenecks",
            "Perf target overrides if any",
        ],
        "deliverables": [
            "JSON with `budgets`, `measurement`, `actions`, and `skill_log`",
            "Each action includes a verification method",
        ],
        "gates": [
            "Budgets are numeric and testable.",
            "Measurement distinguishes field and lab data.",
            "Actions are prioritized by expected impact.",
            "No unverified improvement claims.",
        ],
        "system_role": "You are a performance engineer.",
        "user_task": "Define budgets, measurement, actions, and verification steps in JSON.",
    },
    {
        "name": "security-hardening",
        "title": "Security Hardening",
        "description": "Generate threat-driven hardening plans with control mapping, header strategy, and CI verification steps. Use when Codex needs a practical security posture for frontend, backend, or full-stack work with explicit assumptions, controls, and validation.",
        "summary": "Separate threats, controls, and verification. Treat security as a checklist of explicit controls and gates rather than generic advice.",
        "workflow": [
            "List the most relevant threats for the declared scope and sensitivity.",
            "Map controls to known categories such as auth, session safety, injection, XSS, or dependency hygiene.",
            "Define security headers and CSP strategy when web UI is in scope.",
            "Return CI-suitable verification steps, including dependency audit expectations.",
        ],
        "inputs": [
            "System scope",
            "Data sensitivity",
            "Auth model",
        ],
        "deliverables": [
            "JSON with `threats`, `controls`, `headers`, `dependency_audit`, and `skill_log`",
            "Threat-model assumptions called out separately from verified controls",
        ],
        "gates": [
            "Threats, controls, and verification are distinct sections.",
            "Dependency-audit behavior is explicit.",
            "Header and CSP guidance is concrete when applicable.",
            "Unknown security inputs are surfaced as assumptions, not fabricated facts.",
        ],
        "system_role": "You are a security-first engineer.",
        "user_task": "Produce a threat-led hardening plan and verification steps in JSON.",
    },
    {
        "name": "test-author-gate",
        "title": "Test Author Gate",
        "description": "Design user-centered unit, integration, and e2e test plans with coverage and anti-flake gates. Use when Codex needs to write or review a test strategy that spans levels, risk areas, CI reliability, and measurable pass criteria.",
        "summary": "Bias toward tests that mirror real behavior. Separate what belongs in unit, integration, and e2e layers, and encode coverage plus flake controls as explicit gates.",
        "workflow": [
            "Write a testing strategy by level and justify what belongs in each layer.",
            "Provide representative unit, integration, and e2e coverage targets for the feature.",
            "Define coverage thresholds and CI behavior for failures.",
            "Specify anti-flake controls such as actionability, retries, and tracing policy.",
        ],
        "inputs": [
            "Feature under test",
            "Risk areas",
            "Test levels required",
        ],
        "deliverables": [
            "JSON with `strategy`, `tests`, `coverage`, `e2e`, and `skill_log`",
            "At least one end-to-end flow outline",
        ],
        "gates": [
            "Tests are organized by risk and execution level.",
            "Coverage thresholds are explicit.",
            "E2E guidance avoids sleeps and other flake-heavy patterns.",
            "User-observable behavior is prioritized over implementation details.",
        ],
        "system_role": "You are a test engineer.",
        "user_task": "Return a layered test plan, coverage gates, and e2e reliability guidance in JSON.",
    },
    {
        "name": "i18n-locale-readiness",
        "title": "I18n Locale Readiness",
        "description": "Prepare UI work for translation, locale formatting, pluralization, and multilingual edge cases. Use when Codex needs a stable i18n plan, ICU-style messages, Intl formatting guidance, or locale-readiness review before shipping UI copy.",
        "summary": "Make localization explicit early. Avoid concatenated strings, use stable keys, and treat pluralization, formatting, and text expansion as product requirements.",
        "workflow": [
            "Define message-key structure and naming conventions.",
            "Provide representative ICU-style messages for plurals or selects.",
            "Specify formatting via Intl APIs for dates, money, units, and relative time as needed.",
            "List likely failure modes such as missing keys, RTL, or expansion issues, then return a checklist.",
        ],
        "inputs": [
            "UI surface",
            "Target locales",
            "Formatting needs",
        ],
        "deliverables": [
            "JSON with `keying`, `messages`, `formatting`, `pitfalls`, and `skill_log`",
            "Message-catalog starter content",
        ],
        "gates": [
            "No string-concatenation localization patterns.",
            "Plural or select behavior is explicit when counts or variants exist.",
            "Formatting decisions are locale-aware rather than hard-coded.",
            "Missing translation risks are surfaced early.",
        ],
        "system_role": "You are an internationalization engineer.",
        "user_task": "Return a locale-readiness plan, message examples, and extraction guidance in JSON.",
    },
    {
        "name": "architecture-adr-pack",
        "title": "Architecture ADR Pack",
        "description": "Produce durable architecture artifacts such as ADRs, C4-style diagrams, API semantics notes, and implementation roadmaps. Use when Codex needs to formalize system design decisions instead of only describing architecture informally.",
        "summary": "Turn architectural intent into durable artifacts. Capture decisions, consequences, interface semantics, and a roadmap so future work inherits explicit reasoning instead of tribal knowledge.",
        "workflow": [
            "Write ADRs with context, decision, and consequences.",
            "Provide context and container-level diagrams in Mermaid.",
            "Spell out API semantics, retries, idempotency, and error-model notes.",
            "Return a roadmap and quality-attribute checklist with the architecture pack.",
        ],
        "inputs": [
            "System goal",
            "Key constraints",
            "Important integrations",
        ],
        "deliverables": [
            "JSON with `adrs`, `c4_mermaid`, `api_semantics`, `roadmap`, and `skill_log`",
            "At least two ADRs unless the prompt narrows the scope",
        ],
        "gates": [
            "ADRs include consequences rather than only decisions.",
            "Diagrams are consistent with the written interfaces.",
            "API semantics cover safety, idempotency, and retry behavior when relevant.",
            "Roadmap calls out quality attributes, not only features.",
        ],
        "system_role": "You are a software architect.",
        "user_task": "Return ADRs, diagrams, interface semantics, roadmap, and a skill log as JSON.",
    },
    {
        "name": "ci-pipeline-generator",
        "title": "CI Pipeline Generator",
        "description": "Generate minimal but complete CI pipelines with explicit quality gates, caching, and failure behavior. Use when Codex needs to author or review GitHub Actions or similar pipelines for linting, typechecking, tests, security checks, or deployment readiness.",
        "summary": "Treat CI as executable policy. Encode the required jobs, caches, matrices, and gates so the pipeline is fast, reproducible, and intentionally strict.",
        "workflow": [
            "Model the repo shape, package manager, and required quality gates.",
            "Choose job boundaries, matrices, and caching strategy deliberately.",
            "Encode install, lint, typecheck, test, and security steps with clear failure behavior.",
            "Return workflow files, gate explanations, and a skill log.",
        ],
        "inputs": [
            "Repo type",
            "Package manager",
            "Quality gates",
            "Deploy target if any",
        ],
        "deliverables": [
            "JSON with `workflow_files`, `gates`, and `skill_log`",
            "At least one workflow file path and contents",
        ],
        "gates": [
            "Each gate has a concrete command or step.",
            "Caching and matrix choices are deliberate, not boilerplate.",
            "Failure behavior is explicit for security and test gates.",
            "Workflow stays minimal while remaining complete.",
        ],
        "system_role": "You are a CI/CD engineer.",
        "user_task": "Generate the workflow YAML, explain each gate, and return a skill log in JSON.",
    },
    {
        "name": "refactor-without-fear",
        "title": "Refactor Without Fear",
        "description": "Plan and execute behavior-preserving refactors with explicit invariants, checkpoints, and verification steps. Use when Codex needs to improve maintainability or structure without silently changing externally visible behavior.",
        "summary": "Refactor with declared invariants and proof points. Start by naming what must not change, then stage the work so every step can be verified before moving forward.",
        "workflow": [
            "Declare invariants and user-visible behavior that must remain stable.",
            "Split the refactor into small checkpoints with verification after each step.",
            "Update or add tests alongside structural changes when the existing suite is not enough to preserve confidence.",
            "Return a diff summary, gate results, and a skill log.",
        ],
        "inputs": [
            "Refactor target",
            "Motivation",
            "Constraints such as timebox or no-behavior-change requirements",
        ],
        "deliverables": [
            "JSON with `invariants`, `plan`, `changes`, `gates`, and `skill_log`",
            "Explicit no-behavior-change checks unless the prompt allows behavior changes",
        ],
        "gates": [
            "Must-not-change behaviors are named before edits.",
            "Each step has a verification checkpoint.",
            "Tests or other proof points guard the refactor.",
            "Cleanup work does not silently broaden scope.",
        ],
        "system_role": "You are a refactoring engineer.",
        "user_task": "Return a behavior-safe refactor plan, staged changes, verification gates, and a skill log in JSON.",
    },
]


def existing_skill_names() -> set[str]:
    return {path.parent.name for path in REPO_ROOT.rglob("SKILL.md")}


def render_report_skill(skill: dict[str, object]) -> str:
    workflow = "\n".join(
        f"{idx}. {step}" for idx, step in enumerate(skill["workflow"], start=1)
    )
    inputs = "\n".join(f"- {item}" for item in skill["inputs"])
    deliverables = "\n".join(f"- {item}" for item in skill["deliverables"])
    gates = "\n".join(f"- {item}" for item in skill["gates"])
    scaffold_inputs = "\n".join(f"- {item}" for item in skill["inputs"])
    scaffold_outputs = "\n".join(f"- {item}" for item in skill["deliverables"])
    return (
        f'---\n'
        f'name: "{skill["name"]}"\n'
        f'description: "{skill["description"]}"\n'
        f'---\n\n'
        f'# {skill["title"]}\n\n'
        f'{skill["summary"]}\n\n'
        f'## Workflow\n'
        f'{workflow}\n\n'
        f'## Inputs\n'
        f'{inputs}\n\n'
        f'## Deliverables\n'
        f'{deliverables}\n\n'
        f'## Quality Gates\n'
        f'{gates}\n\n'
        f'## Prompt Scaffold\n'
        f'```text\n'
        f'SYSTEM\n'
        f'{skill["system_role"]}\n\n'
        f'USER\n'
        f'Inputs:\n'
        f'{scaffold_inputs}\n\n'
        f'Task:\n'
        f'{skill["user_task"]}\n\n'
        f'Output requirements:\n'
        f'{scaffold_outputs}\n'
        f'```\n'
    )


def create_report_skills() -> list[str]:
    created: list[str] = []
    for skill in REPORT_SKILLS:
        target_dir = REPO_ROOT / skill["name"]
        skill_file = target_dir / "SKILL.md"
        if skill_file.exists():
            continue
        target_dir.mkdir(parents=True, exist_ok=True)
        skill_file.write_text(render_report_skill(skill), encoding="utf-8")
        created.append(skill["name"])
    return created


def pick_external_sources() -> dict[str, tuple[str, Path]]:
    chosen: dict[str, tuple[str, Path]] = {}
    repo_names = existing_skill_names()
    for label, root in SOURCE_ROOTS:
        if not root.exists():
            continue
        for skill_md in sorted(root.rglob("SKILL.md")):
            name = skill_md.parent.name
            if name in EXCLUDED_NAMES or name in repo_names or name in chosen:
                continue
            chosen[name] = (label, skill_md.parent)
    return chosen


def import_external_skills() -> list[tuple[str, str]]:
    imported: list[tuple[str, str]] = []
    for name, (label, source_dir) in pick_external_sources().items():
        dest_dir = REPO_ROOT / name
        if dest_dir.exists():
            continue
        shutil.copytree(source_dir, dest_dir)
        imported.append((name, label))
    return imported


def main() -> None:
    created_report = create_report_skills()
    imported_external = import_external_skills()

    print(f"Created report skills: {len(created_report)}")
    for name in created_report:
        print(f"  report  {name}")

    print(f"Imported external skills: {len(imported_external)}")
    for name, label in imported_external:
        print(f"  {label:<13} {name}")


if __name__ == "__main__":
    main()
