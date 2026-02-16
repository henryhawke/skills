---
name: "testing"
description: "Use when the user needs test automation, TDD implementation, test strategy design, or quality assurance. Covers unit tests, integration tests, e2e tests with Playwright/Cypress, self-healing tests, and CI/CD integration."
---

# Test Automation & TDD

## When to use
- Write unit, integration, or e2e tests
- Implement test-driven development (red-green-refactor)
- Design testing strategies and test architectures
- Set up test automation in CI/CD pipelines
- Create self-healing tests

## Workflow
1. Analyze code to identify testable units and boundaries
2. Choose appropriate testing framework for the stack
3. Write tests following AAA pattern (Arrange, Act, Assert)
4. For TDD: write failing test first, implement, refactor
5. Ensure tests are deterministic and independent
6. Add tests to CI/CD pipeline

## Frameworks
- JavaScript/TypeScript: Jest, Vitest, Testing Library, Playwright, Cypress
- Python: pytest, unittest, hypothesis
- Go: testing, testify
- Rust: built-in test framework, proptest

## Best practices
- Test behavior, not implementation
- Use descriptive test names
- Minimize test dependencies and shared state
- Mock external services at boundaries
- Maintain fast test execution
