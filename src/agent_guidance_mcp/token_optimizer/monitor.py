"""Aggregate optimization metrics without retaining raw response bodies."""

from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Any


class PerformanceMonitor:
    """Monitor token optimization performance across MCP actions."""

    def __init__(self, recent_limit: int = 100) -> None:
        self.started_at = datetime.now(timezone.utc)
        self.total_actions = 0
        self.total_original_tokens = 0
        self.total_optimized_tokens = 0
        self.total_tokens_saved = 0
        self.optimization_errors = 0
        self.action_stats: dict[str, dict[str, Any]] = defaultdict(
            lambda: {
                "count": 0,
                "modified": 0,
                "total_saved": 0,
                "total_original": 0,
                "avg_saved_tokens": 0.0,
            }
        )
        self.strategy_counts: dict[str, int] = defaultdict(int)
        self.recent: deque[dict[str, Any]] = deque(maxlen=recent_limit)

    def record_optimization(self, result: Any) -> None:
        action = str(result.metadata.get("action_type", "unknown"))
        saved_tokens = max(0, result.original_tokens - result.optimized_tokens)

        self.total_actions += 1
        self.total_original_tokens += result.original_tokens
        self.total_optimized_tokens += result.optimized_tokens
        self.total_tokens_saved += saved_tokens

        stats = self.action_stats[action]
        stats["count"] += 1
        stats["total_saved"] += saved_tokens
        stats["total_original"] += result.original_tokens
        if result.modified:
            stats["modified"] += 1
        stats["avg_saved_tokens"] = stats["total_saved"] / stats["count"]

        for strategy in result.strategy_used.split("+"):
            if strategy and strategy not in {"none", "disabled", "error"}:
                self.strategy_counts[strategy] += 1

        self.recent.append(
            {
                "action_type": action,
                "content_type": result.content_type.value,
                "strategy": result.strategy_used,
                "modified": result.modified,
                "truncated": result.truncated,
                "original_tokens": result.original_tokens,
                "optimized_tokens": result.optimized_tokens,
                "saved_tokens": saved_tokens,
                "cache_hit": result.cache_hit,
            }
        )

    def record_error(self, action_type: str, error_message: str) -> None:
        self.optimization_errors += 1
        self.recent.append(
            {
                "action_type": action_type,
                "strategy": "error",
                "modified": False,
                "error": error_message[:200],
            }
        )

    def get_summary(self, detailed: bool = False, cache_stats: dict[str, int] | None = None) -> dict[str, Any]:
        avg_savings = (
            (self.total_tokens_saved / self.total_original_tokens) * 100
            if self.total_original_tokens
            else 0.0
        )
        summary: dict[str, Any] = {
            "total_actions": self.total_actions,
            "total_tokens_original": self.total_original_tokens,
            "total_tokens_optimized": self.total_optimized_tokens,
            "total_tokens_saved": self.total_tokens_saved,
            "average_savings_percent": round(avg_savings, 1),
            "optimization_errors": self.optimization_errors,
            "uptime_seconds": round(
                (datetime.now(timezone.utc) - self.started_at).total_seconds(), 3
            ),
            "cache": cache_stats or {},
            "top_strategies": dict(sorted(self.strategy_counts.items())),
        }
        if detailed:
            summary["by_action_type"] = dict(sorted(self.action_stats.items()))
            summary["recent"] = list(self.recent)
        return summary

    def reset(self) -> None:
        self.__init__(recent_limit=self.recent.maxlen or 100)
