"""Environment-driven RTK optimization settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping


TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"0", "false", "no", "off"}
VALID_LEVELS = {"conservative", "balanced", "aggressive"}


def _env_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    return default


def _env_int(value: str | None, default: int, minimum: int = 1) -> int:
    if value is None:
        return default
    try:
        return max(minimum, int(value))
    except ValueError:
        return default


def _env_level(value: str | None, default: str = "conservative") -> str:
    normalized = (value or default).strip().lower()
    return normalized if normalized in VALID_LEVELS else default


@dataclass(frozen=True)
class OptimizationSettings:
    """Global optimization settings loaded from RTK_* environment variables."""

    enabled: bool = True
    level: str = "conservative"
    max_tokens: int = 12_000
    cache_ttl: int = 300
    cache_enabled: bool = True
    log_metrics: bool = False
    auto_detect: bool = True

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "OptimizationSettings":
        env = environ if environ is not None else os.environ
        return cls(
            enabled=_env_bool(env.get("RTK_OPTIMIZATION_ENABLED"), True),
            level=_env_level(env.get("RTK_OPTIMIZATION_LEVEL"), "conservative"),
            max_tokens=_env_int(env.get("RTK_MAX_TOKENS"), 12_000),
            cache_ttl=_env_int(env.get("RTK_CACHE_TTL"), 300),
            cache_enabled=_env_bool(env.get("RTK_CACHE_ENABLED"), True),
            log_metrics=_env_bool(env.get("RTK_LOG_METRICS"), False),
            auto_detect=_env_bool(env.get("RTK_AUTO_DETECT"), True),
        )

    def with_overrides(
        self,
        *,
        rtk_enabled: bool | None = None,
        rtk_level: str | None = None,
        rtk_max_tokens: Any | None = None,
    ) -> "OptimizationSettings":
        return OptimizationSettings(
            enabled=self.enabled if rtk_enabled is None else bool(rtk_enabled),
            level=self.level if rtk_level is None else _env_level(rtk_level, self.level),
            max_tokens=_env_int(
                None if rtk_max_tokens is None else str(rtk_max_tokens),
                self.max_tokens,
            ),
            cache_ttl=self.cache_ttl,
            cache_enabled=self.cache_enabled,
            log_metrics=self.log_metrics,
            auto_detect=self.auto_detect,
        )

    def to_config(self) -> "OptimizationConfig":
        from .core import OptimizationConfig

        aggressive = self.level == "aggressive"
        return OptimizationConfig(
            enabled=self.enabled,
            level=self.level,
            auto_detect_type=self.auto_detect,
            max_tokens=self.max_tokens,
            preserve_structure=not aggressive,
            aggressive_mode=aggressive,
            cache_enabled=self.cache_enabled,
            cache_ttl=self.cache_ttl,
            log_metrics=self.log_metrics,
        )
