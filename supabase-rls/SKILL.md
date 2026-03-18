---
name: "supabase-rls"
description: "Use for designing and implementing Supabase Row Level Security (RLS) policies. Covers policy patterns for CRUD operations, auth integration, role-based access, multi-tenant isolation, performance optimization, and security auditing with get_advisors."
---

# Supabase Row Level Security (RLS)

## When to use
- Enable or design RLS policies on any public table
- Implement authorization logic at the database level
- Debug "no rows returned" issues (often missing RLS policies)
- Audit security posture after schema changes
- Optimize RLS policy performance
- Implement multi-tenant data isolation

## Core Concepts

### Enable RLS
```sql
-- ALWAYS enable RLS on public tables
ALTER TABLE public.my_table ENABLE ROW LEVEL SECURITY;

-- Force RLS even for table owners (important!)
ALTER TABLE public.my_table FORCE ROW LEVEL SECURITY;
```

### Policy Structure
```sql
CREATE POLICY "policy_name"
  ON public.table_name
  FOR {SELECT | INSERT | UPDATE | DELETE | ALL}
  TO {authenticated | anon | service_role | role_name}
  USING (condition)        -- filter rows (SELECT, UPDATE, DELETE)
  WITH CHECK (condition);  -- validate new/updated rows (INSERT, UPDATE)
```

## Common Policy Patterns

### User Owns Row
```sql
-- Users can only see their own data
CREATE POLICY "users_select_own" ON public.profiles
  FOR SELECT TO authenticated
  USING (auth.uid() = user_id);

-- Users can only update their own data
CREATE POLICY "users_update_own" ON public.profiles
  FOR UPDATE TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Users can only delete their own data
CREATE POLICY "users_delete_own" ON public.profiles
  FOR DELETE TO authenticated
  USING (auth.uid() = user_id);
```

### Insert with Auth
```sql
-- Authenticated users can insert, must set their own user_id
CREATE POLICY "users_insert" ON public.farts
  FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = user_id);
```

### Friends Can See
```sql
-- Users see their own OR friends' data
CREATE POLICY "friends_select" ON public.farts
  FOR SELECT TO authenticated
  USING (
    user_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM public.friendships
      WHERE (user_id = auth.uid() AND friend_id = farts.user_id)
         OR (friend_id = auth.uid() AND user_id = farts.user_id)
    )
  );
```

### Public Read, Auth Write
```sql
-- Anyone can read
CREATE POLICY "public_select" ON public.leaderboard
  FOR SELECT TO anon, authenticated
  USING (true);

-- Only authenticated can write
CREATE POLICY "auth_insert" ON public.leaderboard
  FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = user_id);
```

### Admin/Service Role Bypass
```sql
-- Service role bypasses RLS by default (no policy needed)
-- For custom admin role via JWT claims:
CREATE POLICY "admin_all" ON public.settings
  FOR ALL TO authenticated
  USING (
    (auth.jwt() ->> 'role')::text = 'admin'
  );
```

### Blocked Users
```sql
-- Hide content from blocked users
CREATE POLICY "not_blocked_select" ON public.farts
  FOR SELECT TO authenticated
  USING (
    NOT EXISTS (
      SELECT 1 FROM public.blocks
      WHERE blocker_id = farts.user_id AND blocked_id = auth.uid()
    )
  );
```

## Performance Optimization

### Use Security Definer Functions
```sql
-- Wrap complex permission checks in a function
CREATE OR REPLACE FUNCTION public.is_friend(target_user_id uuid)
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1 FROM friendships
    WHERE (user_id = auth.uid() AND friend_id = target_user_id)
       OR (friend_id = auth.uid() AND user_id = target_user_id)
  );
$$;

-- Use in policy (faster, cached per transaction)
CREATE POLICY "friends_select" ON public.farts
  FOR SELECT TO authenticated
  USING (user_id = auth.uid() OR public.is_friend(user_id));
```

### Index for RLS
```sql
-- Index columns used in RLS policies
CREATE INDEX idx_friendships_lookup
  ON public.friendships (user_id, friend_id);

CREATE INDEX idx_blocks_lookup
  ON public.blocks (blocker_id, blocked_id);
```

## Security Audit Workflow

1. After any DDL change, run: `get_advisors(type: "security")`
2. Check for tables missing RLS:
   ```sql
   SELECT tablename FROM pg_tables
   WHERE schemaname = 'public' AND tablename NOT IN (
     SELECT tablename FROM pg_tables t
     JOIN pg_class c ON c.relname = t.tablename
     WHERE c.relrowsecurity = true
   );
   ```
3. Review existing policies:
   ```sql
   SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual, with_check
   FROM pg_policies WHERE schemaname = 'public';
   ```

## Common Pitfalls
- **Missing RLS** — table returns no rows to client. Enable RLS + add SELECT policy.
- **USING vs WITH CHECK** — `USING` filters existing rows, `WITH CHECK` validates writes. UPDATE needs both.
- **`auth.uid()` returns NULL for anon** — policies using `auth.uid()` silently exclude anonymous users.
- **Service role bypasses RLS** — this is intentional. Use it in Edge Functions for admin operations.
- **Subquery performance** — `EXISTS` is faster than `IN` for RLS subqueries. Always add indexes.
- **`FORCE ROW LEVEL SECURITY`** — without this, table owners bypass RLS. Always set it.
