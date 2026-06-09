---
name: coding-standards
description: Baseline coding conventions for readability, naming, immutability, KISS, DRY, and code-quality review. Use when starting or reviewing implementation work.
origin: ECC
---

# Coding Standards

Use this skill when you need the baseline floor for code quality across projects.

## Trigger

- Writing or reviewing general-purpose code
- Enforcing naming, readability, or structural consistency
- Checking for unnecessary complexity or duplication

## What to Apply

- Prefer clear names over clever names.
- Keep the smallest solution that satisfies the request.
- Avoid speculative abstractions.
- Keep logic DRY, but do not over-abstract single-use code.
- Favor immutable updates when practical.

## Reference Files

- [karpathy/principles.md](../../karpathy/principles.md)
- [karpathy/examples.md](../../karpathy/examples.md)
- [ai-agent-standards/quality-control/code-review-checklist.md](../../ai-agent-standards/quality-control/code-review-checklist.md)
- [ai-agent-standards/quality-control/audit-ai-code-full.md](../../ai-agent-standards/quality-control/audit-ai-code-full.md)

## Output Expectation

When this skill is active, explain the coding convention being applied only if it affects the implementation choice or review outcome.