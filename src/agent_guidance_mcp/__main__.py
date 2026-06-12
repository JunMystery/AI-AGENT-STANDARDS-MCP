"""Command-line entry point for the Agent Guidance MCP server."""

from __future__ import annotations

import argparse
import json
import os
import sys

from .catalog import find_standards_root
from .server import create_server
from .token_optimizer import OptimizationSettings, TokenOptimizer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Agent Guidance MCP server.")
    parser.add_argument(
        "--root",
        help=(
            "Path to a standards corpus. Defaults to AGENT_GUIDANCE_ROOT, "
            "legacy AI_AGENT_STANDARDS_ROOT, or the bundled MCP repo corpus."
        ),
    )
    parser.add_argument(
        "--optimize-all",
        dest="optimize_all",
        action="store_true",
        help="Enable RTK optimization for all MCP responses.",
    )
    parser.add_argument(
        "--no-optimize-all",
        dest="optimize_all",
        action="store_false",
        help="Disable RTK optimization for all MCP responses.",
    )
    parser.add_argument(
        "--show-stats",
        action="store_true",
        help="Print RTK settings and empty fresh-process startup stats, then exit.",
    )
    parser.set_defaults(optimize_all=None)
    return parser.parse_args()


def main() -> None:
    try:
        args = parse_args()
        if args.optimize_all is not None:
            os.environ["RTK_OPTIMIZATION_ENABLED"] = "true" if args.optimize_all else "false"
        if args.show_stats:
            settings = OptimizationSettings.from_env()
            optimizer = TokenOptimizer(settings.to_config())
            cache_stats = optimizer.cache.stats() if optimizer.cache is not None else {}
            payload = {
                "settings": {
                    "enabled": settings.enabled,
                    "level": settings.level,
                    "max_tokens": settings.max_tokens,
                    "cache_enabled": settings.cache_enabled,
                    "cache_ttl": settings.cache_ttl,
                    "auto_detect": settings.auto_detect,
                    "log_metrics": settings.log_metrics,
                },
                "stats": optimizer.monitor.get_summary(
                    detailed=True, cache_stats=cache_stats
                ),
            }
            print(json.dumps(payload, indent=2, sort_keys=True))
            return
        root = find_standards_root(args.root)
        server = create_server(root)
        server.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
