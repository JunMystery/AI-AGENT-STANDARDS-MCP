---
name: prompt-optimizer
description: Prompt analysis and optimization workflow for turning rough requests into clearer task prompts. Use when the user asks to improve or rewrite a prompt.
origin: ECC
---

# Prompt Optimizer

Use this skill when the request is about improving a prompt rather than executing the task directly.

## Trigger

- User asks to rewrite or improve a prompt
- User asks how to ask the model for a task
- Prompt quality feels ambiguous or underspecified

## What to Apply

- Extract intent, scope, constraints, and missing context.
- Reframe the prompt into a clear task structure.
- Recommend task-specific references when useful.

## Reference Files

- [ai-agent-standards/prompts/PROMPT-TEMPLATE.md](../../ai-agent-standards/prompts/PROMPT-TEMPLATE.md)
- [ai-agent-standards/prompts/indexed-by-category.md](../../ai-agent-standards/prompts/indexed-by-category.md)
- [README.md](../../README.md)

## Output Expectation

Return a ready-to-paste prompt and note any missing context that still matters.