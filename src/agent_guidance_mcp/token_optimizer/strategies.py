"""Safe optimization strategies used by the RTK core."""

from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any


class SemanticCompression:
    """Semantic compression for opt-in text/log/error content only."""

    def compress(self, content: str, content_type: str, max_chars: int) -> tuple[str, dict[str, Any]]:
        original_len = len(content)
        if content_type not in {"text", "log", "error"}:
            return content, {"saved_chars": 0}

        compact = re.sub(r"\n\s*\n\s*\n+", "\n\n", content)
        if content_type in {"log", "error"}:
            compact = self._summarize_repeated_errors(compact)

        if len(compact) > max_chars:
            compact, metadata = AdaptiveTruncation().truncate(compact, content_type, max_chars)
            metadata["semantic_saved_chars"] = original_len - len(compact)
            return compact, metadata

        return compact, {"saved_chars": max(0, original_len - len(compact))}

    def _summarize_repeated_errors(self, content: str) -> str:
        lines = content.splitlines()
        signatures: Counter[str] = Counter()
        kept: list[str] = []

        for line in lines:
            if re.search(r"error|exception|failed", line, re.IGNORECASE):
                signature = re.sub(r"\d+", "N", line)
                signatures[signature] += 1
                if signatures[signature] <= 3:
                    kept.append(line)
            else:
                kept.append(line)

        omitted = sum(count - 3 for count in signatures.values() if count > 3)
        if omitted:
            kept.append(f"[RTK: {omitted} similar error lines collapsed]")
        return "\n".join(kept)


class StructuralGrouping:
    """Group generated tree/list/table content while preserving original schema."""

    def compact_entries(
        self, entries: list[Any], max_items: int
    ) -> tuple[list[Any], dict[str, Any]]:
        if len(entries) <= max_items:
            return entries, {"omitted_count": 0}
        kept = entries[:max_items]
        return kept, {"omitted_count": len(entries) - len(kept)}

    def summarize_tree(self, entries: list[dict[str, Any]]) -> dict[str, Any]:
        summary: dict[str, dict[str, int]] = {}
        for entry in entries:
            path = str(entry.get("path", ""))
            top = path.split("/", 1)[0] if path else "."
            bucket = summary.setdefault(top, {"files": 0, "directories": 0})
            if entry.get("type") == "directory":
                bucket["directories"] += 1
            else:
                bucket["files"] += 1
        return summary

    def group_text(self, content: str, content_type: str, max_chars: int) -> tuple[str, dict[str, Any]]:
        if len(content) <= max_chars:
            return content, {"omitted_count": 0}

        lines = content.splitlines()
        if content_type == "table" and len(lines) > 12:
            kept = lines[:6] + [f"[RTK: {len(lines) - 10} rows omitted]"] + lines[-4:]
            return "\n".join(kept), {"omitted_count": len(lines) - 10}

        return AdaptiveTruncation().truncate(content, content_type, max_chars)


class AdaptiveTruncation:
    """Truncate text with explicit markers and no silent removal."""

    def truncate(self, content: str, content_type: str, max_chars: int) -> tuple[str, dict[str, Any]]:
        if len(content) <= max_chars:
            return content, {"omitted_chars": 0, "omitted_lines": 0}

        lines = content.splitlines()
        if content_type in {"code", "diff", "error", "log"}:
            return self._truncate_by_lines(lines, max_chars)
        return self._truncate_head_tail(content, max_chars)

    def _truncate_by_lines(self, lines: list[str], max_chars: int) -> tuple[str, dict[str, Any]]:
        kept: list[str] = []
        used = 0
        for line in lines:
            needed = len(line) + 1
            if kept and used + needed > max_chars:
                break
            kept.append(line)
            used += needed

        omitted_lines = max(0, len(lines) - len(kept))
        if omitted_lines:
            kept.append(f"[RTK: {omitted_lines} more lines available]")
        return "\n".join(kept), {
            "omitted_lines": omitted_lines,
            "omitted_chars": max(0, sum(len(line) + 1 for line in lines) - used),
        }

    def _truncate_head_tail(self, content: str, max_chars: int) -> tuple[str, dict[str, Any]]:
        head_size = max(1, int(max_chars * 0.7))
        tail_size = max(0, max_chars - head_size)
        omitted = len(content) - max_chars
        marker = f"\n[RTK: {omitted} chars omitted]\n"
        compact = content[:head_size] + marker + (content[-tail_size:] if tail_size else "")
        return compact, {"omitted_chars": omitted, "omitted_lines": 0}


class PatternDeduplication:
    """Collapse repeated lines with explicit counts."""

    def deduplicate(self, content: str, content_type: str) -> tuple[str, dict[str, Any]]:
        lines = content.splitlines()
        if len(lines) < 5 or content_type not in {"text", "log", "error"}:
            return content, {"collapsed_count": 0}

        result: list[str] = []
        collapsed_count = 0
        previous: str | None = None
        count = 0

        def flush() -> None:
            nonlocal collapsed_count
            if previous is None:
                return
            if count > 1:
                result.append(f"[{count}x] {previous}")
                collapsed_count += count - 1
            else:
                result.append(previous)

        for line in lines:
            if line == previous:
                count += 1
                continue
            flush()
            previous = line
            count = 1
        flush()

        return "\n".join(result), {"collapsed_count": collapsed_count}


def compact_json_text(content: str, max_items: int = 20) -> tuple[str, dict[str, Any]]:
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return content, {"omitted_count": 0}

    if isinstance(data, list) and len(data) > max_items:
        compact = {
            "items": data[:max_items],
            "_rtk_omitted_count": len(data) - max_items,
            "_rtk_total_items": len(data),
        }
        return json.dumps(compact, indent=2), {"omitted_count": len(data) - max_items}

    if isinstance(data, dict) and len(data) > max_items:
        kept = dict(list(data.items())[:max_items])
        kept["_rtk_omitted_count"] = len(data) - max_items
        kept["_rtk_total_keys"] = len(data)
        return json.dumps(kept, indent=2), {"omitted_count": len(data) - max_items}

    return content, {"omitted_count": 0}
