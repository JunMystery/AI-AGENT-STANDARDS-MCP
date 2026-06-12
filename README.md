# Agent Guidance MCP (v3.1.0)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Version](https://img.shields.io/badge/mcp-%3E%3D1.0.0-green)](https://modelcontextprotocol.io/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](#development)

MCP server serving AI agent guidance through the AI Agent Coding Standards corpus, skill set, prompts, and bounded project-code context tools over **Stdio** transport.

![Agent Guidance MCP Architecture Flowchart](docs/images/architecture-flowchart.png)

## Installation

Automatic install:

```bash
python3 scripts/install-mcp.py        # Linux / macOS
python  scripts/install-mcp.py        # Windows
```

Manual install:

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"      # Linux / macOS
.venv\Scripts\pip install -e ".[dev]"  # Windows
```

Run the server module:

```bash
.venv/bin/python -m ai_agent_standards_mcp          # Linux / macOS
.venv\Scripts\python.exe -m ai_agent_standards_mcp  # Windows
```

To point the server to a different standards corpus, set:

```bash
AI_AGENT_STANDARDS_ROOT=/path/to/AI-Agent-Standards
```

Platform notes and client-specific setup are covered in [Installation](docs/installation.md) and [Client Configuration](docs/client-configuration.md).

## Quick Start

Run the server through an MCP client, or verify it locally with MCP Inspector:

```bash
npx @modelcontextprotocol/inspector .venv/bin/python -m ai_agent_standards_mcp
```

Then use the standards tools to load guidance and the project-context tools to inspect code before editing. See [Usage Guide](docs/usage.md) for practical workflows.

## Documentation

- [Installation](docs/installation.md) - automatic and manual setup.
- [Client Configuration](docs/client-configuration.md) - VS Code, GitHub Copilot, Claude Desktop, Cursor, Gemini-compatible config, and env vars.
- [Usage Guide](docs/usage.md) - quick checks, recommended agent workflows, and examples.
- [MCP Surface Reference](docs/mcp-surface.md) - all tools, prompts, and resources.
- [Project Context Tools](docs/project-context-tools.md) - tree, search, file read, snapshot export, token guidance, and freshness rules.
- [Development Guide](docs/development.md) - tests, project structure, and maintainer notes.
- [Repo Map For Agents](docs/repo-map-for-agents.md) - existing repository orientation notes.
- [Rules Generation](docs/rules-generation.md) - existing rules-generation documentation.
- [Skills Overview](docs/SKILLS_OVERVIEW.md) - generated index of packaged skills.

## MCP Surface

Core standards tools:

- `list_entries(category, kind)`
- `get_entry(identifier)`
- `search_entries(query, limit, kind)`
- `recommend_context(task, limit)`

Project-context tools:

- `get_project_tree(project_path, max_depth)`
- `search_project_code(project_path, query, limit)`
- `read_project_file(project_path, relative_path, start_line, max_lines)`
- `export_project_snapshot(project_path, output_path, max_file_bytes, max_total_bytes)`

Prompts include `/init`, `/plan`, `/design`, `/code`, `/run`, `/test`, `/deploy`, `/debug`, `/refactor`, `/audit`, `/rollback`, and `/recap`. Full details are in [MCP Surface Reference](docs/mcp-surface.md).

## Development

```bash
python -m pytest
```

The test suite verifies catalog discovery, MCP handler registration, standards search, recommendation behavior, and project-context tooling. See [Development Guide](docs/development.md) for more detail.
