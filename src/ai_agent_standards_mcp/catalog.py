"""Catalog and search logic for AI Agent Coding Standards content."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .constants import TASK_ANCHORS
from .paths import (
    find_standards_root,
    identifier_for,
    infer_category,
    infer_kind,
    iter_content_files,
    resolve_inside_root,
)
from .text import (
    extract_description,
    extract_title,
    infer_task_keywords,
    make_recommendation_reason,
    make_snippet,
    normalize_identifier,
    title_from_path,
    tokenize,
)


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

        def add_recommendation(identifier: str, reason: str) -> bool:
            try:
                entry = self.get_entry(identifier)
            except KeyError:
                return False
            if entry.identifier in seen:
                return False
            selected.append({**entry.to_dict(), "reason": reason})
            seen.add(entry.identifier)
            return True

        for identifier in essentials:
            add_recommendation(identifier, "Core operating context")

        for keyword in keywords:
            for identifier in TASK_ANCHORS.get(keyword, ()):
                if add_recommendation(identifier, f"Task-specific {keyword} reference"):
                    break
            if len(selected) >= limit:
                break

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

    return StandardsCatalog(standards_root, entries)


def make_entry(root: Path, relative_path: str) -> CatalogEntry | None:
    path = root / relative_path
    content = path.read_text(encoding="utf-8")
    title = extract_title(content) or title_from_path(relative_path)
    description = extract_description(content)
    kind = infer_kind(relative_path)
    category = infer_category(relative_path)
    identifier = identifier_for(relative_path, kind)
    return CatalogEntry(identifier, title, relative_path, kind, category, description)
