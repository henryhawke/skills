---
name: "supabase-migrations"
description: "Use for Supabase database migrations including schema changes, triggers, functions, indexes, RLS policies, pg_cron jobs, and PostGIS spatial setup. Covers the apply_migration MCP tool, zero-downtime strategies, and migration best practices."
---

# Supabase Database Migrations

## When to use
- Create or alter tables, columns, indexes
- Add or modify database triggers and functions
- Set up pg_cron scheduled jobs
- Configure PostGIS spatial extensions
- Apply RLS policies via migration
- Plan zero-downtime schema changes
- Review migration history

## MCP Tools

### Apply Migration
```
apply_migration({
  project_id: "your-ref",
  name: "add_reactions_table",    // snake_case, descriptive
  query: "CREATE TABLE ..."
})
```

### List Migrations
```
list_migrations({ project_id: "your-ref" })
```

### Branching for Safe Testing
```
create_branch({ project_id: "your-ref", name: "feature-reactions" })
// Apply migration to branch first
apply_migration({ project_id: "branch-ref", ... })
// Test, then merge
merge_branch({ branch_id: "branch-id" })
```

## Migration Patterns

### Create Table
```sql
CREATE TABLE IF NOT EXISTS public.reactions (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  fart_id uuid NOT NULL REFERENCES public.farts(id) ON DELETE CASCADE,
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  reaction_type text NOT NULL CHECK (reaction_type IN ('laugh', 'love', 'surprise', 'disgust')),
  created_at timestamptz DEFAULT now() NOT NULL,
  UNIQUE (fart_id, user_id, reaction_type)
);

-- Always enable RLS
ALTER TABLE public.reactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reactions FORCE ROW LEVEL SECURITY;

-- Indexes for common queries
CREATE INDEX idx_reactions_fart_id ON public.reactions(fart_id);
CREATE INDEX idx_reactions_user_id ON public.reactions(user_id);

-- RLS policies
CREATE POLICY "users_select_reactions" ON public.reactions
  FOR SELECT TO authenticated USING (true);
CREATE POLICY "users_insert_reactions" ON public.reactions
  FOR INSERT TO authenticated WITH CHECK (auth.uid() = user_id);
CREATE POLICY "users_delete_own_reactions" ON public.reactions
  FOR DELETE TO authenticated USING (auth.uid() = user_id);
```

### Database Trigger (Counter Pattern)
```sql
-- Function: auto-increment counter on parent table
CREATE OR REPLACE FUNCTION public.handle_reaction_count()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE farts SET reaction_count = reaction_count + 1 WHERE id = NEW.fart_id;
    RETURN NEW;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE farts SET reaction_count = reaction_count - 1 WHERE id = OLD.fart_id;
    RETURN OLD;
  END IF;
END;
$$;

-- Trigger
CREATE TRIGGER trigger_on_reaction_change
  AFTER INSERT OR DELETE ON public.reactions
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_reaction_count();
```

### Materialized View (Leaderboard)
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS public.mv_leaderboard AS
SELECT
  u.id AS user_id,
  u.username,
  u.avatar_url,
  COUNT(f.id) AS total_farts,
  COALESCE(SUM(f.reaction_count), 0) AS total_reactions,
  RANK() OVER (ORDER BY COUNT(f.id) DESC) AS rank
FROM auth.users u
LEFT JOIN public.farts f ON f.user_id = u.id
GROUP BY u.id, u.username, u.avatar_url;

CREATE UNIQUE INDEX idx_mv_leaderboard_user ON public.mv_leaderboard(user_id);

-- Refresh via pg_cron (hourly)
SELECT cron.schedule(
  'refresh-leaderboard',
  '0 * * * *',
  $$REFRESH MATERIALIZED VIEW CONCURRENTLY public.mv_leaderboard$$
);
```

### pg_cron Job
```sql
-- Enable extension first
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Schedule: process notification batch every 5 minutes
SELECT cron.schedule(
  'process-notifications',
  '*/5 * * * *',
  $$SELECT net.http_post(
    url := current_setting('app.settings.supabase_url') || '/functions/v1/process_notification_batch',
    headers := jsonb_build_object(
      'Authorization', 'Bearer ' || current_setting('app.settings.service_role_key'),
      'Content-Type', 'application/json'
    ),
    body := '{}'::jsonb
  )$$
);

-- List scheduled jobs
SELECT * FROM cron.job;

-- Unschedule
SELECT cron.unschedule('process-notifications');
```

### PostGIS Setup
```sql
CREATE EXTENSION IF NOT EXISTS postgis;

-- Add geometry column
ALTER TABLE public.farts ADD COLUMN IF NOT EXISTS
  location geography(Point, 4326);

-- Spatial index (critical for performance)
CREATE INDEX idx_farts_location ON public.farts USING GIST (location);

-- Nearby query function
CREATE OR REPLACE FUNCTION public.get_nearby_farts(
  lat double precision,
  lng double precision,
  radius_meters integer DEFAULT 5000
)
RETURNS SETOF public.farts
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT *
  FROM farts
  WHERE ST_DWithin(
    location,
    ST_SetSRID(ST_MakePoint(lng, lat), 4326)::geography,
    radius_meters
  )
  ORDER BY location <-> ST_SetSRID(ST_MakePoint(lng, lat), 4326)::geography
  LIMIT 50;
$$;
```

## Zero-Downtime Strategies

### Add Column (Safe)
```sql
-- Adding a nullable column is instant, no table rewrite
ALTER TABLE public.farts ADD COLUMN IF NOT EXISTS audio_url text;
```

### Add NOT NULL Column (Safe)
```sql
-- Step 1: Add nullable
ALTER TABLE public.farts ADD COLUMN IF NOT EXISTS visibility text DEFAULT 'public';
-- Step 2: Backfill
UPDATE public.farts SET visibility = 'public' WHERE visibility IS NULL;
-- Step 3: Add constraint
ALTER TABLE public.farts ALTER COLUMN visibility SET NOT NULL;
```

### Rename Column (Dangerous — Avoid)
```sql
-- DON'T rename in production. Instead:
-- 1. Add new column
-- 2. Backfill data
-- 3. Update application code
-- 4. Drop old column in a later migration
```

### Create Index Concurrently
```sql
-- Won't lock the table during creation
CREATE INDEX CONCURRENTLY idx_farts_created
  ON public.farts(created_at DESC);
```

## Best Practices
- Use `IF NOT EXISTS` / `IF EXISTS` for idempotent migrations
- Never hardcode generated IDs (UUIDs) in migrations
- Test migrations on a branch before applying to production
- One logical change per migration file
- Name migrations descriptively: `add_reactions_table`, `create_leaderboard_view`
- Always add RLS + indexes in the same migration as the table creation
- Use `CONCURRENTLY` for index creation on large tables
- Use `SECURITY DEFINER` + `SET search_path` on functions that bypass RLS
