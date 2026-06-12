# Installation

[Back to README](../README.md)

This project runs as a Python MCP server over Stdio transport. It requires Python 3.10 or newer.

## Automatic Install

Use the bundled installer when setting up the server for local MCP clients:

```bash
python3 scripts/install-mcp.py        # Linux / macOS
python  scripts/install-mcp.py        # Windows
```

The installer creates a local `.venv`, installs the package in editable mode, and attempts to configure supported MCP clients.

## Manual Install

Create a virtual environment and install the package locally:

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"      # Linux / macOS
.venv\Scripts\pip install -e ".[dev]"  # Windows
```

For runtime-only usage, the project depends on `mcp>=1.0.0`. The `dev` extra adds test dependencies such as `pytest`.

## Run The Server

After installation, run the MCP server with:

```bash
agent-guidance-mcp
.venv/bin/python -m ai_agent_standards_mcp      # Linux / macOS
.venv\Scripts\python.exe -m ai_agent_standards_mcp  # Windows
```

The server uses Stdio transport, so it is normally launched by an MCP client rather than directly by a human-operated terminal.

## Standards Corpus Root

By default, the package discovers the bundled standards corpus. To point the server to a different standards folder, set:

```bash
AI_AGENT_STANDARDS_ROOT=/path/to/AI-Agent-Standards
```

The target folder must contain:

- `karpathy/principles.md`
- `SKILL-REFERENCE.md`
- `ai-agent-standards/INDEX.md`

## Related Docs

- [Client Configuration](client-configuration.md)
- [Usage Guide](usage.md)
- [Development Guide](development.md)
