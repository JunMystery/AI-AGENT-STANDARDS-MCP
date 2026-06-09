---
name: skill-stocktake
description: Local skill quality audit workflow. Use when reviewing, pruning, expanding, or validating skills for trigger clarity, duplication, context cost, stale references, missing frontmatter, or weak on-demand behavior.
origin: ECC
---

# Skill Stocktake

Use this skill when maintaining the `skills/` directory.

## What to Apply

- Inventory skill names, descriptions, origins, and reference links.
- Check that descriptions carry the trigger conditions because bodies load only on demand.
- Detect duplicate or overlapping skills and prefer the smaller set.
- Verify references exist and point to stable repo standards.
- Keep skill bodies concise and task-oriented.

## Reference Files

- [SKILL-REFERENCE.md](../../SKILL-REFERENCE.md)
- [skills/README.md](../README.md)
- [ai-agent-standards/INDEX.md](../../ai-agent-standards/INDEX.md)

## Output Expectation

Return findings first, then a minimal edit plan for skill quality or coverage gaps.
