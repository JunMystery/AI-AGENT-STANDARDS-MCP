"""Command-line entry point for the AI Agent Standards MCP server."""

from __future__ import annotations

import argparse

from .catalog import find_standards_root
from .server import create_server


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the AI Agent Standards MCP server.")
    parser.add_argument(
        "--root",
        help="Path to a standards corpus. Defaults to AI_AGENT_STANDARDS_ROOT or the bundled MCP repo corpus.",
    )
    parser.add_argument(
        "--transport",
        choices=("stdio", "streamable-http"),
        default="stdio",
        help="MCP transport to use.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for HTTP transports. Defaults to 127.0.0.1.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=41731,
        help="Port for HTTP transports. Defaults to 41731.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = find_standards_root(args.root)
    server = create_server(root, host=args.host, port=args.port)
    server.run(transport=args.transport)


if __name__ == "__main__":
    main()
