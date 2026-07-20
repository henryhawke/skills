# Toxic Candy Arcade Style System

## Design Thesis

Make Fart With Friends feel like a forbidden late-1990s candy toy rebuilt with contemporary product discipline. The first read is premium tactile fun; the second read is the ridiculous seriousness of sending and cataloging farts.

The system is not “neon everywhere.” It uses controlled contrast:

- Matte stage for focus.
- Acrylic structure for navigation and information.
- Inflated gel for touch, audio, and celebration.
- Sticker graphics only as punctuation.

## Palette

Use these as design targets; map them to the nearest project tokens during implementation.

| Role | Color | Usage |
| --- | --- | --- |
| Night stage | `#12091D` | Main canvas; about 70% of a screen |
| Raised plum | `#241231` | Cards, sheets, dock |
| Acrylic edge | `#553868` | Borders and separators |
| Candy white | `#FFF8FF` | Primary text |
| Muted lilac | `#CBB9D5` | Secondary text |
| Methane lime | `#A8F04F` | Global fart action, active listening, success |
| Bubblegum pink | `#FF70AE` | Social/reaction action, unread emphasis |
| Electric cyan | `#BDF3F8` | Information, distance, map utility |
| Gas yellow | `#FFE45B` | Warning, recording timer, attention |
| Arcade violet | `#7C3DFF` | Decorative depth, premium accent |
| Destructive coral | `#FF6B73` | Delete, discard, report |

Rules:

- Use one dominant accent and at most two supporting accents per screen.
- Never place body copy in a saturated accent color.
- Do not use lime for ordinary navigation, passive badges, or decoration.
- Pair every state color with text, icon, shape, or motion.

## Materials and Depth

### Matte stage

- Near-black plum, subtle radial lift behind the hero, no visible texture at normal scale.
- Avoid star fields, fog, bubbles, or glitter behind dense content.

### Hard acrylic

- Use for cards, dock, segmented controls, utility buttons, and sheets.
- Keep blur restrained; preserve a solid-enough fill for contrast.
- Use a 1px plum/lilac edge, a narrow top highlight, and one soft shadow.

### Inflated gel

- Use only for the fart button, active hold target, recording pressure, or a single celebratory token.
- Use a crisp silhouette, thick inner highlight, subtle subsurface color, and controlled shadow.
- Never render entire lists or navigation as inflated gel.

### Sticker punctuation

- Allow one or two per screen: unread burst, reaction stamp, rare Saved badge, onboarding flourish.
- Keep stickers away from primary copy and controls.

## Typography

- Use Archivo Expanded 800–900 for screen titles and compressed arcade authority.
- Use Public Sans 500–700 for navigation, labels, metadata, and copy.
- Permit a custom bubble wordmark only for the app name, mode title, or large celebratory phrase.
- Use sentence case for controls; reserve all caps for short display labels and status stamps.
- Keep body text at 15–17sp, metadata at 12–13sp, controls at 15–17sp, titles at 28–36sp.
- Keep glow off text. If luminous type is needed, use a crisp fill plus a restrained 2–4px halo.

## Geometry and Spacing

- Base all layout on the existing 8dp grid with 4dp optical adjustments.
- Use 24px screen gutters, 16px card padding, 12–16px card gaps.
- Use 16–20px card radii, 24–28px sheet radii, full pill geometry only for chips or segmented controls.
- Preserve 44–48px minimum touch targets.
- Preserve the 80px center-docked fart action and give it at least 12px clear space.
- Use asymmetry only in decorative framing, never in control alignment or data lists.

## Icons and Avatars

- Use the existing Lucide-like outline family for utility navigation.
- Give active icons a small filled candy core; do not mix five icon styles.
- Treat avatars as framed user identity, not invented game characters. Allow a gel rim or sticker badge around actual avatars.
- Use `assets/images/icon.png` as the core product mark inside the global fart action. Avoid substitute cloud/wind glyphs, poop emoji, and bathroom clichés.

## Motion and Haptics

- Tap: 140ms compress to 0.96, short haptic, highlight travels across gel edge.
- Hold: progress ring fills continuously; gel swells 2–4%; waveform responds to audio.
- Recording: yellow timer and pressure feedback; do not flash the whole screen.
- Send: 220ms elastic release with one short gas-particle trail.
- Incoming: idle hero breathes subtly; holding locks into steady lime progress.
- Transition: use the existing cloud wipe selectively for major audio moments, not every route.
- Reduced motion: replace swelling, particles, and elastic overshoot with opacity and border-state changes.

## Copy Voice

Use short, confident, stupidly official language. Good examples: “Hold to listen,” “Fart back,” “Public drop,” “Walked through,” “Saved,” and “Reaction ready.” Do not invent lore, currencies, streaks, rarity, or XP unless the product adds those systems.

## Accessibility

- Maintain WCAG AA contrast for text and essential icons.
- Never require hue alone to distinguish public/private, recording/idle, or enabled/disabled.
- Provide a reduced-transparency rendering with more opaque raised plum surfaces.
- Keep focus states as a 2px candy-white or cyan ring outside the component edge.
- Preserve native text scaling; decorative display type may wrap but must not clip.
- Keep audio actions labeled and expose progress/state semantically.

## Anti-Patterns

- Do not cover every object in chrome, gloss, glow, or slime.
- Do not use anime avatars as a substitute for real user identity.
- Do not place decorative fog behind controls.
- Do not build a generic cyberpunk HUD; this is social toy-tech, not military telemetry.
- Do not make every label a sticker.
- Do not add fictional tabs, streaks, public/private radar filters, trophies, or currencies.
- Do not let visual jokes obscure consent, privacy, location, or destructive actions.
