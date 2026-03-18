---
name: "security-audit"
description: "Use for security audits, vulnerability assessment, OWASP Top 10 checks, Supabase RLS verification, Edge Function auth review, secret scanning, dependency auditing, and DevSecOps pipeline setup. Covers both manual review and automated scanning."
---

# Security Auditing

You audit for exploitability, not theoretical risk. Every finding includes proof-of-concept severity, not just "this could be bad." You prioritize by blast radius: auth bypass > data leak > denial of service > information disclosure.

## When to use
- Audit a codebase or feature for security vulnerabilities
- Review authentication and authorization logic
- Check for OWASP Top 10 vulnerabilities
- Verify Supabase RLS policies are correct
- Scan for exposed secrets or insecure dependencies
- Set up security scanning in CI/CD

## Audit Workflow

### 1. Attack Surface Mapping
- List all entry points: API endpoints, Edge Functions, client-side forms
- Identify auth boundaries: which endpoints are public, which require auth?
- Map data flows: where does user input go? Where does sensitive data live?
- Check third-party integrations: webhooks, OAuth providers, payment processors

### 2. Authentication & Authorization Review
```
For each endpoint:
  ✓ Is authentication required? (verify_jwt, auth middleware)
  ✓ Is the authenticated user authorized for this action? (RLS, role check)
  ✓ Can a user escalate privileges? (modify user_id in request body)
  ✓ Are tokens validated correctly? (signature, expiration, audience)
```

### 3. Input Validation Audit
```
For each user input:
  ✓ Is it validated before use? (type, length, format)
  ✓ Is it sanitized before database insertion? (SQL injection)
  ✓ Is it sanitized before HTML rendering? (XSS)
  ✓ Can oversized input cause DoS? (file uploads, JSON payloads)
```

### 4. Supabase-Specific Checks
```sql
-- Tables without RLS (CRITICAL)
SELECT schemaname, tablename FROM pg_tables
WHERE schemaname = 'public'
AND tablename NOT IN (
  SELECT relname FROM pg_class WHERE relrowsecurity = true
);

-- Tables with RLS enabled but NO policies (data is inaccessible)
SELECT c.relname FROM pg_class c
WHERE c.relrowsecurity = true
AND NOT EXISTS (SELECT 1 FROM pg_policies p WHERE p.tablename = c.relname);
```

Also run: `get_advisors(type: "security")` via MCP after any DDL change.

### 5. Secret Scanning
```bash
# Check for hardcoded secrets
grep -rn "sk_live\|sk_test\|supabase_service_role\|SUPABASE_SERVICE_ROLE_KEY\|password\s*=" --include="*.ts" --include="*.dart" --include="*.json" .

# Check .gitignore covers sensitive files
# These should NEVER be committed:
# .env, .env.local, .env.production
# *-credentials.json, service-account-key.json
# *.p8, *.p12 (Apple signing keys)
```

### 6. Dependency Audit
```bash
# Flutter
flutter pub outdated
# Check for known vulnerabilities in pubspec.lock

# Node/Bun
npm audit      # or
bun pm audit   # if available
```

## OWASP Top 10 Quick Check

| # | Vulnerability | What to Look For |
|---|---|---|
| A01 | Broken Access Control | Missing auth checks, IDOR (user A sees user B's data), missing RLS |
| A02 | Cryptographic Failures | Hardcoded keys, weak hashing, HTTP instead of HTTPS |
| A03 | Injection | Unparameterized SQL, unsanitized HTML output, command injection |
| A04 | Insecure Design | Missing rate limiting, no account lockout, predictable tokens |
| A05 | Security Misconfiguration | Default credentials, verbose errors in production, open CORS |
| A06 | Vulnerable Components | Outdated dependencies with known CVEs |
| A07 | Auth Failures | Weak passwords allowed, no MFA, session fixation |
| A08 | Data Integrity Failures | No webhook signature verification, insecure deserialization |
| A09 | Logging Failures | Logging passwords/tokens, no audit trail for sensitive ops |
| A10 | SSRF | User-controlled URLs fetched server-side without validation |

## Output Format

```
## Security Audit Report

### Critical (Exploit Now)
- [Finding + proof of concept + fix]

### High (Exploit with Effort)
- [Finding + conditions + fix]

### Medium (Defense in Depth)
- [Finding + risk + recommendation]

### Verified Secure
- [What you checked and confirmed is correctly implemented]
```

## Common Supabase Security Mistakes
1. **`verify_jwt: false`** on Edge Function without alternative auth
2. **Missing RLS** on tables with user data
3. **Service role key** referenced in client-side code
4. **Webhook endpoints** without signature verification (Apple S2S, Stripe)
5. **RLS policy using `auth.uid() = user_id`** but the `user_id` column is user-writable
6. **Overly permissive CORS** (`*`) on authenticated endpoints
