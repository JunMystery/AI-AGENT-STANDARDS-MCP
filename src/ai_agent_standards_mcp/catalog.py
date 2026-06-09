"""Catalog and search logic for AI Agent Coding Standards content."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {".md", ".mdc", ".txt", ".yaml", ".yml", ".json"}
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "node_modules"}
DEFAULT_INCLUDE_DIRS = ("karpathy", "ai-agent-standards", "skills", "docs")
AGENT_FILES = {
    "codex": "AGENTS.md",
    "claude": "CLAUDE.md",
    "gemini": "GEMINI.md",
    "copilot": "COPILOT.md",
    "vscode-copilot": ".instructions.md",
    "cursor": ".cursor/rules/karpathy-guidelines.mdc",
    "windsurf": ".cursorrules",
}


@dataclass(frozen=True)
class CatalogEntry:
    identifier: str
    title: str
    path: str
    kind: str
    category: str
    description: str = ""

    @property
    def uri(self) -> str:
        if self.kind == "skill":
            return f"standards://skill/{self.identifier}"
        if self.kind == "agent":
            return f"standards://agent/{self.identifier}"
        return f"standards://document/{self.identifier}"

    def to_dict(self) -> dict[str, str]:
        return {
            "identifier": self.identifier,
            "title": self.title,
            "path": self.path,
            "kind": self.kind,
            "category": self.category,
            "description": self.description,
            "uri": self.uri,
        }


class StandardsCatalog:
    def __init__(self, root: Path, entries: Iterable[CatalogEntry]):
        self.root = root
        self.entries = sorted(entries, key=lambda entry: (entry.kind, entry.path))
        self._by_identifier = {entry.identifier: entry for entry in self.entries}
        self._by_path = {entry.path.replace("\\", "/").lower(): entry for entry in self.entries}

    def list_entries(
        self, category: str | None = None, kind: str | None = None
    ) -> list[dict[str, str]]:
        entries = self.entries
        if category:
            category_key = category.lower()
            entries = [entry for entry in entries if entry.category.lower() == category_key]
        if kind:
            kind_key = kind.lower()
            entries = [entry for entry in entries if entry.kind.lower() == kind_key]
        return [entry.to_dict() for entry in entries]

    def get_entry(self, identifier: str) -> CatalogEntry:
        key = normalize_identifier(identifier)
        if key in self._by_identifier:
            return self._by_identifier[key]

        path_key = identifier.replace("\\", "/").lower().strip("/")
        if path_key in self._by_path:
            return self._by_path[path_key]

        raise KeyError(f"No standards entry found for {identifier!r}.")

    def read_entry(self, identifier: str) -> str:
        entry = self.get_entry(identifier)
        return self.read_path(entry.path)

    def read_path(self, relative_path: str) -> str:
        path = resolve_inside_root(self.root, relative_path)
        return path.read_text(encoding="utf-8")

    def manifest(self) -> dict[str, object]:
        kinds: dict[str, int] = {}
        categories: dict[str, int] = {}
        for entry in self.entries:
            kinds[entry.kind] = kinds.get(entry.kind, 0) + 1
            categories[entry.category] = categories.get(entry.category, 0) + 1

        return {
            "name": "AI Agent Coding Standards",
            "root": str(self.root),
            "entry_count": len(self.entries),
            "kinds": dict(sorted(kinds.items())),
            "categories": dict(sorted(categories.items())),
            "entries": [entry.to_dict() for entry in self.entries],
        }

    def manifest_json(self) -> str:
        return json.dumps(self.manifest(), indent=2, sort_keys=True)

    def search_entries(
        self, query: str, limit: int = 10, kind: str | None = None
    ) -> list[dict[str, object]]:
        terms = tokenize(query)
        if not terms:
            return []

        results: list[tuple[int, CatalogEntry, str]] = []
        for entry in self.entries:
            if kind and entry.kind.lower() != kind.lower():
                continue

            content = self.read_path(entry.path)
            haystack = " ".join(
                [entry.title, entry.description, entry.category, entry.path, content]
            ).lower()
            score = sum(haystack.count(term) for term in terms)
            if score:
                results.append((score, entry, make_snippet(content, terms)))

        results.sort(key=lambda result: (-result[0], result[1].path))
        return [
            {
                **entry.to_dict(),
                "score": score,
                "snippet": snippet,
            }
            for score, entry, snippet in results[: max(1, limit)]
        ]

    def recommend_context(self, task: str, limit: int = 8) -> dict[str, object]:
        keywords = infer_task_keywords(task)
        weighted_query = " ".join([task, *keywords, *keywords])
        results = self.search_entries(weighted_query, limit=max(limit * 2, limit))

        essentials = [
            "karpathy-principles",
            "skill-reference",
            "repo-map-for-agents",
        ]
        selected: list[dict[str, object]] = []
        seen: set[str] = set()
        for identifier in essentials:
            try:
                entry = self.get_entry(identifier)
            except KeyError:
                continue
            selected.append({**entry.to_dict(), "reason": "Core operating context"})
            seen.add(entry.identifier)

        for result in results:
            identifier = str(result["identifier"])
            if identifier in seen:
                continue
            selected.append(
                {
                    key: value
                    for key, value in result.items()
                    if key not in {"score", "snippet"}
                }
                | {"reason": make_recommendation_reason(result, keywords)}
            )
            seen.add(identifier)
            if len(selected) >= limit:
                break

        return {
            "task": task,
            "keywords": keywords,
            "recommendations": selected[:limit],
        }


def build_catalog(root: str | Path | None = None) -> StandardsCatalog:
    standards_root = find_standards_root(root)
    entries: list[CatalogEntry] = []

    for relative in iter_content_files(standards_root):
        entry = make_entry(standards_root, relative)
        if entry is not None:
            entries.append(entry)

    for key, relative in AGENT_FILES.items():
        if (standards_root / relative).is_file():
            entries.append(
                CatalogEntry(
                    identifier=key,
                    title=agent_title(key),
                    path=relative,
                    kind="agent",
                    category="agent-instructions",
                    description="Generated agent instruction file.",
                )
            )

    return StandardsCatalog(standards_root, entries)


def find_standards_root(root: str | Path | None = None) -> Path:
    candidates: list[Path] = []
    if root:
        candidates.append(Path(root))
    if os.environ.get("AI_AGENT_STANDARDS_ROOT"):
        candidates.append(Path(os.environ["AI_AGENT_STANDARDS_ROOT"]))

    here = Path(__file__).resolve()
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
    root_files = ("README.md", "INSTALL.md", "PROJECT-STANDARDS.md", "SKILL-REFERENCE.md")
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


def make_entry(root: Path, relative_path: str) -> CatalogEntry | None:
    path = root / relative_path
    content = path.read_text(encoding="utf-8")
    title = extract_title(content) or title_from_path(relative_path)
    description = extract_description(content)
    kind = infer_kind(relative_path)
    category = infer_category(relative_path)
    identifier = identifier_for(relative_path, kind)
    return CatalogEntry(identifier, title, relative_path, kind, category, description)


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
    for suffix in (".md", ".mdc", ".txt", ".yaml", ".yml", ".json"):
        if stem_path.lower().endswith(suffix):
            stem_path = stem_path[: -len(suffix)]
            break
    return normalize_identifier(stem_path)


def normalize_identifier(value: str) -> str:
    cleaned = value.strip().replace("\\", "/")
    cleaned = cleaned.removeprefix("standards://document/")
    cleaned = cleaned.removeprefix("standards://skill/")
    cleaned = cleaned.removeprefix("standards://agent/")
    cleaned = cleaned.removesuffix("/SKILL.md")
    cleaned = cleaned.removesuffix(".md")
    cleaned = cleaned.removesuffix(".mdc")
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", cleaned)
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    return cleaned.lower()


def extract_title(content: str) -> str | None:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return None


def extract_description(content: str) -> str:
    lines = [line.strip() for line in content.splitlines()]
    in_frontmatter = lines[:1] == ["---"]
    description = ""
    if in_frontmatter:
        for line in lines[1:]:
            if line == "---":
                break
            if line.startswith("description:"):
                description = line.split(":", 1)[1].strip().strip('"')
                break
    if description:
        return description

    for line in lines:
        if not line or line.startswith("#") or line.startswith("---"):
            continue
        if line.startswith("**") and line.endswith("**"):
            continue
        return strip_markdown(line)[:220]
    return ""


def title_from_path(relative_path: str) -> str:
    stem = Path(relative_path).stem
    if stem.upper() == stem:
        return stem
    return stem.replace("-", " ").replace("_", " ").title()


def agent_title(key: str) -> str:
    return {
        "codex": "OpenAI Codex Instructions",
        "claude": "Claude Instructions",
        "gemini": "Gemini Instructions",
        "copilot": "GitHub Copilot Instructions",
        "vscode-copilot": "VS Code Copilot Instructions",
        "cursor": "Cursor Instructions",
        "windsurf": "Windsurf Instructions",
    }.get(key, key.replace("-", " ").title())


def tokenize(value: str) -> list[str]:
    return [term for term in re.findall(r"[a-zA-Z0-9][a-zA-Z0-9_-]{1,}", value.lower())]


def make_snippet(content: str, terms: list[str], radius: int = 140) -> str:
    lower = content.lower()
    positions = [lower.find(term) for term in terms if lower.find(term) >= 0]
    if not positions:
        return strip_markdown(content[: radius * 2]).strip()

    start = max(0, min(positions) - radius)
    end = min(len(content), min(positions) + radius)
    snippet = strip_markdown(content[start:end]).replace("\n", " ")
    return re.sub(r"\s+", " ", snippet).strip()


def strip_markdown(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("*", "").replace("_", "")
    return value.strip()


def resolve_inside_root(root: Path, relative_path: str) -> Path:
    path = (root / relative_path).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"Path escapes standards root: {relative_path!r}") from exc
    if not path.is_file():
        raise FileNotFoundError(relative_path)
    return path


def infer_task_keywords(task: str) -> list[str]:
    task_terms = set(tokenize(task))
    mapping = {
        "tests": {"test", "tests", "pytest", "unit", "coverage", "tdd"},
        "security": {"security", "auth", "secret", "token", "password", "owasp", "audit"},
        "api": {"api", "endpoint", "rest", "schema", "request", "response", "mcp"},
        "docs": {"docs", "readme", "documentation", "changelog"},
        "accessibility": {"a11y", "accessibility", "wcag", "aria", "keyboard"},
        "performance": {"performance", "cache", "latency", "database", "query"},
        "release": {"release", "semver", "version", "ci", "workflow"},
        "skills": {"skill", "skills", "capsule", "workflow"},
        "review": {"review", "audit", "checklist", "quality"},
    }

    keywords: list[str] = []
    for label, triggers in mapping.items():
        if task_terms & triggers:
            keywords.extend([label, *sorted(triggers & task_terms)])

    return list(dict.fromkeys(keywords))


def make_recommendation_reason(result: dict[str, object], keywords: list[str]) -> str:
    matched = [keyword for keyword in keywords if keyword in str(result).lower()]
    if matched:
        return f"Matches task signal: {', '.join(matched[:3])}"
    return "Keyword match in standards corpus"
