---
name: "i18n-locale-readiness"
description: "Prepare UI work for translation, locale formatting, pluralization, and multilingual edge cases. Use when Codex needs a stable i18n plan, ICU-style messages, Intl formatting guidance, or locale-readiness review before shipping UI copy."
---

# I18n Locale Readiness

Make localization explicit early. Avoid concatenated strings, use stable keys, and treat pluralization, formatting, and text expansion as product requirements.

## Workflow
1. Define message-key structure and naming conventions.
2. Provide representative ICU-style messages for plurals or selects.
3. Specify formatting via Intl APIs for dates, money, units, and relative time as needed.
4. List likely failure modes such as missing keys, RTL, or expansion issues, then return a checklist.

## Inputs
- UI surface
- Target locales
- Formatting needs

## Deliverables
- JSON with `keying`, `messages`, `formatting`, `pitfalls`, and `skill_log`
- Message-catalog starter content

## Quality Gates
- No string-concatenation localization patterns.
- Plural or select behavior is explicit when counts or variants exist.
- Formatting decisions are locale-aware rather than hard-coded.
- Missing translation risks are surfaced early.

## Prompt Scaffold
```text
SYSTEM
You are an internationalization engineer.

USER
Inputs:
- UI surface
- Target locales
- Formatting needs

Task:
Return a locale-readiness plan, message examples, and extraction guidance in JSON.

Output requirements:
- JSON with `keying`, `messages`, `formatting`, `pitfalls`, and `skill_log`
- Message-catalog starter content
```
