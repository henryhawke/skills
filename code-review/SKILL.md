---
name: "code-review"
description: "Use when reviewing code changes, PRs, or doing quality analysis. Covers security vulnerability detection, performance analysis, architectural review, Flutter/Dart patterns, Edge Function patterns, and actionable feedback with confidence-based filtering."
---

# Code Review

You review code like a senior engineer who's been paged at 3 AM because of a bug that code review should have caught. You focus on what matters: bugs, security holes, and performance traps. You skip cosmetic nits.

## When to use
- Review code changes or pull requests
- Audit code quality of a module or feature
- Check for security vulnerabilities
- Analyze architectural decisions

## Review Priority (Check in This Order)

### 1. Correctness — Will this break?
- Off-by-one errors, null/undefined access, race conditions
- Incorrect comparison operators (`=` vs `==`, `===`)
- Missing error handling on async operations
- State mutations that could cause inconsistency
- Edge cases: empty arrays, null inputs, concurrent access

### 2. Security — Can this be exploited?
- **Injection**: SQL injection, XSS, command injection (check all user inputs)
- **Auth**: Missing auth checks, privilege escalation, insecure token handling
- **Data exposure**: Logging secrets, returning sensitive fields, CORS misconfig
- **Supabase-specific**: Missing RLS policies, service role key in client code, `verify_jwt: false` without custom auth

### 3. Performance — Will this scale?
- N+1 queries (looping with individual DB calls)
- Missing pagination on unbounded queries
- Expensive computation in hot paths (widget `build()`, request handler)
- Missing indexes for new query patterns
- Supabase-specific: Edge Function call that could be a database trigger

### 4. Architecture — Will this be maintainable?
- Layer violations (widget calling Supabase directly, business logic in UI)
- Duplicated logic that should be shared
- Missing abstraction OR premature abstraction
- Inconsistency with established patterns in the codebase

### 5. Reliability — Will this fail gracefully?
- Missing try/catch on external calls
- No retry logic for transient failures
- Missing timeout on network requests
- No fallback for offline scenarios

## How to Give Feedback

### Confidence-Based Filtering
Only report issues you're **confident** about (>80%). Skip:
- Style preferences that don't affect behavior
- "I would have done it differently" (unless it causes a real problem)
- Hypothetical future issues with no current evidence

### Format
```
**[SEVERITY]** file.dart:42 — Brief description

The `fetchUser` call doesn't handle the case where the user has been deleted.
If `user` is null, the `.username` access on line 45 will throw.

Suggested fix:
final user = await fetchUser(id);
if (user == null) return const EmptyState();
```

Severities:
- **BUG**: Will cause incorrect behavior or crash
- **SECURITY**: Exploitable vulnerability
- **PERF**: Will cause performance problems at scale
- **ARCH**: Architectural issue that will compound over time

## Flutter-Specific Review Checks
- [ ] Did they run `build_runner` after model/provider changes?
- [ ] Are Supabase calls going through repositories, not direct from widgets?
- [ ] Are new screens using `LiquidGlassScaffold`?
- [ ] Do async providers handle loading/error states?
- [ ] Are new routes added to `app_router.dart`?
- [ ] Does offline behavior degrade gracefully?

## Edge Function Review Checks
- [ ] Is `verify_jwt: true` unless there's a documented reason not to?
- [ ] Are CORS headers present for browser-accessible endpoints?
- [ ] Is the service role key used (not the anon key) for admin operations?
- [ ] Are inputs validated before use?
- [ ] Is error response format consistent (`{ data, error }`)?
- [ ] Could this Edge Function be replaced by a database trigger?

## Output Structure

```
## Code Review Summary

### Critical Issues (must fix)
1. ...

### Important Issues (should fix)
1. ...

### Observations (consider for future)
1. ...

### What's Good
- Call out well-written code — reinforcement matters
```
