# FWF Design Bible Laws

Apply these inherited design-bible rules before the Toxic Candy surface treatment.

## Three-question gate

1. Explain itself: a first-time user identifies the screen job and hero within three seconds.
2. Feel alive: every touch receives visible feedback within 100ms.
3. Get out of the way: content owns the ground layer; chrome is a quiet floating control layer.

## Ten laws

1. Name exactly one hero per screen.
2. Build hierarchy with scale, color, shape, motion, and containment—not clutter.
3. Use the fixed radius scale and nested-radius rule; avoid arbitrary sharp corners.
4. Keep hit targets at least 44pt on iOS and 48dp on Android.
5. Specify default, pressed, focus, disabled, loading, and error for every interactive component.
6. Use motion only to explain origin, state, progress, or outcome; repeated actions stay under 150ms.
7. Design empty, loading, partial, long, error, and offline states before declaring a screen complete.
8. Spend delight by frequency; the 50th repetition must still feel good.
9. Pair color with icon, label, shape, or motion and meet contrast requirements.
10. Introduce at most one unfamiliar pattern per screen and always provide a visible fallback.

## FWF personality

Use three adjectives: **tactile, shameless, precise**. Tactile supplies gel and pressure feedback. Shameless supplies copy and the absurd premise. Precise keeps consent, privacy, audio, navigation, and errors crystal clear.

## Novel interaction rule

The global fart action and hold-to-listen are the only signature verbs. Teach them through affordance, responsive progress, and safe release. Do not invent novel gestures in navigation, Saved, Profile, or map filtering.

## Motion budget

- Press/toggle: 100–150ms.
- Chip or small element: 150–200ms.
- Selection/tab state: 200–250ms.
- Sheet/screen transition: 300–400ms.
- Rare celebration: 400–600ms.
- Reduced motion: cross-fade, border, and opacity alternatives; no parallax or looping gas motion.

## Craft gate

Reject output with magic-number spacing, mixed icon families, nested cards, unlabeled gestures, silent async work, lost input on failure, inaccessible text scaling, or flourish-dependent comprehension.
