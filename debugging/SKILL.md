---
name: "debugging"
description: "Use when debugging errors, test failures, unexpected behavior, analyzing logs, stack traces, or investigating production errors. Covers systematic debugging, log correlation, distributed tracing, and root cause analysis."
---

# Debugging & Error Analysis

## When to use
- Debug errors, exceptions, and test failures
- Analyze log files and stack traces
- Investigate production incidents
- Correlate errors across distributed systems
- Find root causes of unexpected behavior

## Workflow
1. Reproduce the error and gather context
2. Read error messages and stack traces carefully
3. Search for error patterns in logs and code
4. Correlate across systems if distributed
5. Form hypothesis and test with targeted investigation
6. Identify root cause and implement fix
7. Add tests to prevent regression

## Techniques
- Binary search / git bisect for regression finding
- Log correlation across services
- Distributed tracing analysis
- Memory profiling for leaks
- Network debugging for connectivity issues
- Database query analysis for performance issues
