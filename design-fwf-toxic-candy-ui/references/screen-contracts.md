# Verified Screen Contracts

Use these contracts when designing or implementing the active app. Verify source again if routes or flows have changed.

## Global Shell

- Navigation order: Fart Map, Inbox, 80px center Fart button, Saved, Profile.
- Hide/show dock and fart action with the existing scroll behavior.
- Keep safe-area behavior, max-width dock, and 44–48px touch targets.

## Inbox and Friends

Source: `lib/presentation/screens/home/snap_feed_hub_screen.dart`.

- Keep the `Inbox | Friends` segmented control and unread badge.
- Show profile, search, and requests in top chrome.
- Support farts, replies, and reaction clips in the inbox queue.
- Route fart rows to Incoming and reaction clips to their viewer.
- Provide populated, unread/new, empty, loading, and error states.

## Global Fart Composer

Sources: `lib/presentation/widgets/common/fart_button.dart` and `lib/presentation/widgets/common/snap_shell_scaffold.dart`.

- Keep the persistent 80px center-docked action.
- Render `assets/images/icon.png` inside it while preserving semantics and state feedback.
- Tap performs quick-send behavior; hold records up to 10 seconds.
- Show idle, pressure, recording timer/waveform, cooldown, and error feedback.
- Target selection is Private or Fart Map, with an Edit path.
- Private requires an explicit friend/group recipient.
- Fart Map is public and requires location.
- Preserve reply/source/inbox intent when editing.

## Incoming and Reaction

Source: `lib/presentation/screens/social/incoming_fart_screen.dart`.

- Require press-and-hold to play; show progress while held.
- After explicit consent, start reaction recording automatically with the hold and stop it when playback/hold ends.
- Show sender, distance, and delivery context.
- Offer Save and Fart Back after listening.
- Gate simultaneous reaction capture behind camera/mic consent.
- Require reaction preview before sending.
- Offer None, Slow-mo, and High-pitch effects.
- Offer discard, listen again, and send reaction.

## Fart Map and Public Detail

Sources: `lib/presentation/screens/map/fart_map_screen.dart` and `lib/presentation/screens/map/fart_detail_screen.dart`.

- Fart Map contains public drops only. Permit `Everyone | My friends` as an authorship filter over public drops; never add a private browsing toggle.
- Support marker clusters and a selected-marker detail state.
- Show nearby public drops, walked-through encounters, and tracking/queued metrics.
- Include recenter, refresh, fullscreen, and live/cached/offline status.
- Public detail includes identity/anonymous state, time, optional secret message, listens, Public Map badge, playable audio, Share, Fart Back, and Refresh.

## Saved

Source: `lib/presentation/screens/profile/fart_bank_screen.dart`.

- Use a two-column grid; allow three columns on wide layouts.
- Keep stats, sort/filter, playable/unplayable status, pagination, and empty/loading/error states.
- Support replay, rename, highlight, share, remove, and the social-selection overlay.
- Public-only is a filter, not a separate library.

## Onboarding

Sources: `lib/presentation/screens/auth/onboarding_screen.dart` and `lib/presentation/screens/onboarding/tutorial_overlay.dart`.

- Ask for a unique Fart Tag with availability, suggestions, and offline queued state.
- Offer an optional avatar.
- Teach the center Fart button, Map/location, and friend discovery.
- Ask explicitly for camera/mic reaction consent and provide Not Now.
- Guide the first fart and then complete onboarding.

## Profile

Source: `lib/presentation/screens/profile/profile_screen.dart`.

- Support own-profile and other-profile states.
- Show avatar, username, member-since, Farts, Friends, and Walked Through.
- Own profile exposes notifications, settings, friends, invite, and share.
- Other profile exposes unfriend, block, and report safety actions.

## Required Mockup Set

Produce these boards for a comprehensive visual pass:

1. Inbox and Friends — populated/unread plus Friends segment.
2. Composer — idle, recording, and target chooser.
3. Incoming — pre-listen, holding/listening, and reaction preview.
4. Fart Map — main map and selected public-drop detail.
5. Saved — library grid and filter/selection state.
6. Onboarding — Fart Tag, tutorial, consent, and first-fart handoff.
7. Profile — own profile and other-user safety variant.
