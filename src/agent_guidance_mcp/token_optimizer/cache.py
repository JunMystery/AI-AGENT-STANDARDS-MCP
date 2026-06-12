"""Small in-memory TTL cache for optimized responses."""

from __future__ import annotations

from dataclasses import replace
from time import monotonic
from typing import Generic, TypeVar

T = TypeVar("T")


class OptimizedCache(Generic[T]):
    """Cache optimized results only for the lifetime of one server process."""

    def __init__(self, ttl_seconds: int = 300) -> None:
        self.ttl_seconds = max(1, ttl_seconds)
        self._items: dict[str, tuple[float, T]] = {}
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> T | None:
        now = monotonic()
        item = self._items.get(key)
        if item is None:
            self.misses += 1
            return None

        expires_at, value = item
        if expires_at <= now:
            self._items.pop(key, None)
            self.misses += 1
            return None

        self.hits += 1
        try:
            return replace(value, cache_hit=True)  # type: ignore[arg-type]
        except TypeError:
            return value

    def set(self, key: str, value: T) -> None:
        self._items[key] = (monotonic() + self.ttl_seconds, value)

    def clear(self) -> None:
        self._items.clear()
        self.hits = 0
        self.misses = 0

    def stats(self) -> dict[str, int]:
        return {
            "entries": len(self._items),
            "hits": self.hits,
            "misses": self.misses,
            "ttl_seconds": self.ttl_seconds,
        }
