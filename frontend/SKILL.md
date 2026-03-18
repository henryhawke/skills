---
name: "frontend"
description: "Use for web frontend development including React 19, Next.js 15 (App Router, Server Components), Tailwind CSS, TypeScript, client-side state management (Redux Toolkit, Zustand, React Query), component architecture, performance optimization, and accessibility."
---

# Frontend Development

You build UIs that are fast by default. Server Components for data, Client Components for interaction. You never send JavaScript to the browser that could have been HTML.

## When to use
- Build React/Next.js components, pages, or layouts
- Set up or modify state management
- Optimize Core Web Vitals (LCP, CLS, INP)
- Implement responsive layouts or design systems
- Debug client-side rendering issues

## Next.js 15 App Router Patterns

### Server vs Client Component Decision
```
Does it need useState, useEffect, event handlers, or browser APIs?
  YES → 'use client' (Client Component)
  NO  → Server Component (default, preferred)

Does it fetch data?
  YES → Server Component with async/await (no useEffect, no loading spinners)
  NO  → Either works, prefer Server Component
```

### Data Fetching (Server Component)
```tsx
// app/dashboard/page.tsx — Server Component, NO 'use client'
export default async function DashboardPage() {
  const stats = await getStats();  // runs on server, never shipped to browser
  return <Dashboard stats={stats} />;
}
```

### Interactive Component (Client Component)
```tsx
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### Layout with Suspense
```tsx
// app/layout.tsx
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Suspense fallback={<NavSkeleton />}>
          <Nav />
        </Suspense>
        {children}
      </body>
    </html>
  );
}
```

## State Management Decision Tree

```
Server data (API responses, DB queries)?
  → React Query / SWR (handles caching, revalidation, optimistic updates)

Form state (inputs, validation)?
  → react-hook-form + zod (validation, no re-renders)

Small shared state (theme, sidebar open)?
  → Zustand or Jotai (lightweight, no boilerplate)

Complex app state (many reducers, middleware)?
  → Redux Toolkit (but question if you really need this)

URL state (filters, pagination)?
  → useSearchParams / nuqs (source of truth is the URL)
```

## Tailwind Patterns

### Responsive (Mobile-First)
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

### Dark Mode
```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
```

### Component Variants (CVA)
```tsx
import { cva } from 'class-variance-authority';

const button = cva('rounded-lg font-medium transition-colors', {
  variants: {
    intent: {
      primary: 'bg-blue-600 text-white hover:bg-blue-700',
      secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
      danger: 'bg-red-600 text-white hover:bg-red-700',
    },
    size: {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg',
    },
  },
  defaultVariants: { intent: 'primary', size: 'md' },
});
```

## Performance Checklist
- [ ] Images use `next/image` with proper `width`/`height` or `fill`
- [ ] Fonts use `next/font` (no layout shift)
- [ ] Dynamic imports for heavy components (`next/dynamic`)
- [ ] Memoize expensive computations (`useMemo`, not everything)
- [ ] Virtualize long lists (`@tanstack/react-virtual`)
- [ ] No `useEffect` for data fetching — use Server Components or React Query

## Accessibility Essentials
- Every interactive element is keyboard accessible
- Images have `alt` text (empty `alt=""` for decorative)
- Form inputs have associated `<label>` elements
- Color contrast meets WCAG AA (4.5:1 for text)
- Focus indicators are visible
- Use semantic HTML (`<nav>`, `<main>`, `<article>`) before `role=` attributes

## Anti-Patterns
- `'use client'` on everything — most components don't need it
- `useEffect` for data fetching — use Server Components or React Query
- Prop drilling through 5+ levels — use context or state library
- CSS-in-JS in Server Components — use Tailwind or CSS Modules
- `any` type in TypeScript — defeats the purpose, use proper types
- Re-rendering entire page on small state change — isolate Client Components
