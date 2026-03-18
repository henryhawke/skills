---
name: "supabase-edge-functions"
description: "Use for creating, deploying, debugging, and optimizing Supabase Edge Functions. Covers Deno runtime, request handling, auth validation, CORS, shared utilities, service-based architecture, and the deploy_edge_function MCP tool."
---

# Supabase Edge Functions

## When to use
- Create new Edge Functions (Deno/TypeScript)
- Deploy or update existing functions via MCP
- Debug Edge Function errors using logs
- Structure shared utilities across functions
- Implement auth validation, CORS, error handling
- Connect Edge Functions to Postgres, Storage, Auth APIs
- Design service-based function architecture

## Architecture

### How Edge Functions Work
1. Request enters edge gateway (handles routing, JWT validation)
2. Auth & policies applied (rate limits, security checks)
3. Edge runtime executes function on nearest node
4. Function calls Supabase APIs or third-party services
5. Response returns via gateway with request metadata logged

### File Structure (Service-Based)
```
supabase/functions/
├── _shared/                    # Shared across ALL functions
│   ├── clients/
│   │   └── supabaseAdmin.ts   # Admin client singleton
│   ├── utils/
│   │   ├── auth.ts            # JWT/auth helpers
│   │   ├── responses.ts       # Standard response builders
│   │   ├── logger.ts          # Structured logging
│   │   └── validation.ts      # Input validators
│   ├── services/
│   │   └── notification.ts    # FCM/notification helpers
│   └── config.ts              # Runtime configuration
├── auth_service/
│   └── index.ts               # Auth operations
├── fart_service/
│   └── index.ts               # Core domain logic
├── social_service/
│   └── index.ts               # Friends, blocking
└── cron_service/
    └── index.ts               # Scheduled jobs
```

## Function Template

### Basic Handler
```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req: Request) => {
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const { action, ...params } = await req.json();

    switch (action) {
      case "create":
        return await handleCreate(req, params);
      case "list":
        return await handleList(req, params);
      default:
        return new Response(
          JSON.stringify({ error: "Unknown action" }),
          { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
    }
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
```

### Auth-Validated Handler
```typescript
import { createClient } from "jsr:@supabase/supabase-js@2";

async function getAuthUser(req: Request) {
  const authHeader = req.headers.get("Authorization");
  if (!authHeader) throw new Error("Missing authorization header");

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

### Admin Client (Service Role)
```typescript
import { createClient } from "jsr:@supabase/supabase-js@2";

export const supabaseAdmin = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  { auth: { autoRefreshToken: false, persistSession: false } }
);
```

## Deployment via MCP

```
deploy_edge_function({
  project_id: "your-project-ref",
  name: "my_function",
  entrypoint_path: "index.ts",
  verify_jwt: true,           // ALWAYS true unless custom auth
  files: [
    { name: "index.ts", content: "..." },
    { name: "deno.json", content: "..." }   // include if exists
  ]
})
```

## Debugging

1. **Check logs**: `get_logs(service: "edge-function")` for last 24h
2. **Common errors**:
   - `Boot failure` — syntax error or bad import
   - `Worker exceeded` — function timed out (default 150s wall, 50s CPU for free tier)
   - `413` — request body too large (default 2MB, configurable to 150MB)
3. **Environment variables**: Set in Dashboard > Edge Functions > Secrets
4. **Local testing**: `supabase functions serve my_function --env-file .env.local`

## Best Practices
- One service function can handle multiple actions via `action` parameter routing
- Share code via `_shared/` directory (imported with relative paths)
- Use structured JSON responses: `{ data, error, message }`
- Always handle CORS preflight for browser clients
- Use `SUPABASE_SERVICE_ROLE_KEY` only in server-side functions, never expose to client
- Set `verify_jwt: true` and validate auth in the function body for defense in depth
- Prefer database triggers over Edge Functions for simple counter updates
- For webhooks (Stripe, Apple S2S): disable JWT verification but implement signature validation
