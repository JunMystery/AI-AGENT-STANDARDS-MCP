"""Repository discovery and content-path helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from .constants import DEFAULT_INCLUDE_DIRS, SKIP_PARTS, TEXT_SUFFIXES
from .text import normalize_identifier


def find_standards_root(root: str | Path | None = None) -> Path:
    candidates: list[Path] = []
    if root:
        candidates.append(Path(root))
    if os.environ.get("AI_AGENT_STANDARDS_ROOT"):
        candidates.append(Path(os.environ["AI_AGENT_STANDARDS_ROOT"]))

    here = Path(__file__).resolve()
    candidates.append(here.parent / "bundled")
    candidates.extend(parent for parent in here.parents)
    candidates.extend(parent.parent for parent in here.parents if parent.parent != parent)

    for candidate in candidates:
        resolved = candidate.resolve()
        if is_standards_root(resolved):
            return resolved

    raise FileNotFoundError(
        "Could not find AI-Agent-Standards root. Set AI_AGENT_STANDARDS_ROOT or pass --root."
    )


def is_standards_root(path: Path) -> bool:
    return (
        (path / "karpathy" / "principles.md").is_file()
        and (path / "SKILL-REFERENCE.md").is_file()
        and (path / "ai-agent-standards" / "INDEX.md").is_file()
    )


def iter_content_files(root: Path) -> Iterable[str]:
    root_files = ("README.md", "SKILL-REFERENCE.md", "PROJECT-STANDARDS.md")
    for name in root_files:
        if (root / name).is_file():
            yield name

    for directory in DEFAULT_INCLUDE_DIRS:
        base = root / directory
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            yield path.relative_to(root).as_posix()


def infer_kind(relative_path: str) -> str:
    parts = Path(relative_path).parts
    if parts and parts[0] == "skills" and relative_path.endswith("SKILL.md"):
        return "skill"
    if parts and parts[0] == "docs":
        return "doc"
    if parts and parts[0] == "karpathy":
        return "principle"
    if parts and parts[0] == "ai-agent-standards":
        return "standard"
    return "root"


def infer_category(relative_path: str) -> str:
    parts = Path(relative_path).parts
    if not parts:
        return "root"
    if parts[0] == "ai-agent-standards" and len(parts) > 1:
        return parts[1]
    if parts[0] == "skills" and len(parts) > 1:
        return "skills"
    if parts[0] in {"karpathy", "docs"}:
        return parts[0]
    return "root"


def identifier_for(relative_path: str, kind: str) -> str:
    path = Path(relative_path)
    if kind == "skill" and len(path.parts) >= 2:
        return normalize_identifier(path.parts[1])

    stem_path = relative_path
    for suffix in TEXT_SUFFIXES:
        if stem_path.lower().endswith(suffix):
            stem_path = stem_path[: -len(suffix)]
            break
    return normalize_identifier(stem_path)


def resolve_inside_root(root: Path, relative_path: str) -> Path:
    path = (root / relative_path).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"Path escapes standards root: {relative_path!r}") from exc
    if not path.is_file():
        raise FileNotFoundError(relative_path)
    return path
