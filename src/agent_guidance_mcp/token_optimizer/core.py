"""Core RTK token optimizer for MCP response payloads."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from math import ceil
from typing import Any

from .cache import OptimizedCache
from .monitor import PerformanceMonitor
from .strategies import (
    AdaptiveTruncation,
    PatternDeduplication,
    SemanticCompression,
    StructuralGrouping,
    compact_json_text,
)


class ContentType(Enum):
    TEXT = "text"
    JSON = "json"
    CODE = "code"
    TABLE = "table"
    LIST = "list"
    TREE = "tree"
    DIFF = "diff"
    LOG = "log"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class OptimizationConfig:
    enabled: bool = True
    level: str = "conservative"
    auto_detect_type: bool = True
    max_tokens: int = 12_000
    preserve_structure: bool = True
    aggressive_mode: bool = False
    cache_enabled: bool = True
    cache_ttl: int = 300
    log_metrics: bool = False


@dataclass(frozen=True)
class OptimizationResult:
    optimized_content: Any
    original_tokens: int
    optimized_tokens: int
    savings_percent: float
    strategy_used: str
    content_type: ContentType
    cache_hit: bool = False
    modified: bool = False
    truncated: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def saved_tokens(self) -> int:
        return max(0, self.original_tokens - self.optimized_tokens)

    def rtk_metadata(self) -> dict[str, Any]:
        payload = {
            "enabled": True,
            "modified": self.modified,
            "truncated": self.truncated,
            "content_type": self.content_type.value,
            "strategy": self.strategy_used,
            "original_tokens": self.original_tokens,
            "optimized_tokens": self.optimized_tokens,
            "saved_tokens": self.saved_tokens,
            "savings_percent": self.savings_percent,
            "cache_hit": self.cache_hit,
        }
        for key in (
            "omitted_count",
            "omitted_lines",
            "omitted_chars",
            "collapsed_count",
            "cap_exceeded_by_metadata",
            "continuation",
            "summary",
            "error",
        ):
            if key in self.metadata:
                payload[key] = self.metadata[key]
        return payload


class TokenOptimizer:
    """Universal optimizer that defaults to safe, stats-first behavior."""

    def __init__(
        self,
        config: OptimizationConfig | None = None,
        monitor: PerformanceMonitor | None = None,
    ) -> None:
        self.config = config or OptimizationConfig()
        self.cache: OptimizedCache[OptimizationResult] | None = (
            OptimizedCache(self.config.cache_ttl) if self.config.cache_enabled else None
        )
        self.monitor = monitor or PerformanceMonitor()
        self.semantic = SemanticCompression()
        self.structural = StructuralGrouping()
        self.truncation = AdaptiveTruncation()
        self.deduplication = PatternDeduplication()

    def optimize(
        self,
        content: Any,
        action_type: str = "unknown",
        context: dict[str, Any] | None = None,
        config: OptimizationConfig | None = None,
    ) -> OptimizationResult:
        active_config = config or self.config
        context = context or {}
        serialized = self._serialize_content(content)
        content_type = self._detect_content_type(content, serialized, action_type)
        original_tokens = self.count_tokens(serialized)

        if not active_config.enabled:
            result = self._result(
                content,
                original_tokens,
                original_tokens,
                "disabled",
                content_type,
                action_type,
                modified=False,
            )
            self.monitor.record_optimization(result)
            return result

        cache_key = self._cache_key(serialized, action_type, context, active_config)
        if self.cache is not None:
            cached = self.cache.get(cache_key)
            if cached is not None:
                if isinstance(cached.optimized_content, dict):
                    optimized = copy.deepcopy(cached.optimized_content)
                    cached = OptimizationResult(
                        optimized_content=optimized,
                        original_tokens=cached.original_tokens,
                        optimized_tokens=cached.optimized_tokens,
                        savings_percent=cached.savings_percent,
                        strategy_used=cached.strategy_used,
                        content_type=cached.content_type,
                        cache_hit=True,
                        modified=cached.modified,
                        truncated=cached.truncated,
                        metadata=cached.metadata,
                    )
                    optimized["rtk"] = cached.rtk_metadata()
                self.monitor.record_optimization(cached)
                return cached

        try:
            result = self._optimize_uncached(
                content, serialized, action_type, context, active_config, content_type
            )
        except Exception as exc:  # pragma: no cover - defensive fallback.
            self.monitor.record_error(action_type, exc.__class__.__name__)
            result = self._result(
                content,
                original_tokens,
                original_tokens,
                "error",
                content_type,
                action_type,
                modified=False,
                metadata={"error": exc.__class__.__name__},
            )

        self.monitor.record_optimization(result)
        if self.cache is not None and result.modified and result.saved_tokens > 0:
            self.cache.set(cache_key, result)
        return result

    def _optimize_uncached(
        self,
        content: Any,
        serialized: str,
        action_type: str,
        context: dict[str, Any],
        config: OptimizationConfig,
        content_type: ContentType,
    ) -> OptimizationResult:
        original_tokens = self.count_tokens(serialized)
        max_chars = max(1, config.max_tokens * 4)
        policy = str(context.get("mutation_policy", "stats_only"))

        if isinstance(content, dict):
            optimized, metadata, strategies, truncated = self._optimize_mapping(
                content, action_type, policy, max_chars, config
            )
            return self._finalize(
                optimized,
                original_tokens,
                serialized,
                strategies,
                content_type,
                action_type,
                truncated,
                metadata,
                max_chars,
            )

        if isinstance(content, list):
            return self._result(
                content, original_tokens, original_tokens, "none", content_type, action_type
            )

        optimized_text, metadata, strategies, truncated = self._optimize_text(
            serialized, content_type, policy, max_chars, config
        )
        return self._finalize(
            optimized_text,
            original_tokens,
            serialized,
            strategies,
            content_type,
            action_type,
            truncated,
            metadata,
            max_chars,
        )

    def _optimize_mapping(
        self,
        content: dict[str, Any],
        action_type: str,
        policy: str,
        max_chars: int,
        config: OptimizationConfig,
    ) -> tuple[dict[str, Any], dict[str, Any], list[str], bool]:
        optimized = dict(content)
        metadata: dict[str, Any] = {}
        strategies: list[str] = []
        truncated = False

        if policy == "edit_critical" and isinstance(content.get("content"), str):
            text = str(content["content"])
            if len(text) > max_chars:
                optimized_text, trim_meta = self._truncate_edit_content(content, text, max_chars)
                optimized["content"] = optimized_text
                optimized["end_line"] = trim_meta.get("visible_end_line", optimized.get("end_line"))
                metadata.update(trim_meta)
                strategies.append("safe_truncation")
                truncated = True
            return optimized, metadata, strategies, truncated

        serialized = self._serialize_content(content)
        over_budget = len(serialized) > max_chars
        allow_generated = policy == "safe_generated"
        level = config.level

        if action_type.endswith("get_project_tree") and isinstance(content.get("tree"), list):
            tree = list(content["tree"])
            metadata["summary"] = self.structural.summarize_tree(
                [entry for entry in tree if isinstance(entry, dict)]
            )
            if over_budget or level in {"balanced", "aggressive"} and allow_generated:
                max_items = self._list_budget(tree, max_chars)
                compact, compact_meta = self.structural.compact_entries(tree, max_items)
                if compact_meta["omitted_count"]:
                    optimized["tree"] = compact
                    metadata.update(compact_meta)
                    strategies.append("structural")
                    truncated = True
            return optimized, metadata, strategies, truncated

        if action_type.endswith("search_project_code") and isinstance(content.get("matches"), list):
            matches = list(content["matches"])
            if over_budget and allow_generated:
                max_items = self._list_budget(matches, max_chars)
                compact, compact_meta = self.structural.compact_entries(matches, max_items)
                if compact_meta["omitted_count"]:
                    optimized["matches"] = compact
                    metadata.update(compact_meta)
                    strategies.append("structural")
                    truncated = True
            return optimized, metadata, strategies, truncated

        if over_budget and allow_generated:
            text, text_meta = self.truncation.truncate(serialized, "json", max_chars)
            try:
                loaded = json.loads(text)
            except json.JSONDecodeError:
                return optimized, metadata, strategies, truncated
            if isinstance(loaded, dict):
                metadata.update(text_meta)
                strategies.append("truncation")
                truncated = True
                return loaded, metadata, strategies, truncated

        return optimized, metadata, strategies, truncated

    def _optimize_text(
        self,
        content: str,
        content_type: ContentType,
        policy: str,
        max_chars: int,
        config: OptimizationConfig,
    ) -> tuple[str, dict[str, Any], list[str], bool]:
        if policy == "stats_only":
            return content, {}, [], False

        text_type = content_type.value
        metadata: dict[str, Any] = {}
        strategies: list[str] = []
        optimized = content
        truncated = False
        over_budget = len(content) > max_chars

        if config.level == "aggressive" and text_type in {"text", "log", "error"}:
            optimized, semantic_meta = self.semantic.compress(optimized, text_type, max_chars)
            metadata.update(semantic_meta)
            if optimized != content:
                strategies.append("semantic")

        if config.level in {"balanced", "aggressive"} and text_type in {"log", "error", "text"}:
            deduped, dedup_meta = self.deduplication.deduplicate(optimized, text_type)
            metadata.update(dedup_meta)
            if deduped != optimized:
                optimized = deduped
                strategies.append("deduplication")

        if over_budget or len(optimized) > max_chars:
            optimized, trunc_meta = self.truncation.truncate(optimized, text_type, max_chars)
            metadata.update(trunc_meta)
            strategies.append("truncation")
            truncated = True

        return optimized, metadata, strategies, truncated

    def _truncate_edit_content(
        self, payload: dict[str, Any], text: str, max_chars: int
    ) -> tuple[str, dict[str, Any]]:
        lines = text.splitlines()
        kept: list[str] = []
        used = 0
        for line in lines:
            needed = len(line) + 1
            if kept and used + needed > max_chars:
                break
            kept.append(line)
            used += needed

        start_line = int(payload.get("start_line", 1) or 1)
        visible_end = start_line + len(kept) - 1 if kept else start_line - 1
        continuation = None
        omitted_lines = max(0, len(lines) - len(kept))
        if omitted_lines:
            continuation = {
                "next_start_line": visible_end + 1,
                "suggested_tool": "read_project_file",
            }
        return "\n".join(kept), {
            "omitted_lines": omitted_lines,
            "omitted_chars": max(0, len(text) - used),
            "continuation": continuation,
            "visible_end_line": visible_end,
        }

    def _finalize(
        self,
        optimized: Any,
        original_tokens: int,
        original_serialized: str,
        strategies: list[str],
        content_type: ContentType,
        action_type: str,
        truncated: bool,
        metadata: dict[str, Any],
        max_chars: int,
    ) -> OptimizationResult:
        optimized_serialized = self._serialize_content(optimized)
        optimized_tokens = self.count_tokens(optimized_serialized)
        modified = optimized_serialized != original_serialized
        strategy = "+".join(strategies) if strategies else "none"
        result = self._result(
            optimized,
            original_tokens,
            optimized_tokens,
            strategy,
            content_type,
            action_type,
            modified=modified,
            truncated=truncated,
            metadata=metadata,
        )

        if isinstance(optimized, dict):
            optimized["rtk"] = result.rtk_metadata()
            final_serialized = self._serialize_content(optimized)
            final_tokens = self.count_tokens(final_serialized)
            if len(final_serialized) > max_chars:
                metadata = dict(metadata)
                metadata["cap_exceeded_by_metadata"] = True
            for _ in range(5):
                result = self._result(
                    optimized,
                    original_tokens,
                    final_tokens,
                    strategy,
                    content_type,
                    action_type,
                    modified=modified,
                    truncated=truncated,
                    metadata=metadata,
                )
                optimized["rtk"] = result.rtk_metadata()
                final_serialized = self._serialize_content(optimized)
                next_tokens = self.count_tokens(final_serialized)
                if next_tokens == final_tokens:
                    break
                final_tokens = next_tokens
        return result

    def _result(
        self,
        content: Any,
        original_tokens: int,
        optimized_tokens: int,
        strategy: str,
        content_type: ContentType,
        action_type: str,
        *,
        modified: bool = False,
        truncated: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> OptimizationResult:
        savings = (
            ((original_tokens - optimized_tokens) / original_tokens) * 100
            if original_tokens
            else 0.0
        )
        payload = dict(metadata or {})
        payload["action_type"] = action_type
        return OptimizationResult(
            optimized_content=content,
            original_tokens=original_tokens,
            optimized_tokens=optimized_tokens,
            savings_percent=round(max(0.0, savings), 1),
            strategy_used=strategy,
            content_type=content_type,
            modified=modified,
            truncated=truncated,
            metadata=payload,
        )

    def _detect_content_type(self, content: Any, serialized: str, action_type: str) -> ContentType:
        if action_type.endswith("get_project_tree"):
            return ContentType.TREE
        if action_type.endswith("search_project_code"):
            return ContentType.LIST
        if isinstance(content, (dict, list)):
            return ContentType.JSON
        if not self.config.auto_detect_type:
            return ContentType.UNKNOWN
        if self._is_json(serialized):
            return ContentType.JSON
        if self._is_error(serialized):
            return ContentType.ERROR
        if self._is_diff(serialized):
            return ContentType.DIFF
        if self._is_log(serialized):
            return ContentType.LOG
        if self._is_code(serialized):
            return ContentType.CODE
        if self._is_table(serialized):
            return ContentType.TABLE
        if self._is_tree(serialized):
            return ContentType.TREE
        if self._is_list(serialized):
            return ContentType.LIST
        return ContentType.TEXT

    @staticmethod
    def count_tokens(text: str) -> int:
        return ceil(len(text) / 4) if text else 0

    @staticmethod
    def _serialize_content(content: Any) -> str:
        if isinstance(content, (dict, list)):
            return json.dumps(content, ensure_ascii=False, sort_keys=True)
        return str(content)

    @staticmethod
    def _is_json(content: str) -> bool:
        try:
            json.loads(content)
        except json.JSONDecodeError:
            return False
        return True

    @staticmethod
    def _is_code(content: str) -> bool:
        indicators = ("def ", "class ", "function ", "fn ", "import ", "#include", "package ")
        lines = content.splitlines()[:20]
        return sum(1 for line in lines if any(token in line for token in indicators)) >= 2

    @staticmethod
    def _is_table(content: str) -> bool:
        lines = [line for line in content.splitlines() if line.strip()][:4]
        return len(lines) >= 3 and (
            all("|" in line for line in lines[:3])
            or all(len(line.split()) >= 3 for line in lines[:3])
        )

    @staticmethod
    def _is_diff(content: str) -> bool:
        return any(marker in content for marker in ("diff --git", "--- ", "+++ ", "@@ -"))

    @staticmethod
    def _is_log(content: str) -> bool:
        patterns = [
            r"\d{4}-\d{2}-\d{2}",
            r"\[(INFO|WARN|ERROR|DEBUG)\]",
            r"\b(INFO|WARN|ERROR|DEBUG)\b",
            r"Traceback",
        ]
        return sum(1 for pattern in patterns if re.search(pattern, content)) >= 2

    @staticmethod
    def _is_error(content: str) -> bool:
        return bool(re.search(r"error|failed|assertion|panic|exception", content, re.IGNORECASE))

    @staticmethod
    def _is_tree(content: str) -> bool:
        return any(marker in content for marker in ("├──", "└──", "\n  "))

    @staticmethod
    def _is_list(content: str) -> bool:
        lines = content.splitlines()[:10]
        return sum(1 for line in lines if re.match(r"^\s*(?:[-*+]|\d+\.|\[.\])\s+", line)) >= 3

    @staticmethod
    def _list_budget(items: list[Any], max_chars: int) -> int:
        if not items:
            return 0
        average = max(1, sum(len(str(item)) for item in items[:20]) // min(len(items), 20))
        return max(1, min(len(items), max_chars // average))

    def _cache_key(
        self,
        serialized: str,
        action_type: str,
        context: dict[str, Any],
        config: OptimizationConfig,
    ) -> str:
        config_text = f"{config.enabled}:{config.level}:{config.max_tokens}"
        raw = f"{action_type}\0{context}\0{config_text}\0{serialized}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


__all__ = [
    "ContentType",
    "OptimizationConfig",
    "OptimizationResult",
    "TokenOptimizer",
    "compact_json_text",
]
