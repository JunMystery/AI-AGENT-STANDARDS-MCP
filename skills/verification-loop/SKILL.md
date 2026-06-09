---
name: verification-loop
description: Post-change verification loop for build, type, lint, test, security, and diff review. Use before PRs or after significant edits.
origin: ECC
---

# Verification Loop

Use this skill after completing a meaningful change or before handing work back.

## Trigger

- After implementation or refactor
- Before creating a PR
- When validating a potentially risky change

## What to Apply

- Run build verification first.
- Run type checks and lint next.
- Run the relevant tests with coverage.
- Check for obvious secret or logging issues.
- Review the diff for unintended edits.

## Reference Files

- [ai-agent-standards/quality-control/README.md](../../ai-agent-standards/quality-control/README.md)
- [ai-agent-standards/quality-control/ci-cd-gates.md](../../ai-agent-standards/quality-control/ci-cd-gates.md)
- [ai-agent-standards/quality-control/self-check-report-template.md](../../ai-agent-standards/quality-control/self-check-report-template.md)

## Output Expectation

Return a compact pass/fail report with blockers first.