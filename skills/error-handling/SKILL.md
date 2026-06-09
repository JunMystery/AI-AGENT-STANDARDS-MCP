---
name: error-handling
description: General error-handling design and review workflow. Use when adding or auditing error boundaries, retries, timeouts, validation failures, user-facing messages, logging, fallbacks, circuit breakers, or API error responses.
origin: ECC
---

# Error Handling

Use this skill when failure behavior is part of the work.

## What to Apply

- Make errors explicit at the boundary where they occur.
- Separate user-facing messages from developer diagnostics.
- Never silently swallow failures; handle, log, or propagate them.
- Add retries only for transient failures and include limits, backoff, and timeout behavior.
- Keep error contracts consistent across APIs, jobs, UI flows, and integrations.

## Reference Files

- [ai-agent-standards/reference/error-reference-complete.md](../../ai-agent-standards/reference/error-reference-complete.md)
- [ai-agent-standards/risk-management/security-constraints.md](../../ai-agent-standards/risk-management/security-constraints.md)
- [ai-agent-standards/quality-control/code-review-checklist.md](../../ai-agent-standards/quality-control/code-review-checklist.md)

## Output Expectation

Document what can fail, what the user sees, what gets logged, and how the system recovers.
