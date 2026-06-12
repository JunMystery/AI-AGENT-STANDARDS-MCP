"""MCP registration for Agent Guidance MCP."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import project_context
from .catalog import StandardsCatalog, build_catalog
from .token_optimizer import OptimizationSettings, TokenOptimizer

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover - exercised only without optional runtime dependency.
    FastMCP = None  # type: ignore[assignment]
    MCP_IMPORT_ERROR = exc
else:
    MCP_IMPORT_ERROR = None


def create_server(
    root: str | Path | None = None,
) -> Any:
    if FastMCP is None:
        raise RuntimeError(
            "The 'mcp' package is required to run the server. Install with "
            "'pip install -e .', or 'pip install mcp'."
        ) from MCP_IMPORT_ERROR

    catalog = build_catalog(root)
    mcp = FastMCP("Agent Guidance MCP", json_response=True)
    register_handlers(mcp, catalog)
    return mcp


def register_handlers(mcp: Any, catalog: StandardsCatalog) -> None:
    settings = OptimizationSettings.from_env()
    optimizer = TokenOptimizer(settings.to_config())

    def optimize_response(
        content: Any,
        action_type: str,
        mutation_policy: str = "stats_only",
        *,
        rtk_enabled: bool | None = None,
        rtk_level: str | None = None,
        rtk_max_tokens: Any | None = None,
    ) -> Any:
        call_settings = settings.with_overrides(
            rtk_enabled=rtk_enabled,
            rtk_level=rtk_level,
            rtk_max_tokens=rtk_max_tokens,
        )
        result = optimizer.optimize(
            content,
            action_type=action_type,
            context={"mutation_policy": mutation_policy},
            config=call_settings.to_config(),
        )
        return result.optimized_content

    @mcp.resource("standards://manifest", mime_type="application/json")
    def manifest() -> str:
        """Return the indexed standards manifest."""
        return optimize_response(catalog.manifest_json(), "resource:standards://manifest")

    @mcp.resource("standards://document/{identifier}", mime_type="text/markdown")
    def document(identifier: str) -> str:
        """Return a standards document by slug."""
        return optimize_response(
            catalog.read_entry(identifier),
            "resource:standards://document",
        )

    @mcp.resource("standards://skill/{name}", mime_type="text/markdown")
    def skill(name: str) -> str:
        """Return a local on-demand skill capsule by name."""
        return optimize_response(catalog.read_entry(name), "resource:standards://skill")

    @mcp.tool()
    def list_entries(category: str | None = None, kind: str | None = None) -> list[dict[str, str]]:
        """List standards catalog entries, optionally filtered by category or kind."""
        return optimize_response(
            catalog.list_entries(category=category, kind=kind),
            "tool:list_entries",
        )

    @mcp.tool()
    def get_entry(identifier: str) -> dict[str, object]:
        """Fetch a standards entry by slug, skill name, agent key, URI, or relative path."""
        entry = catalog.get_entry(identifier)
        return optimize_response(
            {
                **entry.to_dict(),
                "content": catalog.read_entry(entry.identifier),
            },
            "tool:get_entry",
        )

    @mcp.tool()
    def search_entries(
        query: str, limit: int = 10, kind: str | None = None
    ) -> list[dict[str, object]]:
        """Search standards entries and return ranked snippets."""
        return optimize_response(
            catalog.search_entries(query=query, limit=limit, kind=kind),
            "tool:search_entries",
        )

    @mcp.tool()
    def recommend_context(task: str, limit: int = 8) -> dict[str, object]:
        """Recommend standards, skills, and references for a coding task."""
        return optimize_response(
            catalog.recommend_context(task=task, limit=limit),
            "tool:recommend_context",
        )

    @mcp.tool()
    def get_rtk_stats(detailed: bool = False) -> dict[str, object]:
        """Get RTK token optimization statistics for this server process."""
        cache_stats = optimizer.cache.stats() if optimizer.cache is not None else {}
        return optimizer.monitor.get_summary(detailed=detailed, cache_stats=cache_stats)

    @mcp.tool()
    def reset_rtk_stats() -> dict[str, object]:
        """Reset RTK token optimization statistics and cache for this server process."""
        optimizer.monitor.reset()
        if optimizer.cache is not None:
            optimizer.cache.clear()
        return {"status": "reset"}

    @mcp.tool()
    def export_project_snapshot(
        project_path: str = ".",
        output_path: str = project_context.DEFAULT_SNAPSHOT_PATH,
        max_file_bytes: int = project_context.DEFAULT_MAX_FILE_BYTES,
        max_total_bytes: int = project_context.DEFAULT_MAX_TOTAL_BYTES,
        rtk_enabled: bool | None = None,
        rtk_level: str | None = None,
        rtk_max_tokens: Any | None = None,
    ) -> dict[str, object]:
        """Export bounded project tree and code content for AI agent context."""
        return optimize_response(
            project_context.export_project_snapshot(
                project_path=project_path,
                output_path=output_path,
                max_file_bytes=max_file_bytes,
                max_total_bytes=max_total_bytes,
            ),
            "tool:export_project_snapshot",
            mutation_policy="safe_generated",
            rtk_enabled=rtk_enabled,
            rtk_level=rtk_level,
            rtk_max_tokens=rtk_max_tokens,
        )

    @mcp.tool()
    def get_project_tree(
        project_path: str = ".",
        max_depth: int = project_context.DEFAULT_MAX_DEPTH,
        rtk_enabled: bool | None = None,
        rtk_level: str | None = None,
        rtk_max_tokens: Any | None = None,
    ) -> dict[str, object]:
        """Return a bounded source tree for a project."""
        return optimize_response(
            project_context.get_project_tree(project_path=project_path, max_depth=max_depth),
            "tool:get_project_tree",
            mutation_policy="safe_generated",
            rtk_enabled=rtk_enabled,
            rtk_level=rtk_level,
            rtk_max_tokens=rtk_max_tokens,
        )

    @mcp.tool()
    def read_project_file(
        project_path: str = ".",
        relative_path: str = "",
        start_line: int = 1,
        max_lines: int = 300,
        rtk_enabled: bool | None = None,
        rtk_level: str | None = None,
        rtk_max_tokens: Any | None = None,
    ) -> dict[str, object]:
        """Read a bounded line range from one project text file."""
        return optimize_response(
            project_context.read_project_file(
                project_path=project_path,
                relative_path_value=relative_path,
                start_line=start_line,
                max_lines=max_lines,
            ),
            "tool:read_project_file",
            mutation_policy="edit_critical",
            rtk_enabled=rtk_enabled,
            rtk_level=rtk_level,
            rtk_max_tokens=rtk_max_tokens,
        )

    @mcp.tool()
    def search_project_code(
        project_path: str = ".",
        query: str = "",
        limit: int = 20,
        rtk_enabled: bool | None = None,
        rtk_level: str | None = None,
        rtk_max_tokens: Any | None = None,
    ) -> dict[str, object]:
        """Search project source files and return bounded snippets."""
        return optimize_response(
            project_context.search_project_code(
                project_path=project_path, query=query, limit=limit
            ),
            "tool:search_project_code",
            mutation_policy="safe_generated",
            rtk_enabled=rtk_enabled,
            rtk_level=rtk_level,
            rtk_max_tokens=rtk_max_tokens,
        )

    @mcp.prompt()
    def apply_standards(task: str = "", focus: str = "general") -> str:
        """Generate a standards-aware prompt for a coding task."""
        recommendations = catalog.recommend_context(f"{focus} {task}".strip(), limit=6)
        lines = [
            "Apply AI-Coding-Standards v3.2.0 while completing this task.",
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
        return optimize_response("\n".join(lines), "prompt:apply_standards")

    @mcp.prompt()
    def review_ai_code(scope: str = "the current diff") -> str:
        """Generate an AI-code review prompt grounded in this standards framework."""
        return optimize_response(
            "\n".join(
                [
                    f"Review {scope} against AI-Coding-Standards v3.2.0.",
                    "",
                    "Prioritize findings in this order:",
                    "- Correctness bugs and behavioral regressions.",
                    "- Security, secrets, auth, and data-handling risks.",
                    "- Missing or weak tests for changed behavior.",
                    "- Violations of surgical-change, simplicity, DRY, or organization rules.",
                    "",
                    "Useful references:",
                    "- agent-guidance/quality-control/code-review-checklist.md",
                    "- agent-guidance/quality-control/audit-ai-code-full.md",
                    "- agent-guidance/risk-management/security-constraints.md",
                    "- karpathy/principles.md",
                ]
            ),
            "prompt:review_ai_code",
        )

    @mcp.prompt()
    def init(project_name: str = "") -> str:
        """Initialize a new project."""
        content = catalog.read_entry("workflow-init")
        if project_name:
            return optimize_response(f"{content}\n\nProject Name: {project_name}", "prompt:init")
        return optimize_response(content, "prompt:init")

    @mcp.prompt()
    def plan(task: str = "") -> str:
        """Plan feature designs."""
        content = catalog.read_entry("workflow-plan")
        if task:
            return optimize_response(f"{content}\n\nTask to plan: {task}", "prompt:plan")
        return optimize_response(content, "prompt:plan")

    @mcp.prompt()
    def design(feature: str = "") -> str:
        """Technical design for features."""
        content = catalog.read_entry("workflow-design")
        if feature:
            return optimize_response(f"{content}\n\nFeature to design: {feature}", "prompt:design")
        return optimize_response(content, "prompt:design")

    @mcp.prompt()
    def visualize(ui_description: str = "") -> str:
        """UI/UX interface design."""
        content = catalog.read_entry("workflow-visualize")
        if ui_description:
            return optimize_response(
                f"{content}\n\nUI Description: {ui_description}",
                "prompt:visualize",
            )
        return optimize_response(content, "prompt:visualize")

    @mcp.prompt()
    def code(task: str = "") -> str:
        """Implement high-quality features."""
        content = catalog.read_entry("workflow-code")
        if task:
            return optimize_response(f"{content}\n\nTask to implement:\n{task}", "prompt:code")
        return optimize_response(content, "prompt:code")

    @mcp.prompt()
    def run(environment: str = "local") -> str:
        """Run/launch the application."""
        content = catalog.read_entry("workflow-run")
        return optimize_response(f"{content}\n\nTarget environment: {environment}", "prompt:run")

    @mcp.prompt()
    def test(test_target: str = "") -> str:
        """Run test cases and write tests automatically."""
        content = catalog.read_entry("workflow-test")
        if test_target:
            return optimize_response(f"{content}\n\nTest target: {test_target}", "prompt:test")
        return optimize_response(content, "prompt:test")

    @mcp.prompt()
    def deploy(target: str = "production") -> str:
        """Deploy the application to production/staging."""
        content = catalog.read_entry("workflow-deploy")
        return optimize_response(f"{content}\n\nDeploy target: {target}", "prompt:deploy")

    @mcp.prompt()
    def debug(error_message: str = "") -> str:
        """Analyze and fix bugs automatically."""
        content = catalog.read_entry("workflow-debug")
        if error_message:
            return optimize_response(
                f"{content}\n\nError/Bug Description:\n{error_message}",
                "prompt:debug",
            )
        return optimize_response(content, "prompt:debug")

    @mcp.prompt()
    def refactor(target_file: str = "") -> str:
        """Optimize and refactor code safely."""
        content = catalog.read_entry("workflow-refactor")
        if target_file:
            return optimize_response(
                f"{content}\n\nFile or module to refactor: {target_file}",
                "prompt:refactor",
            )
        return optimize_response(content, "prompt:refactor")

    @mcp.prompt()
    def audit(scope: str = "security") -> str:
        """Audit project health."""
        content = catalog.read_entry("workflow-audit")
        return optimize_response(f"{content}\n\nAudit scope: {scope}", "prompt:audit")

    @mcp.prompt()
    def rollback(revision: str = "") -> str:
        """Safely rollback to a previous state."""
        content = catalog.read_entry("workflow-rollback")
        if revision:
            return optimize_response(
                f"{content}\n\nRollback revision/commit: {revision}",
                "prompt:rollback",
            )
        return optimize_response(content, "prompt:rollback")

    @mcp.prompt()
    def recap(session_id: str = "") -> str:
        """Restore working context from a previous session."""
        content = catalog.read_entry("workflow-recap")
        if session_id:
            return optimize_response(f"{content}\n\nSession ID: {session_id}", "prompt:recap")
        return optimize_response(content, "prompt:recap")
