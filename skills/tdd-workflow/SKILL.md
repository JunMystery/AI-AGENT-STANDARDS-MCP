---
name: tdd-workflow
description: Test-first workflow for features, bug fixes, and refactors. Enforces unit, integration, and E2E coverage with a RED-GREEN-REFACTOR loop.
origin: ECC
---

# TDD Workflow

Use this skill when implementation should be driven by tests.

## Trigger

- New feature work
- Bug fixes
- Refactors that change behavior
- Test generation or test coverage work

## What to Apply

- Write the test before production code.
- Confirm the test fails for the right reason.
- Implement the minimum code to make it pass.
- Refactor only after the test is green.
- Keep the test pyramid balanced.

## Reference Files

- [ai-agent-standards/engineering-practices/TESTING_STANDARDS.md](../../ai-agent-standards/engineering-practices/TESTING_STANDARDS.md)
- [ai-agent-standards/quality-control/self-check-report-template.md](../../ai-agent-standards/quality-control/self-check-report-template.md)
- [ai-agent-standards/quality-control/code-review-checklist.md](../../ai-agent-standards/quality-control/code-review-checklist.md)

## Output Expectation

State the current TDD phase and the next verification step before changing production code.