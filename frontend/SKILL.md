---
name: "frontend"
description: "Build, refactor, debug, and review web UI in React, Next.js, Vite, Tailwind, CSS Modules, and design-system-driven applications. Use when Codex needs to implement or refine components, pages, forms, navigation, responsive layouts, client-side state, loading or error or empty states, frontend performance, accessibility, or visual polish while preserving or intentionally evolving an existing product's patterns."
---

# Frontend Engineering

Preserve the existing product before inventing a new one. Follow the current routing model, data-fetching approach, styling system, component conventions, and visual language unless the user asks for a redesign or migration.

## Inspect the stack first
1. Read `package.json`, framework config, lint or test scripts, and the nearest route or component files before editing.
2. Identify the routing, data-fetching, styling, state, form, and testing conventions already in use.
3. Copy adjacent patterns before adding new abstractions. Avoid introducing new UI libraries, state managers, or CSS conventions unless the repo already uses them or the user requests them.

## Plan the UI
1. Define the state matrix up front: loading, empty, error, success, pending, disabled, destructive, and permission-denied when relevant.
2. Keep the interactive boundary as small as possible instead of lifting entire trees into client code.
3. Prefer composition and explicit props over generic wrapper components with unclear behavior.

## Implement carefully
- Keep rendering and data-loading concerns on the server when the framework supports it.
- Add client components only for interactivity, browser APIs, local state, or subscriptions.
- Reuse existing tokens, layout primitives, typography, and motion before adding new styles.
- Keep forms resilient with labels, validation feedback, pending states, and recovery paths.
- Treat accessibility as part of implementation: semantic HTML, names, roles, values, keyboard support, and visible focus states.
- Avoid hydration mismatches by keeping server and client responsibilities clear.
- Optimize perceived performance first with streaming, skeletons, deferred work, and lazy loading where they improve the experience.

## Handle design-heavy work deliberately
- Match the established visual system when one exists.
- If the user wants something new, make explicit choices for typography, color, spacing, and motion instead of shipping a template-like default.
- Design for mobile and desktop intentionally; do not let one become an afterthought.

## Verify before handing off
- Run the smallest useful lint, type-check, and targeted test commands available in the repo.
- Check the UI in a browser or preview when available.
- Verify narrow mobile and common desktop widths, interactive states, and loading or error paths.
- Watch console and network output when behavior is unclear.
- Call out residual risk if you could not run a preview or relevant tests.

## Work with neighboring skills
- Use `accessibility` for a dedicated WCAG audit or screen-reader pass.
- Use `testing` when adding or repairing substantial frontend test coverage.
- Use `debugging` for elusive runtime behavior, race conditions, or browser-only failures.

## Load references only when needed
- Read [references/execution-checklist.md](references/execution-checklist.md) for a compact build-review-verify checklist.
- Read [references/react-next-patterns.md](references/react-next-patterns.md) when deciding server or client boundaries, async UI structure, forms, or React composition patterns.
