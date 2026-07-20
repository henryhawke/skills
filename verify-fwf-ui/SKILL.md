---
name: verify-fwf-ui
description: Validate Fart With Friends Flutter UI changes against canonical visual, interaction, accessibility, privacy, consent, map, audio, reaction, and shell-navigation contracts. Use for UI review, pre-merge verification, regression testing, mockup-to-code comparison, or auditing a screen's loading, empty, error, offline, reduced-motion, and microinteraction states.
---

# Verify FWF UI

Produce evidence, not aesthetic vibes.

## Workflow

1. Read repo `docs/skills/fartwithfriends-ui/SKILL.md` and the owning source/tests.
2. Identify the screen job, hero, novel verb, privacy/consent boundary, and state matrix.
3. Run the smallest relevant Flutter analyze/test set, then broaden only if shared contracts changed.
4. Review visual tokens, semantics, text scaling, hit targets, reduced motion/transparency, and cancellation paths.
5. Report failures by contract and file/line; distinguish source proof from device-only evidence.

## Mandatory Checks

- Shell labels/order and 80px logo-based center action.
- All public vs Friends' public map filtering; no private data path.
- Hold playback and reaction recording start/stop together after consent.
- Preview-before-send and re-record/discard paths.
- Default, pressed, focus, disabled, loading, and error for changed controls.
- Empty, partial, long, offline, and permission-denied screen states.
- 44–48dp targets, semantic labels, logical focus order, and large-text survival.
- One authored route silhouette, no universal card borders, no random accent-per-item, and no continuous decorative atmosphere.

## References

- `references/profiles.md` — targeted validation profiles and evidence boundaries.
