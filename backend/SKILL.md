---
name: "backend"
description: "Use for backend API development including Supabase Edge Functions (Deno), REST API design, request/response patterns, auth middleware, error handling, input validation, CORS, rate limiting, and service-based architecture. Covers both Deno/TypeScript (Supabase) and Node.js/Python backends."
---

# Backend Development

You build backends that are boring in the best way: predictable, observable, and hard to misuse. Every endpoint validates input, authenticates the caller, and returns consistent response shapes.

## When to use
- Create or modify API endpoints (Edge Functions, REST, GraphQL)
- Design service-based backend architecture
- Implement authentication and authorization
- Add input validation and error handling
- Debug backend performance issues

## Supabase Edge Function Patterns

### Service-Based Router (Single Function, Multiple Actions)
```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });

  try {
    const { action, ...params } = await req.json();
    const user = await getAuthUser(req);  // throws if unauthorized

    const handlers: Record<string, Function> = {
      create: () => handleCreate(user, params),
      list: () => handleList(user, params),
      delete: () => handleDelete(user, params),
    };

    const handler = handlers[action];
    if (!handler) return errorResponse(400, `Unknown action: ${action}`);

    const data = await handler();
    return jsonResponse({ data });
  } catch (error) {
    const status = error.message === "Unauthorized" ? 401 : 500;
    return errorResponse(status, error.message);
  }
});

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}

function errorResponse(status: number, message: string) {
  return jsonResponse({ error: message }, status);
}
```

### Auth Helper
```typescript
import { createClient } from "jsr:@supabase/supabase-js@2";

async function getAuthUser(req: Request) {
  const authHeader = req.headers.get("Authorization");
  if (!authHeader) throw new Error("Unauthorized");

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_ANON_KEY")!,
    { global: { headers: { Authorization: authHeader } } }
  );

  const { data: { user }, error } = await supabase.auth.getUser();
  if (error || !user) throw new Error("Unauthorized");
  return { supabase, user };
}
```

### Admin Client (Bypasses RLS)
```typescript
const supabaseAdmin = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  { auth: { autoRefreshToken: false, persistSession: false } }
);
```

## API Design Rules

### Response Shape (Always Consistent)
```typescript
// Success
{ "data": { ... } }
{ "data": [...], "count": 42, "cursor": "abc123" }

// Error
{ "error": "Human-readable message" }
{ "error": "Validation failed", "details": { "field": "reason" } }
```

### Input Validation (At the Boundary)
```typescript
function validateCreateFart(params: unknown): CreateFartParams {
  const { content, lat, lng, audio_url } = params as any;

  if (!content || typeof content !== "string" || content.length > 500)
    throw new Error("content must be a string under 500 chars");
  if (typeof lat !== "number" || lat < -90 || lat > 90)
    throw new Error("lat must be between -90 and 90");
  if (typeof lng !== "number" || lng < -180 || lng > 180)
    throw new Error("lng must be between -180 and 180");

  return { content, lat, lng, audio_url: audio_url ?? null };
}
```

### Pagination (Keyset, Not Offset)
```typescript
// Client sends: { cursor: "2024-01-15T10:30:00Z", limit: 20 }
const { data } = await supabase
  .from("farts")
  .select()
  .lt("created_at", cursor)
  .order("created_at", { ascending: false })
  .limit(limit);

// Return next cursor
const nextCursor = data.length === limit ? data[data.length - 1].created_at : null;
return { data, cursor: nextCursor };
```

## Cost Decision Tree

```
Can the database do it automatically?
  YES → Database trigger (free, instant, no Edge Function call)
  NO  ↓

Is it a scheduled/periodic task?
  YES → pg_cron job (free, runs in Postgres)
  NO  ↓

Is it a read query that rarely changes?
  YES → Materialized view + pg_cron refresh
  NO  ↓

Does it need external API calls?
  YES → Edge Function (this is what they're for)
  NO  → RLS policy or database function (RPC)
```

## Deployment
```
# Via MCP (preferred)
deploy_edge_function({
  project_id: "your-ref",
  name: "fart_service",
  entrypoint_path: "index.ts",
  verify_jwt: true,
  files: [{ name: "index.ts", content: "..." }]
})

# Via CLI
supabase functions deploy fart_service
```

## Anti-Patterns
- Trusting client-provided user IDs — always use `auth.uid()` from JWT
- Returning full database rows to client — select only needed fields
- Using service role key where anon key suffices — principle of least privilege
- Making Edge Functions for simple CRUD — use PostgREST (Supabase client) + RLS instead
- Logging request bodies containing passwords or tokens
- Catching errors silently (`catch (e) {}`) — always log or return the error
