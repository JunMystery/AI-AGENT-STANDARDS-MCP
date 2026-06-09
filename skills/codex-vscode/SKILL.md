---
name: codex-vscode
description: Configure and troubleshoot OpenAI Codex in VS Code and VS Code-compatible IDEs. Use when adding Codex project instructions, installing standards for the Codex VS Code extension, explaining Codex instruction discovery, or aligning Codex with this repository's AI-Agent-Standards workflow.
origin: AI-Agent-Standards
---

# Codex VS Code

Use this skill to make OpenAI Codex follow the repository standards when it runs from VS Code, Cursor, Windsurf, or another VS Code-compatible IDE.

## What to Apply

- Prefer `AGENTS.md` as the Codex project instruction file.
- Keep Codex instructions short and link to standards files instead of duplicating the whole framework.
- Put `AGENTS.md` at the project root so Codex can auto-discover it for the workspace.
- For nested workspaces, check for closer `AGENTS.md` files before editing files in subdirectories.
- Keep task-specific guidance on-demand through [SKILL-REFERENCE.md](../../SKILL-REFERENCE.md) and [skills/](../../skills/).
- When installing this framework into another project, copy `AGENTS.md` together with the other root instruction files and rewrite links with `scripts/setup.py`.

## VS Code Notes

- Treat Codex in VS Code as the same coding agent workflow as Codex CLI: it can inspect the repo, edit files, and run checks subject to approvals and sandbox settings.
- Do not use `.instructions.md` for Codex-specific guidance; that file is for VS Code Copilot.
- Use `AGENTS.md` for shared Codex behavior and `PROJECT-STANDARDS.md` for project-local rules that all agents should honor.
- If the user is configuring a VS Code fork, keep the guidance Codex-specific and avoid changing Cursor or Windsurf rules unless the request also affects those tools.

## Reference Files

- [AGENTS.md](../../AGENTS.md)
- [SKILL-REFERENCE.md](../../SKILL-REFERENCE.md)
- [README.md](../../README.md)
- [INSTALL.md](../../INSTALL.md)
- [scripts/setup.py](../../scripts/setup.py)

## Output Expectation

State which instruction file Codex will load, what changed, and how to verify by asking Codex "What coding standards are you following?"
