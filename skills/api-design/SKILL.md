---
name: api-design
description: API contract design and review workflow. Use when designing or changing endpoints, request and response schemas, status codes, pagination, filtering, sorting, versioning, rate limits, webhooks, or API error models.
origin: ECC
---

# API Design

Use this skill when a task changes an API surface or external contract.

## What to Apply

- Define resources, methods, request bodies, response shapes, and errors before implementation.
- Use consistent naming, versioning, pagination, filtering, and status code conventions.
- Document validation, authentication, authorization, rate limits, and idempotency.
- Preserve backwards compatibility unless the user explicitly accepts a breaking change.
- Keep contracts boring, predictable, and testable.

## Reference Files

- [ai-agent-standards/prompts/sample-use-cases/create-api-with-rate-limiting.md](../../ai-agent-standards/prompts/sample-use-cases/create-api-with-rate-limiting.md)
- [ai-agent-standards/engineering-practices/DOCUMENTATION_STANDARDS.md](../../ai-agent-standards/engineering-practices/DOCUMENTATION_STANDARDS.md)
- [ai-agent-standards/risk-management/security-constraints.md](../../ai-agent-standards/risk-management/security-constraints.md)

## Output Expectation

Return the proposed contract, compatibility notes, and the tests needed to prove the API behavior.
