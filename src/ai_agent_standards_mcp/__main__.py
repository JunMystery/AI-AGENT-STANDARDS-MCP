"""Command-line entry point for the Agent Guidance MCP server."""

from __future__ import annotations

import argparse
import sys

from .catalog import find_standards_root
from .server import create_server


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Agent Guidance MCP server.")
    parser.add_argument(
        "--root",
        help="Path to a standards corpus. Defaults to AI_AGENT_STANDARDS_ROOT or the bundled MCP repo corpus.",
    )
    return parser.parse_args()


def main() -> None:
    try:
        args = parse_args()
        root = find_standards_root(args.root)
        server = create_server(root)
        server.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
