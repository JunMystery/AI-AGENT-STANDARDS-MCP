---
name: browser-qa
description: Browser-based verification for UI behavior, visual regressions, and accessibility. Use after a feature is available in a live environment.
origin: ECC
---

# Browser QA

Use this skill to validate UI behavior in a browser rather than only from code.

## Trigger

- Frontend changes
- PRs touching UI flows
- Visual or accessibility verification

## What to Apply

- Smoke test the page.
- Verify interactions and critical flows.
- Check visual regressions at key breakpoints.
- Run accessibility checks where appropriate.

## Reference Files

- [ai-agent-standards/compliance/A11Y_CHECKLIST.md](../../ai-agent-standards/compliance/A11Y_CHECKLIST.md)
- [ai-agent-standards/quality-control/README.md](../../ai-agent-standards/quality-control/README.md)
- [ai-agent-standards/quality-control/ci-cd-gates.md](../../ai-agent-standards/quality-control/ci-cd-gates.md)

## Output Expectation

Report concrete browser-observable issues first, then accessibility or visual findings.