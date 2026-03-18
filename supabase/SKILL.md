---
name: "supabase"
description: "Use for Supabase platform development including project management, database queries, auth configuration, storage, realtime channels, Edge Functions deployment, branching, and MCP tool usage. Covers Flutter/Dart client, JavaScript client, PostgREST, and Supabase CLI patterns."
---

# Supabase Platform Development

## When to use
- Manage Supabase projects (create, pause, restore, list)
- Query or modify the PostgreSQL database via Supabase
- Configure Supabase Auth (email, phone, OAuth, SSO)
- Work with Supabase Storage (buckets, policies, CDN)
- Set up Realtime channels (presence, broadcast, postgres changes)
- Deploy or debug Edge Functions
- Generate TypeScript types from the database schema
- Use Supabase MCP tools for any of the above
- Integrate Supabase with Flutter/Dart or JavaScript/TypeScript clients

## MCP Tool Reference

### Discovery & Configuration
- `search_docs` — GraphQL search against live Supabase docs. **Always query docs first** even if you think you know the answer; docs update frequently.
- `list_projects` — List all projects to find project IDs.
- `get_project` — Get project details (status, region, tier).
- `get_project_url` — Get the API URL for the connected project.
- `get_publishable_keys` — Get anon/publishable keys. Prefer `sb_publishable_*` format keys.

### Database
- `list_tables` — List tables in schemas. Use `verbose: true` for columns, PKs, FKs.
- `execute_sql` — Run read queries (SELECT) or DML (INSERT/UPDATE/DELETE). **Not for DDL.**
- `apply_migration` — Run DDL (CREATE TABLE, ALTER, etc.). Use snake_case names.
- `list_migrations` — See applied migrations.
- `list_extensions` — Check installed Postgres extensions.
- `generate_typescript_types` — Generate TypeScript types from schema.

### Edge Functions
- `list_edge_functions` — List all deployed functions.
- `get_edge_function` — Read function source code.
- `deploy_edge_function` — Deploy or update a function. Include `deno.json` if present.

### Branching
- `create_branch` — Create a dev branch (runs all migrations on fresh DB).
- `list_branches` — Check branch status.
- `merge_branch` / `rebase_branch` / `reset_branch` / `delete_branch` — Branch lifecycle.

### Observability
- `get_logs` — Fetch 24h logs by service: `api`, `postgres`, `edge-function`, `auth`, `storage`, `realtime`, `branch-action`.
- `get_advisors` — Security and performance advisories. **Run after DDL changes** to catch missing RLS policies.

## Key Patterns

### Flutter/Dart Client
```dart
// Initialize
final supabase = Supabase.instance.client;

// Query
final data = await supabase.from('farts').select().eq('user_id', uid);

// Insert
await supabase.from('farts').insert({'content': 'hello', 'user_id': uid});

// RPC (call database function)
final result = await supabase.rpc('get_nearby_farts', params: {'lat': 37.7, 'lng': -122.4});

// Realtime
supabase.channel('room1')
  .onPostgresChanges(event: PostgresChangeEvent.all, schema: 'public', table: 'messages',
    callback: (payload) => print(payload))
  .subscribe();

// Auth
await supabase.auth.signInWithOtp(phone: '+1234567890');
final session = supabase.auth.currentSession;
```

### Edge Function Pattern (Deno)
```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

Deno.serve(async (req: Request) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );

  const { data, error } = await supabase.from("table").select();
  return new Response(JSON.stringify({ data, error }), {
    headers: { "Content-Type": "application/json" },
  });
});
```

### Cost Optimization Checklist
1. Use database triggers instead of Edge Functions for counters/aggregations
2. Batch notifications (pg_cron every 5 min) instead of individual sends
3. Use materialized views for leaderboards/aggregations (refresh on schedule)
4. Enforce RLS at database level to reduce Edge Function calls by 50%
5. Use PostGIS for spatial queries (10-50x faster than geohash approximation)
6. Use pg_cron for scheduled maintenance instead of external schedulers

### Security Defaults
- **Always enable JWT verification** on Edge Functions unless custom auth is implemented
- Run `get_advisors(type: "security")` after any DDL change
- Enable RLS on every public table — no exceptions
- Use `auth.uid()` in RLS policies, never trust client-provided user IDs
- Service role key stays server-side only (Edge Functions, backend)
