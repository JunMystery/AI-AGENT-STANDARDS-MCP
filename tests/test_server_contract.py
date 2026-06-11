from pathlib import Path

from ai_agent_standards_mcp.catalog import build_catalog
from ai_agent_standards_mcp import server
from ai_agent_standards_mcp.server import register_handlers


ROOT = Path(__file__).resolve().parents[1]


class FakeMCP:
    def __init__(self):
        self.resources = {}
        self.tools = {}
        self.prompts = {}

    def resource(self, uri, mime_type=None):
        def decorator(func):
            self.resources[uri] = {"func": func, "mime_type": mime_type}
            return func

        return decorator

    def tool(self):
        def decorator(func):
            self.tools[func.__name__] = func
            return func

        return decorator

    def prompt(self):
        def decorator(func):
            self.prompts[func.__name__] = func
            return func

        return decorator


class FakeFastMCP(FakeMCP):
    def __init__(self, name, **kwargs):
        super().__init__()
        self.name = name
        self.kwargs = kwargs


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


def test_register_handlers_exposes_expected_mcp_contract():
    catalog = build_catalog(ROOT)
    mcp = FakeMCP()

    register_handlers(mcp, catalog)

    assert set(mcp.resources) == {
        "standards://manifest",
        "standards://document/{identifier}",
        "standards://skill/{name}",
    }
    assert set(mcp.tools) == {
        "list_entries",
        "get_entry",
        "search_entries",
        "recommend_context",
    }
    assert set(mcp.prompts) == {
        "apply_standards",
        "review_ai_code",
        "init",
        "plan",
        "design",
        "visualize",
        "code",
        "run",
        "test",
        "deploy",
        "debug",
        "refactor",
        "audit",
        "rollback",
        "recap",
    }

    document = mcp.resources["standards://document/{identifier}"]["func"]("karpathy-principles")
    skill = mcp.resources["standards://skill/{name}"]["func"]("codebase-onboarding")
    recommendations = mcp.tools["recommend_context"]("Build a secure API with tests", limit=6)
    prompt = mcp.prompts["apply_standards"]("Build a secure API with tests")

    assert "# Karpathy Coding Principles" in document
    assert "# Codebase Onboarding" in skill
    assert any("security" in item["path"].lower() for item in recommendations["recommendations"])
    assert "Apply AI-Coding-Standards v3.0.2" in prompt


def test_create_server_passes_http_host_and_port(monkeypatch):
    monkeypatch.setattr(server, "FastMCP", FakeFastMCP)

    mcp = server.create_server(ROOT, host="0.0.0.0", port=9001)

    assert mcp.name == "AI Agent Standards"
    assert mcp.kwargs["host"] == "0.0.0.0"
    assert mcp.kwargs["port"] == 9001
    assert mcp.kwargs["json_response"] is True
