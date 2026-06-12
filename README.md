# AI Agent Standards MCP (v3.0.3)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Version](https://img.shields.io/badge/mcp-%3E%3D1.0.0-green)](https://modelcontextprotocol.io/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](#development)

MCP server serving the AI Agent Coding Standards corpus and skill set v3.0.3 over **Stdio** transport (no HTTP required).

![AI Agent Standards MCP Architecture Flowchart](docs/images/architecture-flowchart.png)

---

## Install

**Automatic (recommended):**
```bash
python3 scripts/install-mcp.py        # Linux / macOS
python  scripts/install-mcp.py        # Windows
```

**Manual:**
```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"      # Linux / macOS
.venv\Scripts\pip install -e ".[dev]"  # Windows
```

---

## MCP Client Config

### VS Code & GitHub Copilot (Automatic Workspace Discovery)
We have included a preconfigured workspace MCP settings file under `.vscode/mcp.json`.
When you open this repository in VS Code with GitHub Copilot installed:
1. Ensure you have run the installation script to create the `.venv` directory.
2. VS Code will automatically detect the MCP server listed in `.vscode/mcp.json`.
3. You will be prompted to trust the server. Once approved, the tools and prompts will be available directly in GitHub Copilot Chat.

> [!NOTE]
> By default, `.vscode/mcp.json` points to the Linux/macOS Python path (`.venv/bin/python`).
> If you are on **Windows**, edit `.vscode/mcp.json` to change the command path to point to the Windows executable:
> ```json
> "command": "${workspaceFolder}/.venv/Scripts/python.exe"
> ```

---

### Other MCP Clients (Claude Desktop, Cursor, etc.)
Manually add the following configurations to your global MCP client settings:

**Linux / macOS**
```json
{
  "mcpServers": {
    "ai-agent-standards-mcp": {
      "command": "/absolute/path/to/repo/.venv/bin/python",
      "args": ["-m", "ai_agent_standards_mcp"],
      "env": { "PYTHONPATH": "/absolute/path/to/repo/src" }
    }
  }
}
```

**Windows**
```json
{
  "mcpServers": {
    "ai-agent-standards-mcp": {
      "command": "C:\\absolute\\path\\to\\repo\\.venv\\Scripts\\python.exe",
      "args": ["-m", "ai_agent_standards_mcp"],
      "env": { "PYTHONPATH": "C:\\absolute\\path\\to\\repo\\src" }
    }
  }
}
```

> [!TIP]
> To point the server to a different standards folder, set the environment variable:
> `AI_AGENT_STANDARDS_ROOT=/path/to/AI-Agent-Standards`

---

## Quick Example

Verify the server locally using the MCP Inspector:
```bash
npx @modelcontextprotocol/inspector .venv/bin/python -m ai_agent_standards_mcp
```
Open the printed URL (usually `http://localhost:5173`) in your browser to interactively test tools and prompts.

---

## MCP Surface

### Tools
| Tool | Description |
|---|---|
| `list_entries(category, kind)` | List all indexed standards and skills content |
| `get_entry(identifier)` | Retrieve specific content by slug, skill name, or path |
| `search_entries(query, limit, kind)` | Perform full-text search with match snippets |
| `recommend_context(task, limit)` | Recommend relevant standards and skills for a given task |

### Prompts (Slash Commands)
| Prompt | AWF Command | Description |
|---|---|---|
| `apply_standards` | – | Generate a standards-aware system instructions prompt |
| `review_ai_code` | – | Review code against the Karpathy principles framework |
| `init` | `/init` | Initialize a new project workflow |
| `plan` | `/plan` | Plan feature design and workflow layout |
| `design` | `/design` | Technical architectural design guidelines |
| `visualize` | `/visualize` | Create UI/UX Mockups and design guides |
| `code` | `/code` | Write high-quality compliant code implementations |
| `run` | `/run` | Build, run, and verify the application environment |
| `test` | `/test` | Write and execute unit/integration test suites |
| `deploy` | `/deploy` | Check safety checklists before deployment |
| `debug` | `/debug` | Systematic troubleshooting and error-solving protocol |
| `refactor` | `/refactor` | Safe code refactoring instructions |
| `audit` | `/audit` | Execute security and system-health audits |
| `rollback` | `/rollback` | Execute emergency recovery/rollback steps |
| `recap` | `/recap` | Rebuild workspace and context session state |

### Resources
- `standards://manifest` — Catalog outline containing all available documents
- `standards://document/{slug}` — Core standards and framework manuals
- `standards://skill/{name}` — On-demand skill capsules

---

## Project Tree

```
AI-Agent-Standards-mcp/
├── .vscode/
│   └── mcp.json                 # Automatic VS Code/Copilot MCP server discovery config
├── ai-agent-standards/          # Core standards corpus
│   ├── compliance/              # Checklists for accessibility and guidelines compliance
│   ├── engineering-practices/   # Best practices on testing, documenting, and releasing
│   ├── multi-agent/             # Prompts tailored for various agent roles
│   ├── onboarding/              # Guides to familiarize new agents with workflows
│   ├── principles/              # Foundation rules based on Karpathy framework
│   ├── prompts/                 # Standardized system prompts and cookbooks
│   ├── quality-control/         # Self-checking templates and review practices
│   ├── reference/               # Glossary and complete error index
│   ├── risk-management/         # Security boundaries and escalations
│   ├── CHANGELOG.md
│   └── INDEX.md
├── docs/
│   ├── images/                  # Media assets (flowcharts, diagrams)
│   ├── SKILLS_OVERVIEW.md       # Auto-generated index listing all active skills
│   ├── repo-map-for-agents.md
│   └── rules-generation.md
├── karpathy/                    # Reference documents for Karpathy framework
├── scripts/
│   ├── generate-skills-overview.py
│   ├── install-mcp.py
│   └── run-mcp.cmd / .ps1 / .sh / .py
├── skills/                      # Custom-scoped capsule folders (each contains SKILL.md)
│   └── <skill-name>/SKILL.md
├── src/ai_agent_standards_mcp/  # Python package source code
│   ├── server.py                # FastMCP configuration and tool declarations
│   ├── catalog.py               # Memory indexing, search, and categorization logic
│   ├── paths.py                 # Resolves file paths for standard documents
│   ├── text.py                  # Text extraction and parsing utilities
│   └── __main__.py              # Server launcher
├── tests/                       # Automated Pytest suite
├── LICENSE                      # License details (MIT)
├── PROJECT-STANDARDS.md         # Custom project instructions (index-enabled)
├── pyproject.toml               # Python project configuration
├── README.md                    # Main repository documentation
└── SKILL-REFERENCE.md           # Reference map listing all skill categories
```

---

## Development

```bash
python -m pytest
```

The pytest suite verifies catalog discovery, lookup, searching, and context recommendation features locally.
