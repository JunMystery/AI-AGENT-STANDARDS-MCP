---
name: security-review
description: Security checklist for secrets, input validation, auth, authorization, SQL injection, XSS, and CSRF. Use for sensitive code paths.
origin: ECC
---

# Security Review

Use this skill for anything that could expose data, credentials, or trust boundaries.

## Trigger

- Authentication or authorization changes
- User input handling
- API endpoints
- Secrets or credentials
- Payment or sensitive-data flows

## What to Apply

- Do not hardcode secrets.
- Validate input at the boundary.
- Use parameterized queries or safe ORM methods.
- Enforce auth checks before sensitive operations.
- Sanitize user-controlled HTML.
- Apply CSRF protection where needed.

## Reference Files

- [ai-agent-standards/risk-management/security-constraints.md](../../ai-agent-standards/risk-management/security-constraints.md)
- [ai-agent-standards/risk-management/escalation-workflow.md](../../ai-agent-standards/risk-management/escalation-workflow.md)
- [ai-agent-standards/compliance/COMPLIANCE.md](../../ai-agent-standards/compliance/COMPLIANCE.md)
- [ai-agent-standards/quality-control/audit-ai-code-full.md](../../ai-agent-standards/quality-control/audit-ai-code-full.md)

## Output Expectation

Call out any security-sensitive assumption explicitly and fail closed when the prompt is unclear.