---
name: production-audit
description: Production readiness audit workflow. Use when asked whether an app, feature, release, PR, or deployment is ready to ship, what might break in production, or what blockers remain before launch.
origin: ECC
---

# Production Audit

Use this skill for release-readiness risk review, not as a replacement for formal compliance review.

## What to Apply

- Build the audit from local evidence, CI status, docs, tests, configs, and observable behavior.
- Inspect auth, data, background jobs, external integrations, environment setup, observability, and rollback paths where they exist.
- Separate ship blockers from follow-up risks.
- Do not upload repo contents or run external scanners unless the user explicitly approves.
- Tie each recommendation to a file, command result, deployed behavior, or documented gap.

## Reference Files

- [ai-agent-standards/quality-control/audit-ai-code-full.md](../../ai-agent-standards/quality-control/audit-ai-code-full.md)
- [ai-agent-standards/quality-control/ci-cd-gates.md](../../ai-agent-standards/quality-control/ci-cd-gates.md)
- [ai-agent-standards/engineering-practices/RELEASE_PROCESS.md](../../ai-agent-standards/engineering-practices/RELEASE_PROCESS.md)

## Output Expectation

Return a ship, ship-with-caveats, or block recommendation with the highest-risk findings first.
