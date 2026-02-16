---
name: "code-review"
description: "Use when the user asks for a code review, architecture review, or quality analysis of code changes. Covers security vulnerabilities, performance optimization, production reliability, static analysis, and architectural integrity including clean architecture, microservices, event-driven systems, and DDD."
---

# Code Review

## When to use
- Review code changes for quality, security, and performance
- Analyze architectural decisions and design patterns
- Check for OWASP top 10 vulnerabilities
- Review system designs for scalability and maintainability

## Workflow
1. Read and understand the code changes in context
2. Check for security vulnerabilities (injection, XSS, auth issues)
3. Analyze performance implications
4. Review architectural patterns and consistency
5. Check error handling and edge cases
6. Verify test coverage adequacy
7. Provide actionable, prioritized feedback

## Review checklist
- Security: Input validation, auth, secrets exposure, injection
- Performance: N+1 queries, unnecessary allocations, caching opportunities
- Architecture: SOLID principles, separation of concerns, dependency direction
- Reliability: Error handling, retries, circuit breakers, graceful degradation
- Maintainability: Naming, complexity, documentation, test coverage
