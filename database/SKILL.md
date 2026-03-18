---
name: "database"
description: "Use for PostgreSQL schema design, query optimization, indexing strategies (B-tree/GIN/GiST/BRIN), EXPLAIN analysis, N+1 resolution, materialized views, partitioning, PostGIS spatial queries, triggers, pg_cron, and database migration planning. Covers Supabase-specific patterns including RLS and cost optimization."
---

# Database Architecture & Optimization

You are a database performance expert. You measure everything, guess nothing, and always check EXPLAIN before declaring something "optimized."

## When to use
- Design or modify database schemas
- Optimize slow queries (always start with EXPLAIN ANALYZE)
- Choose index types for specific query patterns
- Detect and fix N+1 query problems
- Plan zero-downtime migrations
- Set up materialized views, triggers, or pg_cron jobs
- Work with PostGIS spatial data

## Query Optimization Workflow

### 1. Always Start Here
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) <your query>;
```

### 2. Read the Plan
- **Seq Scan on large table** → missing index
- **Nested Loop with high row count** → N+1 or missing join index
- **Sort with high cost** → add index on ORDER BY columns
- **Hash Join with large build side** → check join conditions
- **Buffers: shared read** → data not in cache, might need to warm

### 3. Index Selection Guide
| Query Pattern | Index Type | Example |
|---|---|---|
| `WHERE col = value` | B-tree (default) | `CREATE INDEX ON t(col)` |
| `WHERE col IN (...)` | B-tree | Same as equality |
| `WHERE col LIKE 'prefix%'` | B-tree with `text_pattern_ops` | `CREATE INDEX ON t(col text_pattern_ops)` |
| `WHERE col @> '{"key": "val"}'` | GIN | `CREATE INDEX ON t USING GIN(col)` |
| Full-text search | GIN on `tsvector` | `CREATE INDEX ON t USING GIN(to_tsvector('english', col))` |
| `WHERE ST_DWithin(geom, ...)` | GiST | `CREATE INDEX ON t USING GIST(geom)` |
| `WHERE timestamp > now() - '1 day'` on huge table | BRIN | `CREATE INDEX ON t USING BRIN(timestamp)` |
| `WHERE a = X AND b = Y` | Composite B-tree | `CREATE INDEX ON t(a, b)` — column order matters! |
| `WHERE a = X ORDER BY b` | Composite B-tree | `CREATE INDEX ON t(a, b)` |

### 4. Covering Index (Index-Only Scan)
```sql
-- Include columns to avoid table heap lookup
CREATE INDEX idx_farts_user_created ON farts(user_id, created_at DESC)
  INCLUDE (content, reaction_count);
```

## N+1 Detection & Resolution

### Symptoms
- Application makes N+1 queries for a list of N items
- Each item triggers a separate query for related data
- Response time scales linearly with result count

### Fix Patterns
```sql
-- BAD: N+1 (one query per fart to get user)
SELECT * FROM farts WHERE ...;  -- then for each:
SELECT * FROM users WHERE id = $1;

-- GOOD: Single join
SELECT f.*, u.username, u.avatar_url
FROM farts f
JOIN users u ON u.id = f.user_id
WHERE ...;

-- GOOD: Batch with IN clause (when join is awkward)
SELECT * FROM users WHERE id = ANY($1::uuid[]);
```

## Cost-Optimized Patterns (Supabase)

### Database Triggers > Edge Functions
```sql
-- Auto-increment counter (FREE, instant, no Edge Function call)
CREATE OR REPLACE FUNCTION handle_count_change()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE parent_table SET child_count = child_count + 1 WHERE id = NEW.parent_id;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE parent_table SET child_count = child_count - 1 WHERE id = OLD.parent_id;
  END IF;
  RETURN COALESCE(NEW, OLD);
END; $$;
```

### Materialized Views > Computed Queries
```sql
-- Leaderboard: compute once per hour, not per request
CREATE MATERIALIZED VIEW mv_leaderboard AS
SELECT user_id, username, COUNT(*) as total, RANK() OVER (ORDER BY COUNT(*) DESC) as rank
FROM farts GROUP BY user_id, username;

-- Unique index enables CONCURRENTLY refresh
CREATE UNIQUE INDEX ON mv_leaderboard(user_id);

-- pg_cron: refresh hourly
SELECT cron.schedule('refresh-lb', '0 * * * *',
  $$REFRESH MATERIALIZED VIEW CONCURRENTLY mv_leaderboard$$);
```

### Batch Notifications > Individual Sends
```sql
-- Queue notifications in a table, batch-process every 5 min
INSERT INTO notification_queue (user_id, type, payload) VALUES (...);
-- pg_cron calls Edge Function to process batch
```

## PostGIS Spatial Patterns
```sql
-- Nearby query (uses spatial index)
SELECT *, ST_Distance(location, ST_SetSRID(ST_MakePoint($lng, $lat), 4326)::geography) as distance
FROM farts
WHERE ST_DWithin(location, ST_SetSRID(ST_MakePoint($lng, $lat), 4326)::geography, $radius_meters)
ORDER BY distance
LIMIT 50;
```

## Migration Safety Rules
1. `ALTER TABLE ADD COLUMN` (nullable) — safe, instant
2. `ALTER TABLE ADD COLUMN ... DEFAULT` — safe on Postgres 11+
3. `ALTER TABLE DROP COLUMN` — safe but irreversible, verify no code references
4. `CREATE INDEX CONCURRENTLY` — safe, non-blocking
5. `ALTER TABLE ALTER COLUMN TYPE` — DANGEROUS, rewrites table, takes lock
6. Rename column — NEVER in production. Add new, migrate data, update code, drop old.

## Anti-Patterns
- `SELECT *` in production queries — select only needed columns
- Missing `LIMIT` on unbounded queries — always paginate
- Indexing every column — indexes slow writes, only index what you query
- Using `OFFSET` for pagination on large datasets — use keyset pagination instead
- Storing computed values that can be derived — use generated columns or views
- Running DDL without `IF NOT EXISTS` / `IF EXISTS` — breaks idempotency
