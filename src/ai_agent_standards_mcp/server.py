"""MCP registration for AI Agent Coding Standards."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .catalog import StandardsCatalog, build_catalog

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover - exercised only without optional runtime dependency.
    FastMCP = None  # type: ignore[assignment]
    MCP_IMPORT_ERROR = exc
else:
    MCP_IMPORT_ERROR = None


def create_server(
    root: str | Path | None = None,
    host: str = "127.0.0.1",
    port: int = 41731,
) -> Any:
    if FastMCP is None:
        raise RuntimeError(
            "The 'mcp' package is required to run the server. Install with "
            "'pip install -e .', or 'pip install mcp'."
        ) from MCP_IMPORT_ERROR

    catalog = build_catalog(root)
    mcp = FastMCP("AI Agent Standards", json_response=True, host=host, port=port)
    register_handlers(mcp, catalog)
    return mcp


def register_handlers(mcp: Any, catalog: StandardsCatalog) -> None:
    @mcp.resource("standards://manifest", mime_type="application/json")
    def manifest() -> str:
        """Return the indexed standards manifest."""
        return catalog.manifest_json()

    @mcp.resource("standards://document/{identifier}", mime_type="text/markdown")
    def document(identifier: str) -> str:
        """Return a standards document by slug."""
        return catalog.read_entry(identifier)

    @mcp.resource("standards://skill/{name}", mime_type="text/markdown")
    def skill(name: str) -> str:
        """Return a local on-demand skill capsule by name."""
        return catalog.read_entry(name)

    @mcp.tool()
    def list_entries(category: str | None = None, kind: str | None = None) -> list[dict[str, str]]:
        """List standards catalog entries, optionally filtered by category or kind."""
        return catalog.list_entries(category=category, kind=kind)

    @mcp.tool()
    def get_entry(identifier: str) -> dict[str, str]:
        """Fetch a standards entry by slug, skill name, agent key, URI, or relative path."""
        entry = catalog.get_entry(identifier)
        return {
            **entry.to_dict(),
            "content": catalog.read_entry(entry.identifier),
        }

    @mcp.tool()
    def search_entries(
        query: str, limit: int = 10, kind: str | None = None
    ) -> list[dict[str, object]]:
        """Search standards entries and return ranked snippets."""
        return catalog.search_entries(query=query, limit=limit, kind=kind)

    @mcp.tool()
    def recommend_context(task: str, limit: int = 8) -> dict[str, object]:
        """Recommend standards, skills, and references for a coding task."""
        return catalog.recommend_context(task=task, limit=limit)

    @mcp.prompt()
    def apply_standards(task: str, focus: str = "general") -> str:
        """Generate a standards-aware prompt for a coding task."""
        recommendations = catalog.recommend_context(f"{focus} {task}", limit=6)
        lines = [
            "Apply AI-Coding-Standards v2.6.1 while completing this task.",
            "",
            f"Task: {task}",
            f"Focus: {focus}",
            "",
            "Load these references before coding:",
        ]
        for item in recommendations["recommendations"]:
            lines.append(f"- {item['path']} ({item['reason']})")
        lines.extend(
            [
                "",
                "Work expectations:",
                "- State assumptions and success criteria before non-trivial edits.",
                "- Keep changes surgical and match existing project patterns.",
                "- Verify with the smallest relevant tests or checks.",
            ]
        )
        return "\n".join(lines)

    @mcp.prompt()
    def review_ai_code(scope: str = "the current diff") -> str:
        """Generate an AI-code review prompt grounded in this standards framework."""
        return "\n".join(
            [
                f"Review {scope} against AI-Coding-Standards v2.6.1.",
                "",
                "Prioritize findings in this order:",
                "- Correctness bugs and behavioral regressions.",
                "- Security, secrets, auth, and data-handling risks.",
                "- Missing or weak tests for changed behavior.",
                "- Violations of surgical-change, simplicity, DRY, or organization rules.",
                "",
                "Useful references:",
                "- ai-agent-standards/quality-control/code-review-checklist.md",
                "- ai-agent-standards/quality-control/audit-ai-code-full.md",
                "- ai-agent-standards/risk-management/security-constraints.md",
                "- karpathy/principles.md",
            ]
        )
