# Development Guide

[Back to README](../README.md)

This project is a small Python package that exposes Agent Guidance MCP over MCP, backed by the AI Agent Coding Standards corpus.

## Setup

Install the package in editable mode with dev dependencies:

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\pip install -e ".[dev]"
```

## Test

Run the test suite:

```bash
python -m pytest
```

If the system Python does not have `pytest`, use the repository virtual environment:

```bash
.venv/bin/python -m pytest
```

Run a whitespace check before committing:

```bash
git diff --check
```

## Project Structure

```text
AI-Agent-Standards-mcp/
├── ai-agent-standards/          # Core standards corpus
├── docs/                        # Maintainer and user documentation
├── karpathy/                    # Karpathy framework references
├── scripts/                     # Installer, launchers, docs generators
├── skills/                      # On-demand skill capsules
├── src/ai_agent_standards_mcp/  # Python package source
├── tests/                       # Pytest suite
├── PROJECT-STANDARDS.md         # Project-specific agent standards
├── pyproject.toml               # Python package metadata
├── README.md                    # Compact landing page
└── SKILL-REFERENCE.md           # Skill category reference
```

## Core Source Files

- `server.py`: FastMCP registration and MCP surface declarations.
- `catalog.py`: standards catalog indexing, search, and recommendations.
- `paths.py`: standards root discovery and safe corpus path resolution.
- `text.py`: text normalization, snippet, and keyword helpers.
- `project_context.py`: public project-context tool helpers.
- `project_scan.py`: project-context traversal and filtering internals.
- `__main__.py`: command-line module launcher.

## Documentation Notes

- Keep `README.md` compact and link to detailed docs.
- Keep generated documentation such as `docs/SKILLS_OVERVIEW.md` managed by its generator.
- Add new user-facing reference docs under `docs/`.
- Use relative Markdown links so GitHub and IDE previews can open files directly.

## Packaging Notes

The wheel includes:

- `SKILL-REFERENCE.md`
- `docs/`
- `karpathy/`
- `skills/`
- `ai-agent-standards/`

These paths are configured in `pyproject.toml`.

## Related Docs

- [Installation](installation.md)
- [Client Configuration](client-configuration.md)
- [MCP Surface Reference](mcp-surface.md)
