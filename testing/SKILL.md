---
name: "testing"
description: "Use for test strategy design, writing unit/integration/e2e tests, TDD workflows, test debugging, and CI/CD test integration. Covers Flutter testing (widget tests, golden tests, integration tests), Bun test runner, pytest, Jest/Vitest, and Playwright. Includes framework-specific patterns and test debugging."
---

# Testing & Quality Assurance

You write tests that catch real bugs, not tests that verify the obvious. Every test should justify its existence by protecting against a specific failure mode.

## When to use
- Write tests for new or modified code
- Debug failing tests
- Design test strategy for a feature
- Set up test infrastructure or CI/CD integration
- Decide what level of testing is appropriate

## Test Level Decision Framework

```
Is it pure logic with no dependencies?  → Unit test
Does it cross service/layer boundaries? → Integration test
Is it a critical user journey?          → E2E test
Is it a visual component?              → Widget test (Flutter) / Component test (React)
Is it an API endpoint?                 → Integration test with real DB
Would a mock hide a real bug here?     → Integration test (don't mock)
```

## Flutter Testing

### Unit Test
```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('FartScoring', () {
    test('calculates score from reactions and distance', () {
      final score = calculateScore(reactions: 5, distanceMeters: 100);
      expect(score, greaterThan(0));
      expect(score, lessThan(1000));
    });

    test('returns zero for no reactions', () {
      expect(calculateScore(reactions: 0, distanceMeters: 50), equals(0));
    });
  });
}
```

### Widget Test
```dart
testWidgets('FartCard shows reaction count', (tester) async {
  await tester.pumpWidget(
    ProviderScope(
      overrides: [fartProvider.overrideWith((ref) => mockFart)],
      child: const MaterialApp(home: FartCard()),
    ),
  );

  expect(find.text('5 reactions'), findsOneWidget);
  await tester.tap(find.byIcon(LucideIcons.heart));
  await tester.pump();
  expect(find.text('6 reactions'), findsOneWidget);
});
```

### Integration Test
```dart
// test/integration/fart_creation_test.dart
void main() {
  testWidgets('user can create and see a fart', (tester) async {
    await tester.pumpWidget(const MyApp());
    await tester.pumpAndSettle();

    await tester.tap(find.byType(FartButton));
    await tester.pumpAndSettle();

    expect(find.byType(FartDetailScreen), findsOneWidget);
  });
}
```

### Run Flutter Tests
```bash
flutter test                                    # All tests
flutter test test/unit/                         # Unit only
flutter test --coverage                         # With coverage
flutter test test/widget/fart_card_test.dart    # Specific file
```

## Bun Testing (Backend)

**CRITICAL: Bun is NOT Jest. Different APIs.**

```typescript
import { describe, test, expect, mock, beforeEach } from "bun:test";

describe("create_fart edge function", () => {
  test("returns 401 without auth", async () => {
    const res = await fetch(`${BASE_URL}/create_fart`, {
      method: "POST",
      body: JSON.stringify({ content: "test" }),
    });
    expect(res.status).toBe(401);
  }, { timeout: 15000 });  // Bun: options object, NOT positional arg

  test("creates fart with valid auth", async () => {
    const res = await fetch(`${BASE_URL}/create_fart`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify({ content: "test", lat: 37.7, lng: -122.4 }),
    });
    expect(res.status).toBe(200);
    const data = await res.json();
    expect(data.id).toBeDefined();
  });
});
```

### Bun vs Jest Gotchas
| Pattern | Jest | Bun |
|---|---|---|
| Mock function | `jest.fn()` | `mock(() => value)` from `bun:test` |
| Test timeout | `test("name", fn, 15000)` | `test("name", fn, { timeout: 15000 })` |
| Module mock | `jest.mock("module")` | `mock.module("module", () => ...)` |
| Spy | `jest.spyOn(obj, "method")` | `const spy = mock(() => ...)` |

### Run Bun Tests
```bash
cd tools
bun run test:integration          # All integration tests
bun test test/integration/auth.test.ts  # Specific file
```

## Test Debugging

### Test Fails Intermittently (Flaky)
1. Check for shared state between tests (missing cleanup)
2. Check for timing dependencies (race conditions, missing `await`)
3. Check for order dependencies (`beforeEach` not resetting state)
4. Check for external service flakiness (use mock/stub)

### Test Passes Locally, Fails in CI
1. Check for environment differences (env vars, file paths)
2. Check for timezone-dependent assertions
3. Check for port conflicts (hardcoded ports)
4. Check test isolation (parallel test runners sharing state)

## What NOT to Test
- Framework internals (Flutter's `setState` works — you don't need to test it)
- Trivial getters/setters with no logic
- Third-party library behavior (test YOUR integration, not THEIR code)
- Implementation details that could change without affecting behavior
- Generated code (`.g.dart`, `.freezed.dart`)

## What to ALWAYS Test
- Business logic with branching conditions
- Data transformations (JSON parsing, model mapping)
- Edge cases: null, empty, boundary values, negative numbers
- Error paths: what happens when the API returns 500?
- Security boundaries: auth checks, permission validation
