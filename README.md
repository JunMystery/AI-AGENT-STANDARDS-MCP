# AI Agent Standards MCP

Model Context Protocol server for the AI Agent Coding Standards repository.

This server exposes the standards corpus, local skills, generated agent
instructions, and recommendation workflows as MCP resources, tools, and prompts.
It is designed to run next to this repository by default, or against any checkout
passed with `AI_AGENT_STANDARDS_ROOT`.

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

By default the server uses stdio transport and detects the parent
`AI-Agent-Standards` repository. To point at another checkout:

```bash
$env:AI_AGENT_STANDARDS_ROOT="C:\path\to\AI-Agent-Standards"
python -m ai_agent_standards_mcp
```

For Streamable HTTP:

```bash
python -m ai_agent_standards_mcp --transport streamable-http
```

## MCP Surface

Resources:

- `standards://manifest` - JSON catalog summary.
- `standards://document/{slug}` - Markdown standards and framework documents.
- `standards://skill/{name}` - On-demand skill capsules.
- `standards://agent/{key}` - Generated agent instruction files.

Tools:

- `list_entries(category=None, kind=None)` - list indexed content.
- `get_entry(identifier)` - fetch content by slug, skill name, agent key, or path.
- `search_entries(query, limit=10, kind=None)` - keyword search with snippets.
- `recommend_context(task, limit=8)` - recommend standards and skills for a task.

Prompts:

- `apply_standards(task, focus="general")` - produce a standards-aware work prompt.
- `review_ai_code(scope="the current diff")` - produce a review prompt grounded in the framework.

## Development

```bash
python -m pytest
```

The test suite covers catalog discovery, lookup, search, and task-context
recommendations without needing to launch an MCP client.
