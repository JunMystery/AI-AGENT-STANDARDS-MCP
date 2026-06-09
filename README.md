# AI Agent Standards MCP

Model Context Protocol server for the AI Agent Coding Standards corpus.

This server exposes the standards corpus, local skills, and recommendation
workflows as MCP resources, tools, and prompts.
The standards and skills are bundled in this repository so it can run as an
independent checkout. This repo intentionally excludes direct AI-agent
auto-discovery instruction files such as `AGENTS.md`, `CLAUDE.md`, and
`.cursorrules`; clients should consume the content through MCP.

## Install

```bash
python -m venv .venv
.venv\Scripts\pip install -e ".[dev]"
```

## Run

From this directory:

```bash
python -m ai_agent_standards_mcp
```

Or run directly from the source checkout with the scripts in `scripts/`:

```powershell
.\scripts\run-mcp.ps1
```

```cmd
scripts\run-mcp.cmd
```

Do not double-click the stdio launchers above. `stdio` is for MCP clients and
expects JSON-RPC messages on stdin.

For manual Windows use, open CMD or PowerShell first, then run the command from
that terminal. Do not launch the stdio scripts from Windows Explorer.

```bash
./scripts/run-mcp.sh
```

By default the server uses stdio transport and indexes the bundled standards
corpus in this repository. To point at another standards checkout:

```bash
$env:AI_AGENT_STANDARDS_ROOT="C:\path\to\AI-Agent-Standards"
python -m ai_agent_standards_mcp
```

For Streamable HTTP:

```bash
python -m ai_agent_standards_mcp --transport streamable-http
```

The HTTP host and port can be changed:

```bash
python -m ai_agent_standards_mcp --transport streamable-http --host 127.0.0.1 --port 41731
```

## MCP Surface

Resources:

- `standards://manifest` - JSON catalog summary.
- `standards://document/{slug}` - Markdown standards and framework documents.
- `standards://skill/{name}` - On-demand skill capsules.

Tools:

- `list_entries(category=None, kind=None)` - list indexed content.
- `get_entry(identifier)` - fetch content by slug, skill name, agent key, or path.
- `search_entries(query, limit=10, kind=None)` - keyword search with snippets.
- `recommend_context(task, limit=8)` - recommend standards and skills for a task.

Prompts:

- `apply_standards(task, focus="general")` - produce a standards-aware work prompt.
- `review_ai_code(scope="the current diff")` - produce a review prompt grounded in the framework.

## Bundled Corpus

The repository carries its own copy of:

- `skills/` - on-demand skill capsules.
- `ai-agent-standards/` - standards, prompts, compliance, and review docs.
- `karpathy/` - core principle source files.
- `docs/` - maintainer-facing notes for the standards corpus.

Wheel builds include this corpus under the package's bundled data fallback, while
editable/source checkouts index the top-level files directly.

Direct agent instruction files are intentionally excluded from this MCP-only
distribution.

## Development

```bash
python -m pytest
```

The test suite covers catalog discovery, lookup, search, and task-context
recommendations without needing to launch an MCP client.
