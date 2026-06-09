# Repo Map For Agents

Use this map before changing the repository. Prefer the smallest relevant source file and avoid broad documentation moves unless explicitly requested.

## Root Instruction Files

- `AGENTS.md`: OpenAI Codex and Codex VS Code instructions.
- `CLAUDE.md`: Claude Code instructions.
- `GEMINI.md`: Gemini Code Assist and Gemini CLI instructions.
- `COPILOT.md`: GitHub Copilot Chat instructions.
- `.instructions.md`: VS Code Copilot instructions.
- `.cursorrules`: Windsurf and legacy Cursor fallback.
- `.cursor/rules/karpathy-guidelines.mdc`: Cursor rule file with frontmatter.

These files are generated. Edit `karpathy/principles.md`, `rules/agent-manifest.json`, or `rules/templates/`, then run `python scripts/generate-rules.py`.

## Core Sources

- `karpathy/`: source of truth for the 6 Core Principles and examples.
- `rules/`: manifest and templates used to generate agent instruction files.
- `scripts/`: setup, security audit, and rules generation automation.
- `skills/`: on-demand workflow capsules. Do not treat the full directory as always-loaded context.
- `ai-agent-standards/`: framework documentation, standards, checklists, prompts, risk guidance, compliance, and multi-agent docs.
- `docs/`: maintainer-facing docs for repo structure and rules generation.
- `.github/`: PR template and CI workflows.

## Common Workflows

- Updating core behavior: edit `karpathy/principles.md`, regenerate rules, run generator check.
- Adding or changing an agent instruction file: update `rules/agent-manifest.json` and a template, regenerate, then verify setup still lists the agent.
- Updating task-specific standards: edit the relevant file under `ai-agent-standards/`.
- Updating a skill: edit only the matching `skills/<name>/SKILL.md`.
- Refactoring large files or reducing monolithic modules: load `skills/large-file-refactor/SKILL.md`.

## Verification

Use the narrowest checks that prove the change:

```bash
python scripts/generate-rules.py --check
python -m unittest discover
git diff --check
```
