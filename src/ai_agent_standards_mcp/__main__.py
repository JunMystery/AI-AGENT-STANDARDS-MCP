"""Command-line entry point for the AI Agent Standards MCP server."""

from __future__ import annotations

import argparse

from .catalog import find_standards_root
from .server import create_server


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the AI Agent Standards MCP server.")
    parser.add_argument(
        "--root",
        help="Path to the AI-Agent-Standards repository. Defaults to AI_AGENT_STANDARDS_ROOT or parent checkout detection.",
    )
    parser.add_argument(
        "--transport",
        choices=("stdio", "streamable-http"),
        default="stdio",
        help="MCP transport to use.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = find_standards_root(args.root)
    server = create_server(root)
    server.run(transport=args.transport)


if __name__ == "__main__":
    main()
