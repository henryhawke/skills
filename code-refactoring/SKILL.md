---
name: "code-refactoring"
description: "Use when the user wants to refactor code, modernize legacy codebases, migrate frameworks, reduce technical debt, or update dependencies. Handles backward compatibility and gradual modernization strategies."
---

# Code Refactoring & Legacy Modernization

## When to use
- Refactor code for better maintainability
- Modernize legacy codebases and frameworks
- Migrate between framework versions
- Reduce technical debt
- Update outdated dependencies

## Workflow
1. Analyze current codebase structure and patterns
2. Identify technical debt and modernization opportunities
3. Plan incremental refactoring steps
4. Implement changes while maintaining backward compatibility
5. Verify no regressions with existing tests
6. Update tests for refactored code

## Principles
- Incremental changes over big-bang rewrites
- Maintain backward compatibility during migration
- Preserve existing test coverage
- Follow the strangler fig pattern for legacy systems
- Keep refactoring commits separate from feature commits
