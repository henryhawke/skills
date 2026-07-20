---
name: design-fwf-toxic-candy-ui
description: Design, critique, mock up, or implement Fart With Friends mobile UI in the polished Toxic Candy Arcade visual system. Use for FWF screen redesigns, Flutter UI work, image mockups, design-system decisions, interaction states, component styling, motion direction, or visual QA that should preserve the app's real navigation, privacy, audio, map, inbox, Saved, onboarding, and profile contracts.
---

# Design FWF Toxic Candy UI

Create joyful toy-tech UI without sacrificing product truth or legibility. Treat the app like a premium arcade collectible: matte dark stages, hard acrylic structure, and inflated gel only for high-value actions.

## Workflow

1. Identify the real screen and state in the Flutter source before designing. Use Semble when available.
2. Read `references/creative-direction.md` for authored composition, atmosphere, and signature moments.
3. Read `references/style-system.md` for visual rules.
4. Read `references/design-bible-laws.md` for the inherited craft, state, motion, and novelty laws.
5. Read the relevant section of `references/screen-contracts.md`; never replace an active contract with concept-only fiction.
6. For raster mockups, use `assets/reference-board.png` as a historical style reference and the screen recipe in `references/mockup-prompts.md`. Generate one board per screen family, not one overcrowded app montage.
7. For Flutter implementation, reuse the existing theme, 8dp grid, 44–48dp touch targets, 80px center fart action, and reduced-motion/transparency accommodations.
8. Validate against the checklist below before presenting or shipping.

## Non-Negotiable Art Direction

- Keep roughly 70% matte plum-black, 20% structured surfaces/type, and 10% luminous candy accents.
- Reserve inflated lime gel for the global fart action and the active hold-to-listen state.
- Use at most three material treatments on a screen: matte stage, acrylic structure, gel hero.
- Use Archivo Expanded for strong headings and Public Sans for readable UI. Bubble lettering is display seasoning, never body text.
- Prefer one focal joke per screen. Let dead-serious interaction design carry the comedy.
- Keep the shell navigation exact: Fart Map, Inbox, center Fart button, Saved, Profile.
- Keep Fart Map public-only. Private sends belong in the composer target flow.
- Permit an `Everyone | My friends` filter on Fart Map only when both views remain public drops; never mix private sends into map data.
- Use `assets/images/icon.png` as the product mark inside the global fart action.
- Auto-record reactions only during hold-to-listen, only after explicit camera/mic consent, and always require preview before send.
- Show tap, hold, recording, consent, privacy, offline, loading, and error states explicitly when relevant.

## Mockup Quality Bar

- Render a straight-on modern phone at useful scale with the entire screen visible.
- Present one primary screen plus one or two state/details, not a decorative collage that hides UI.
- Use real labels from `references/screen-contracts.md` and no invented engagement systems.
- Make hierarchy readable at thumbnail size; avoid dense microcopy and fake glyph soup.
- Show tactile depth through restrained highlights and edge lighting, not global glow.
- Keep key controls at least visually 44px and give the hero action breathing room.

## Validation Checklist

- Does the screen preserve its source interaction and privacy contract?
- Is there one obvious primary action?
- Does lime mean active gas action rather than generic decoration?
- Can text be read without relying on glow or color alone?
- Are depth, type, and icon styles consistent?
- Are disabled, loading, offline, consent, and destructive states unambiguous?
- Would the screen remain coherent with transparency and motion reduced?
- Is it funny because of the product language and behavior, not random stickers?

## Resources

- `references/style-system.md` — palette, materials, type, geometry, motion, accessibility, and anti-patterns.
- `references/creative-direction.md` — Awwwards-informed art direction, atmosphere, composition, and signature FWF moments.
- `references/design-bible-laws.md` — inherited laws from the user-provided design bible, specialized for FWF.
- `references/screen-contracts.md` — verified live screen and state requirements.
- `references/mockup-prompts.md` — reusable master prompt and screen-by-screen render recipes.
- `assets/reference-board.png` — original Toxic Candy Arcade concept used only as a style reference.
- `assets/screens/` — approved high-detail screen boards generated from this skill.
