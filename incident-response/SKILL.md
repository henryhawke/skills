---
name: "incident-response"
description: "Use for production incident response, outage triage, root cause analysis, blameless post-mortems, runbook creation, and SRE practices. Covers Supabase-specific debugging (Edge Function failures, database issues, auth problems), log analysis, and incident communication."
---

# Incident Response & SRE

You triage by impact, not by panic level. Step one is always: is the system still degraded? If yes, mitigate first, investigate later. Post-mortems are about systems, not people.

## When to use
- Production is down or degraded
- Users are reporting errors
- Monitoring alerts are firing
- Need to write a post-mortem
- Creating runbooks for known failure modes

## Incident Response Protocol

### 1. ASSESS (First 5 Minutes)
- **What's broken?** Check dashboards, error rates, user reports
- **Who's affected?** All users, specific region, specific feature?
- **When did it start?** Correlate with recent deploys or changes
- **Is it getting worse?** Check if error rate is increasing

### 2. MITIGATE (Stop the Bleeding)
```
Can you revert the last deploy?    → Revert and verify
Is it a database issue?            → Check connections, locks, disk space
Is it an Edge Function failure?    → Check logs, redeploy known-good version
Is it a third-party outage?       → Enable fallback/graceful degradation
Is it a traffic spike?             → Scale resources or enable rate limiting
```

### 3. INVESTIGATE (After Mitigation)
Use the Supabase MCP tools:
```
get_logs(service: "edge-function")  # Edge Function errors
get_logs(service: "postgres")       # Database errors
get_logs(service: "auth")           # Authentication issues
get_logs(service: "api")            # PostgREST/API gateway
get_advisors(type: "performance")   # Performance issues
```

### 4. COMMUNICATE
- **Internal**: What's broken, what we're doing, ETA if known
- **Users**: Acknowledge the issue, no false promises on timeline

### 5. RESOLVE & DOCUMENT
- Deploy the fix
- Verify metrics return to normal
- Write a blameless post-mortem

## Supabase-Specific Failure Modes

| Symptom | Check | Common Cause |
|---|---|---|
| 500 errors on API calls | `get_logs(service: "api")` | Database connection pool exhausted |
| Edge Function timeout | `get_logs(service: "edge-function")` | Slow query or external API timeout |
| Auth failures (401/403) | `get_logs(service: "auth")` | JWT expired, RLS policy blocking |
| Realtime not updating | `get_logs(service: "realtime")` | Channel not subscribed, RLS on table |
| Storage upload fails | `get_logs(service: "storage")` | Bucket policy, file size limit |
| Slow queries | `get_advisors(type: "performance")` | Missing index, sequential scan |

## Post-Mortem Template

```markdown
## Incident: [Brief Description]
**Date**: YYYY-MM-DD
**Duration**: X hours Y minutes
**Impact**: [Who was affected and how]
**Severity**: P1/P2/P3

### Timeline
- HH:MM — First alert / user report
- HH:MM — Investigation started
- HH:MM — Root cause identified
- HH:MM — Mitigation applied
- HH:MM — Full resolution confirmed

### Root Cause
[What actually went wrong at the system level — no blame, no names]

### What Went Well
- [Things that helped detection/resolution]

### What Could Be Improved
- [Gaps in monitoring, testing, or process]

### Action Items
- [ ] [Specific fix] — Owner — Due date
- [ ] [Monitoring improvement] — Owner — Due date
- [ ] [Process change] — Owner — Due date
```

## Runbook Essentials

A good runbook answers these for every failure mode:
1. **How will I know?** (alert, error message, user report)
2. **How do I verify?** (dashboard, query, health check)
3. **What do I do?** (step-by-step, not "investigate")
4. **How do I confirm it's fixed?** (metric returns to normal, test passes)
5. **Who do I escalate to?** (if steps don't resolve it)
