# Client Configuration

[Back to README](../README.md)

This server is designed for MCP clients that launch tools over Stdio. Configure clients to run the package module from the repository virtual environment.

## VS Code And GitHub Copilot

The repository includes a workspace MCP settings file under `.vscode/mcp.json`.

When you open this repository in VS Code with GitHub Copilot installed:

1. Run the installer to create `.venv`.
2. Open the repository folder in VS Code.
3. Let VS Code detect the MCP server from `.vscode/mcp.json`.
4. Trust the server when prompted.
5. Use the tools and prompts from Copilot Chat.

By default, `.vscode/mcp.json` points to the Linux/macOS Python path:

```json
"command": "${workspaceFolder}/.venv/bin/python"
```

On Windows, change it to:

```json
"command": "${workspaceFolder}/.venv/Scripts/python.exe"
```

## Generic MCP Client Config

Use this structure for Claude Desktop, Cursor, and other MCP-compatible clients.

Linux/macOS:

```json
{
  "mcpServers": {
    "agent-guidance-mcp": {
      "command": "/absolute/path/to/repo/.venv/bin/python",
      "args": ["-m", "ai_agent_standards_mcp"],
      "env": { "PYTHONPATH": "/absolute/path/to/repo/src" }
    }
  }
}
```

Windows:

```json
{
  "mcpServers": {
    "agent-guidance-mcp": {
      "command": "C:\\absolute\\path\\to\\repo\\.venv\\Scripts\\python.exe",
      "args": ["-m", "ai_agent_standards_mcp"],
      "env": { "PYTHONPATH": "C:\\absolute\\path\\to\\repo\\src" }
    }
  }
}
```

## Client Notes

- Claude Desktop typically uses a global MCP config file.
- Cursor can use a native MCP config or extension-specific MCP settings.
- Gemini-compatible tools can use a JSON MCP config under the user's Gemini configuration directory.
- Codex can use an MCP server entry in `~/.codex/config.toml`.

The bundled `scripts/install-mcp.py` attempts to configure several common clients automatically.

## Environment Variables

Use `AI_AGENT_STANDARDS_ROOT` only when the standards corpus is outside this repository:

```bash
AI_AGENT_STANDARDS_ROOT=/path/to/AI-Agent-Standards
```

Project-context tools should receive an explicit `project_path` argument. Avoid relying on the MCP process current working directory when scanning a user project.

## Related Docs

- [Installation](installation.md)
- [Usage Guide](usage.md)
- [MCP Surface Reference](mcp-surface.md)
