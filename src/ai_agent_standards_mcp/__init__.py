"""MCP server package for AI Agent Coding Standards."""

from .catalog import CatalogEntry, StandardsCatalog, build_catalog, find_standards_root

__all__ = [
    "CatalogEntry",
    "StandardsCatalog",
    "build_catalog",
    "find_standards_root",
]
