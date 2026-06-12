# Usage Guide

[Back to README](../README.md)

Use this MCP server to give AI agents standards guidance, skill references, workflow prompts, and bounded access to project code context.

## Verify With MCP Inspector

After installation, launch the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector .venv/bin/python -m ai_agent_standards_mcp
```

Open the printed URL, usually `http://localhost:5173`, and inspect the registered tools, prompts, and resources.

## Recommended Agent Workflow

At the start of a coding session:

1. Call `recommend_context(task)` to load relevant standards and skills.
2. Call `get_project_tree(project_path, max_depth=3)` to understand the repository shape.
3. For large refactors, upgrades, audits, or unfamiliar code, also use `search_project_code(project_path, query)` and `export_project_snapshot(project_path)` when a reusable overview is useful.
4. Before editing any file, inspect the current target file with `read_project_file(project_path, relative_path)` or an equivalent file-read tool.
5. Run the smallest relevant verification command after changes.

Avoid repeated broad scans during the same session unless the project changed significantly.

## Example: Standards Context

```json
{
  "task": "Build a secure API endpoint with tests",
  "limit": 6
}
```

Use the returned paths and recommendations before making implementation decisions.

## Example: Project Code Context

Inspect project structure:

```json
{
  "project_path": "/absolute/path/to/project",
  "max_depth": 3
}
```

Search for a feature or symbol:

```json
{
  "project_path": "/absolute/path/to/project",
  "query": "refresh token auth",
  "limit": 10
}
```

Read the current source file before editing:

```json
{
  "project_path": "/absolute/path/to/project",
  "relative_path": "src/auth/token_service.py",
  "start_line": 1,
  "max_lines": 160
}
```

## Example: Workflow Prompt

Use prompt commands such as `/plan`, `/code`, `/test`, or `/debug` when the client exposes MCP prompts as slash commands.

For example, `/plan` loads the planning workflow capsule and appends the task the user provided.

## Token Guidance

Prefer narrow calls:

- Use `max_depth=3` or `max_depth=4` for initial tree scans.
- Use `limit=10` or `limit=20` for search.
- Use `max_lines=120` to `200` for file reads unless a broader range is necessary.
- Avoid exporting full snapshots for small one-file tasks.

See [Project Context Tools](project-context-tools.md) for details on snapshot freshness and token cost.

## Related Docs

- [MCP Surface Reference](mcp-surface.md)
- [Project Context Tools](project-context-tools.md)
- [Development Guide](development.md)
