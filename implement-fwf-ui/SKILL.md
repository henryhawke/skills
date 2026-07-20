---
name: implement-fwf-ui
description: Implement or refactor Fart With Friends Flutter screens, widgets, themes, interaction states, audio/reaction capture, Fart Map filtering, shell navigation, and accessibility according to the canonical FWF UI system. Use for code changes under lib/presentation or lib/core/theme and for translating approved Toxic Candy mockups into production Flutter without breaking privacy, consent, offline, or route contracts.
---

# Implement FWF UI

Ship production Flutter UI from the canonical FWF design system.

## Workflow

1. Read repo `AGENTS.md`, `docs/MANIFEST.md`, and `docs/skills/fartwithfriends-ui/SKILL.md` when available.
2. Find the live implementation with Semble; read the smallest owning widget/provider/repository.
3. State the screen job, hero action, privacy/consent boundary, and required edge states.
4. Reuse `FwfTheme`, `FwfThemeTokens`, `AppTokens`, and shared shell/components. Do not add parallel palettes or magic numbers.
5. Keep state in Riverpod/service layers when it crosses widgets; keep transient gesture animation local.
6. Add or update focused widget/unit tests, format changed Dart, and run targeted analysis.

## Hard Contracts

- Global shell order: Fart Map, Inbox, center 80px Fart action, Saved, Profile.
- Center action uses `assets/images/icon.png`; preserve tap/hold semantics and semantic label.
- Fart Map contains public drops. `Everyone | My friends` filters authorship among public drops only.
- Hold-to-listen auto-records a reaction only after explicit camera/mic consent, stops with the hold, and enters preview-before-send.
- Respect reduced motion/transparency, 44–48dp touch targets, text scaling, offline/loading/error states, and cancellation.

## References

- `references/architecture.md` — project file ownership and implementation patterns.
- `references/interaction-contracts.md` — FWF-specific interaction, consent, and privacy rules.
