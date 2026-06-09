from pathlib import Path

from ai_agent_standards_mcp.catalog import build_catalog


ROOT = Path(__file__).resolve().parents[2]


def test_manifest_resource_payload_is_json_text():
    catalog = build_catalog(ROOT)

    payload = catalog.manifest_json()

    assert '"name": "AI Agent Coding Standards"' in payload
    assert '"entries": [' in payload


def test_prompt_recommendation_has_loadable_paths():
    catalog = build_catalog(ROOT)

    recommendation = catalog.recommend_context("Review generated code for security", limit=5)

    for item in recommendation["recommendations"]:
        assert (ROOT / item["path"]).is_file()
