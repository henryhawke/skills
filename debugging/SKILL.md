---
name: "debugging"
description: "Use when debugging errors, crashes, test failures, unexpected behavior, performance issues, or production incidents. Covers systematic root cause analysis, Flutter debugging, Edge Function debugging, log analysis, git bisect, and common failure patterns."
---

# Debugging & Root Cause Analysis

You are a detective, not a guesser. You form hypotheses from evidence, test them, and narrow down. You never shotgun-fix by changing random things.

## When to use
- Any error, crash, or unexpected behavior
- Test failures (local or CI)
- Performance regressions
- Production incidents
- "It works on my machine" problems

## The Debugging Protocol

### 1. REPRODUCE (before anything else)
- Can you trigger the bug reliably?
- What are the exact steps, inputs, and environment?
- If intermittent: what's the frequency? What varies between runs?

### 2. ISOLATE
- What changed since it last worked? (`git log --oneline -20`, `git diff`)
- Is it environment-specific? (iOS vs Android, debug vs release, local vs prod)
- Does it fail with minimal input? (reduce the test case)

### 3. HYPOTHESIZE (only after evidence gathering)
- Form 2-3 specific hypotheses
- For each: what would you expect to see if this hypothesis is correct?
- Test the easiest-to-disprove hypothesis first

### 4. VERIFY
- Add targeted logging or breakpoints
- Check one variable at a time
- When you find the cause, verify by reverting the fix — does the bug return?

### 5. FIX & PROTECT
- Fix the root cause, not the symptom
- Add a test that would have caught this
- Consider: are there similar bugs elsewhere? (same pattern, different location)

## Flutter-Specific Debugging

### Common Failures
| Symptom | Likely Cause | Fix |
|---|---|---|
| `type 'Null' is not a subtype` | Missing null check on JSON field | Add null-aware operator or default value in Freezed model |
| `setState() called after dispose()` | Async callback on unmounted widget | Check `mounted` before setState, or use Riverpod (auto-disposes) |
| `RenderFlex overflowed` | Content too wide/tall | Wrap in `Flexible`, `Expanded`, or `SingleChildScrollView` |
| `MissingPluginException` | Native plugin not registered | `flutter clean && flutter pub get`, rebuild |
| Build runner errors | Stale generated code | `dart run build_runner build --delete-conflicting-outputs` |
| Provider not found | Missing `ProviderScope` ancestor | Wrap app root in `ProviderScope` |

### Performance Debugging
```bash
# Profile mode (real device only)
flutter run --profile

# DevTools
flutter pub global activate devtools
dart devtools
```
- **Jank**: Check for expensive `build()` methods, unnecessary rebuilds
- **Memory**: Look for retained references, unclosed streams/controllers
- **Startup**: Profile with `Timeline.startSync()` / `Timeline.finishSync()`

## Edge Function Debugging

### Check Logs First
```
get_logs(service: "edge-function")  # Last 24h via MCP
```

### Common Failures
| Error | Cause | Fix |
|---|---|---|
| `Boot failure` | Syntax error or bad import | Check import paths, run locally first |
| `Worker exceeded resource limits` | Timeout or memory | Optimize query, add pagination |
| `401 Unauthorized` | Missing/invalid JWT | Check `verify_jwt` setting, validate token |
| `CORS error` in browser | Missing CORS headers | Add `corsHeaders` to response + OPTIONS handler |
| `Connection refused` to Postgres | Wrong connection method | Use Supabase client, not direct connection from edge |

### Local Testing
```bash
supabase functions serve my_function --env-file .env.local
# Then: curl -X POST http://localhost:54321/functions/v1/my_function
```

## Git Bisect (Finding When It Broke)
```bash
git bisect start
git bisect bad              # Current commit is broken
git bisect good abc123      # This commit was known-good
# Git checks out middle commit — test it, then:
git bisect good  # or  git bisect bad
# Repeat until Git identifies the exact commit
git bisect reset            # Done, return to original branch
```

## Log Reading Heuristics
- Read the **first** error in a cascade, not the last — later errors are often consequences
- Stack traces: read **bottom-up** for the call chain, but the **top frame** is where it failed
- Search for the **second occurrence** of an error — the first is often a red herring during startup
- `null` or `undefined` appearing where an object is expected → trace back to where that value was set

## Anti-Patterns (Things That Waste Time)
- Changing multiple things at once — you won't know which fixed it
- Adding `print()` statements everywhere — use targeted breakpoints or structured logging
- Googling the error before reading it — the message often tells you exactly what's wrong
- Assuming the bug is in library code — it's almost always in your code
- Fixing the symptom without understanding the cause — it will come back
