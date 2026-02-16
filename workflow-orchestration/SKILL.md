---
name: "workflow-orchestration"
description: "Use for designing durable workflows with Temporal Python SDK, implementing saga patterns, distributed transactions, and long-running processes. Covers workflow vs activity separation, state management, testing strategies, and production deployment."
---

# Workflow Orchestration (Temporal)

## When to use
- Design durable workflows for distributed systems
- Implement saga patterns and distributed transactions
- Build long-running business processes
- Test workflow logic with time-skipping and mocking

## Temporal patterns
- Workflow vs Activity separation
- Signal and query handlers
- Child workflows and continue-as-new
- Saga pattern with compensating transactions
- Retry policies and timeout configuration

## Testing
- Unit testing with workflow test environments
- Time-skipping for timer-based workflows
- Activity mocking strategies
- Replay testing for determinism verification
- Integration testing with test server

## Best practices
- Keep workflows deterministic
- Use activities for side effects
- Implement proper error handling and compensation
- Version workflows for backward compatibility
