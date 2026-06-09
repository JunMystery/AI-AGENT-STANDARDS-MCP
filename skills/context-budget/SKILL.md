---
name: context-budget
description: Token and context budget audit for agents, skills, rules, and MCP overhead. Use when sessions feel bloated or repeated references are wasting context.
origin: ECC
---

# Context Budget

Use this skill to reduce wasted context and identify bloat.

## Trigger

- Session quality degrades as context grows
- More agents, skills, or rules were added recently
- You want to know what should remain on-demand

## What to Apply

- Prefer on-demand load over always-loaded instructions.
- Identify overlapping docs and duplicate guidance.
- Keep root instruction files short.
- Move specialized guidance into task-specific files.

## Reference Files

- [SKILL-REFERENCE.md](../../SKILL-REFERENCE.md)
- [README.md](../../README.md)
- [ai-agent-standards/INDEX.md](../../ai-agent-standards/INDEX.md)

## Output Expectation

Report the biggest token savings first and separate always-loaded from on-demand content.