# Frontend Execution Checklist

Use this as a compact final pass after the core workflow in `SKILL.md`.

## Before editing
- Map the user flow and the exact route, component, or surface being changed.
- Identify the source of truth for data, form state, and visual tokens.
- Note every state the UI must support: loading, empty, error, success, pending, disabled, and overflow or long-content cases.

## During implementation
- Preserve the existing routing, styling, and state conventions unless the task explicitly changes them.
- Keep client-only code at the leaves when the framework supports server rendering.
- Prefer local state first; only promote state when multiple distant consumers share the same source of truth.
- Make edge states visible instead of hiding them behind implicit branching.
- Keep interactive controls keyboard-accessible and focus-visible.

## Before finishing
- Run the smallest useful lint, type-check, and targeted test commands available.
- Verify the UI at a narrow mobile width and a common desktop width.
- Exercise hover, focus, pressed, disabled, loading, empty, and error states where they exist.
- Check console and network output for failed requests, hydration issues, or warnings.
- Scan for overflow, truncation, sticky-position bugs, and layout shifts.

## Red flags
- A new dependency solves a small local UI problem.
- A large tree becomes client-rendered to host one interactive child.
- Data fetching or derived state gets duplicated without a clear need.
- A custom control lacks keyboard support, labels, or visible focus.
- A visual change ships without browser verification.
