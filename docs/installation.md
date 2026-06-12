# Installation

[Back to README](../README.md)

This project runs as a Python MCP server over Stdio transport. It requires Python 3.10 or newer.

## Automatic Install

Use the bundled installer when setting up the server for local MCP clients:

```bash
python3 scripts/install-mcp.py        # Linux / macOS
python  scripts/install-mcp.py        # Windows
```

The installer creates a local `.venv`, installs the package in editable mode,
and attempts to configure supported MCP clients. It is safe to re-run after
pulling repo updates: owned MCP server blocks are refreshed in place, legacy
`ai-agent-standards-mcp` blocks are migrated when recognized, unrelated servers
are preserved, and existing config files are backed up before changes.

Useful installer options:

```bash
python scripts/install-mcp.py --dry-run       # preview config changes only
python scripts/install-mcp.py --skip-install  # refresh configs without pip install
python scripts/install-mcp.py --no-backup     # do not create .bak timestamp files
```

After config updates, the installer runs a startup smoke check with
`python -m agent_guidance_mcp --show-stats`.

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
.venv/bin/python -m agent_guidance_mcp      # Linux / macOS
.venv\Scripts\python.exe -m agent_guidance_mcp  # Windows
```

The server uses Stdio transport, so it is normally launched by an MCP client rather than directly by a human-operated terminal.

## Standards Corpus Root

By default, the package discovers the bundled standards corpus. To point the server to a different standards folder, set:

```bash
AGENT_GUIDANCE_ROOT=/path/to/Agent-Guidance
```

`AI_AGENT_STANDARDS_ROOT` is still accepted as a legacy alias for existing local setups.

The target folder must contain:

- `karpathy/principles.md`
- `SKILL-REFERENCE.md`
- `agent-guidance/INDEX.md`

## Related Docs

- [Client Configuration](client-configuration.md)
- [Usage Guide](usage.md)
- [Development Guide](development.md)
