# React and Next.js Patterns

Load this file when working in React or Next.js codebases and the task involves boundaries, async UI, forms, or state structure.

## Component boundaries
- Default to server-rendered components when the framework supports them.
- Push `use client` to the smallest leaf that needs interactivity, browser APIs, or subscriptions.
- Do not turn a page or layout tree into a client component just to host one interactive control.

## Data and async UI
- Co-locate server data at the route or layout boundary when possible, then pass serializable props down.
- Place `Suspense` boundaries around slow subtrees instead of wrapping the entire page by habit.
- Avoid duplicating server-fetched data with client refetches unless the product genuinely needs live sync or optimistic updates.

## Forms and mutations
- Follow the mutation path already used in the repo: server actions, route handlers, query libraries, or form libraries.
- Surface pending, success, and failure states explicitly.
- Reset or retain form state intentionally after submit; do not leave it ambiguous.
- Keep optimistic updates reversible and easy to reconcile.

## State and hooks
- Prefer local state before shared state.
- Promote state only when multiple distant consumers need the same source of truth.
- Avoid storing derived values that can be computed during render.
- Follow repo guidance on the React Compiler. Do not add `useMemo` or `useCallback` by default unless the codebase already treats them as standard or profiling shows a need.
- Use `startTransition`, `useDeferredValue`, or `useEffectEvent` when they fit the existing patterns and materially improve interaction behavior.

## Composition and styling
- Reuse existing primitives and variants before creating new component families.
- Prefer clear prop APIs to mega components with dozens of mode flags.
- Keep styling decisions aligned with the design system already present in the repo.

## Common regressions
- Hydration mismatches from non-serializable props, time-dependent rendering, or random values in render.
- Fetch waterfalls caused by nested client-side fetching.
- Effect-driven computations that should be derived directly from props or state.
- Missing keys, missing labels, missing focus styles, or invisible loading states.
