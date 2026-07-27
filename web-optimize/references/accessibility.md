# Accessibility reference

Use this reference for WCAG 2.2 audits and remediation. Automated tools find only a subset of barriers; combine them with manual interaction and assistive-technology checks.

## Contents

- [Scope and conformance](#scope-and-conformance)
- [Perceivable](#perceivable)
- [Operable](#operable)
- [Understandable](#understandable)
- [Robust](#robust)
- [Testing](#testing)
- [Impact and reporting](#impact-and-reporting)
- [Primary sources](#primary-sources)

## Scope and conformance

Use the POUR model:

| Principle | Question |
|---|---|
| Perceivable | Can users perceive the content in different ways? |
| Operable | Can users complete every action with supported inputs? |
| Understandable | Are content, state, instructions, and errors clear? |
| Robust | Do semantics and state work with assistive technologies? |

WCAG levels:

- A: foundational requirements.
- AA: common organizational target.
- AAA: enhanced criteria, generally scoped selectively.

Do not call a site legally compliant based on a code scan, Lighthouse, or a limited sample. Name the WCAG version/level, pages, states, methods, assistive technologies, browsers, exclusions, and unresolved manual checks.

## Perceivable

### Text alternatives

```html
<img src="/sales-chart.png" alt="Quarterly sales rose from $2M to $2.8M">
<img src="/decorative-border.svg" alt="">

<figure>
  <img src="/market-map.png" alt="Market coverage map" aria-describedby="map-details">
  <figcaption id="map-details">Detailed regions and values…</figcaption>
</figure>
```

- Describe the image's purpose in context, not every visual detail.
- Use empty alt text for decorative images.
- Give complex charts an equivalent data table or long description.
- Avoid redundant `role="presentation"` on an image with `alt=""` unless a tested compatibility need exists.

### Accessible names

```html
<button type="button">
  <svg aria-hidden="true"><!-- icon --></svg>
  <span class="visually-hidden">Open menu</span>
</button>
```

Verify the computed accessible name; visible labels and accessible names should align.

```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
  border: 0;
}
```

### Contrast and non-color cues

For WCAG 2.2 AA:

| Content | Minimum contrast |
|---|---:|
| Normal text | `4.5:1` |
| Large text | `3:1` |
| UI components and meaningful graphics | `3:1` against adjacent colors |

AAA text targets are `7:1` normal and `4.5:1` large. Calculate rendered foreground/background across states, gradients, transparency, themes, and images.

Do not rely on color alone. Pair error/success/status color with text, shape, iconography, or patterns.

### Media

Provide captions for synchronized video, transcripts for audio, and audio description or an equivalent alternative where required by scope. Test keyboard control, focus, labels, autoplay, and reduced-motion behavior.

## Operable

### Keyboard

Prefer native controls. A native button already supplies click, keyboard activation, focus, role, and disabled semantics.

```html
<button type="button">Save changes</button>
```

If a custom widget is unavoidable, implement the full Authoring Practices interaction model, including focus movement, key handling, role, state, and announcements. Verify users can Tab into and out of every component without a trap.

### Focus

```css
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

:focus {
  scroll-margin-block: 80px 60px;
}
```

- Never remove focus without an equal or better visible replacement.
- Keep focus order logical and aligned with task order.
- Move focus only when interaction context requires it.
- Restore focus after dialogs/overlays.
- Ensure sticky headers, cookie banners, and panels do not obscure focused elements (WCAG 2.2 2.4.11).

### Bypass and landmarks

Provide a visible-on-focus skip link to the primary content. Use a single main landmark and clearly labeled repeated navigation/region landmarks.

### Target size

WCAG 2.2 AA criterion 2.5.8 uses a 24 by 24 CSS-pixel minimum with spacing and other defined exceptions. A comfortable 44 by 44 target is a useful enhanced design target and aligns with AAA 2.5.5, but do not report it as the universal AA minimum.

### Dragging

Any function requiring dragging needs a single-pointer alternative, such as move buttons, a position input, or a menu action, unless an exception applies.

### Timing and motion

- Let users extend or disable time limits when required.
- Provide pause/stop controls for moving or auto-updating content.
- Avoid unexpected context changes on focus/input.
- Respect reduced-motion preferences.

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Prefer component-level reduced-motion design when a global override would break necessary progress/state cues.

## Understandable

### Language and consistency

Set the page language and mark changes of language:

```html
<html lang="en">
<p>The French greeting is <span lang="fr">bonjour</span>.</p>
```

Keep repeated navigation and help mechanisms in a consistent relative order (including WCAG 2.2 3.2.6).

### Forms

- Give every input a programmatic label.
- Group related controls with `fieldset` and `legend`.
- Connect instructions and errors with `aria-describedby`.
- Set appropriate `autocomplete`, input type, and input mode.
- Preserve user-entered values after validation failures.
- Identify required fields in text/semantics, not color alone.

```html
<label for="email">Email</label>
<input
  id="email"
  name="email"
  type="email"
  autocomplete="email"
  aria-describedby="email-help email-error"
  aria-invalid="true"
>
<p id="email-help">Use the address where you receive orders.</p>
<p id="email-error" role="alert">Enter a valid email address.</p>
```

On submit, provide an error summary and focus it or the first invalid field according to the product pattern. Ensure asynchronous errors are announced once without flooding live regions.

### Redundant entry

Do not force users to re-enter information already provided in the same process when it can be safely reused or selected. Preserve security re-confirmation where necessary.

### Accessible authentication

- Allow password managers, autofill, and paste.
- Use `autocomplete="current-password"` or `new-password` correctly.
- Offer alternatives such as passkeys, SSO, or email links when available.
- Avoid cognitive-function tests without an allowed alternative/exception.

## Robust

### Native semantics first

```html
<button type="button">Open</button>
<label><input type="checkbox"> Send updates</label>
```

Avoid rebuilding these with `div` plus ARIA. ARIA does not add behavior.

For custom widgets, test the complete name, role, value/state, keyboard pattern, focus ownership, and dynamic updates against the WAI-ARIA Authoring Practices.

### Dynamic content

Use live regions for important status that changes without moving focus:

```html
<p id="save-status" role="status" aria-live="polite"></p>
```

- Use polite announcements for status, assertive alerts sparingly.
- Insert or establish the live region before changing its content.
- Avoid announcing the same update multiple times.
- Do not use a live region as a substitute for visible feedback.

### Markup

Check duplicate IDs, invalid relationships, nested interactive controls, heading/landmark structure, labels, table semantics, dialog ownership, and DOM order. HTML validity alone does not prove accessibility, but broken relationships can be real blockers.

## Testing

### Automated

Use project-installed tools when possible:

```bash
npx lighthouse https://example.com --only-categories=accessibility
npx axe https://example.com
```

Do not install global tools or new dependencies without authorization. Record tool versions, rules, URL/state, browser, and exclusions.

### Manual

- [ ] Keyboard: Tab/Shift+Tab, Enter, Space, arrows, Escape, shortcuts.
- [ ] Focus: visible, logical, not obscured, restored after overlays.
- [ ] Screen reader: representative flows with VoiceOver, NVDA, JAWS, or TalkBack as available.
- [ ] Zoom/reflow: 200% zoom and relevant 320 CSS-pixel reflow behavior.
- [ ] Contrast: text, icons, borders, focus, hover, disabled, error, dark mode.
- [ ] Motion: reduced motion and pause/stop behavior.
- [ ] Forms: labels, instructions, errors, preservation, completion.
- [ ] Media: captions, transcript, descriptions, player operation.
- [ ] Pointer/touch: target size, spacing, dragging alternative.
- [ ] Authentication: paste/autofill/password-manager behavior.

Test loading, empty, error, success, disabled, expanded, selected, invalid, stale, and responsive states—not just the initial page.

## Impact and reporting

Typical critical/high barriers include:

- essential actions impossible by keyboard;
- keyboard traps;
- missing names/labels on essential controls;
- inaccessible authentication;
- severe contrast on essential content;
- focus loss/obscuration that blocks completion;
- unannounced errors that prevent recovery.

Moderate/low severity depends on scope, frequency, workaround, and user impact. Do not copy a generic severity list without reproducing the actual barrier.

For each finding, include WCAG criterion when confidently mapped, affected users, exact element/state, reproduction steps, evidence type, code owner, fix, and manual validation. Call an automated pass `no automated violations detected`, not `accessible`.

## Primary sources

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [Understanding Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum)
