"""Text extraction, normalization, and task keyword helpers."""

from __future__ import annotations

import re
from pathlib import Path


TASK_KEYWORD_TRIGGERS = {
    "tests": {"test", "tests", "pytest", "unit", "coverage", "tdd"},
    "security": {
        "security",
        "secure",
        "auth",
        "secret",
        "secrets",
        "token",
        "password",
        "owasp",
        "audit",
    },
    "api": {"api", "endpoint", "rest", "schema", "request", "response", "mcp"},
    "docs": {"docs", "readme", "documentation", "changelog"},
    "accessibility": {"a11y", "accessibility", "wcag", "aria", "keyboard"},
    "performance": {"performance", "cache", "latency", "database", "query"},
    "release": {"release", "semver", "version", "ci", "workflow"},
    "skills": {"skill", "skills", "capsule", "workflow"},
    "review": {"review", "audit", "checklist", "quality"},
}


def normalize_identifier(value: str) -> str:
    cleaned = value.strip().replace("\\", "/")
    cleaned = cleaned.removeprefix("standards://document/")
    cleaned = cleaned.removeprefix("standards://skill/")
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


def infer_task_keywords(task: str) -> list[str]:
    task_terms = set(tokenize(task))
    keywords: list[str] = []
    for label, triggers in TASK_KEYWORD_TRIGGERS.items():
        if task_terms & triggers:
            keywords.extend([label, *sorted(triggers & task_terms)])

    return list(dict.fromkeys(keywords))


def make_recommendation_reason(result: dict[str, object], keywords: list[str]) -> str:
    matched = [keyword for keyword in keywords if keyword in str(result).lower()]
    if matched:
        return f"Matches task signal: {', '.join(matched[:3])}"
    return "Keyword match in standards corpus"
