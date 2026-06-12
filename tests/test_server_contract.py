from pathlib import Path

from ai_agent_standards_mcp.catalog import build_catalog
from ai_agent_standards_mcp import server
from ai_agent_standards_mcp.server import register_handlers


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_BRANDING = ("a" + "wf", "anti" + "gravity")


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
        "export_project_snapshot",
        "get_project_tree",
        "read_project_file",
        "search_project_code",
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
    project_tree = mcp.tools["get_project_tree"](str(ROOT), max_depth=1)
    prompt = mcp.prompts["apply_standards"]("Build a secure API with tests")

    assert "# Karpathy Coding Principles" in document
    assert "# Codebase Onboarding" in skill
    assert any("security" in item["path"].lower() for item in recommendations["recommendations"])
    assert any(entry["path"] == "README.md" for entry in project_tree["tree"])
    assert "Apply AI-Coding-Standards v3.1.0" in prompt


def test_mcp_prompt_docs_and_catalog_metadata_do_not_expose_legacy_branding():
    catalog = build_catalog(ROOT)
    mcp = FakeMCP()

    register_handlers(mcp, catalog)

    prompt_docs = "\n".join(func.__doc__ or "" for func in mcp.prompts.values()).lower()
    catalog_metadata = "\n".join(
        " ".join(
            [
                entry["identifier"],
                entry["title"],
                entry["path"],
                entry["kind"],
                entry["category"],
                entry["description"],
            ]
        )
        for entry in catalog.list_entries()
    ).lower()

    for forbidden in FORBIDDEN_BRANDING:
        assert forbidden not in prompt_docs
        assert forbidden not in catalog_metadata


def test_create_server_initialization(monkeypatch):
    monkeypatch.setattr(server, "FastMCP", FakeFastMCP)

    mcp = server.create_server(ROOT)

    assert mcp.name == "AI Agent Standards"
    assert mcp.kwargs["json_response"] is True


def test_prompts_can_be_called_without_arguments():
    catalog = build_catalog(ROOT)
    mcp = FakeMCP()
    register_handlers(mcp, catalog)

    # These prompts previously had required arguments with no defaults.
    # We verify they can now be executed without parameters.
    assert "Apply AI-Coding-Standards" in mcp.prompts["apply_standards"]()
    assert mcp.prompts["plan"]() is not None
    assert mcp.prompts["design"]() is not None
    assert mcp.prompts["code"]() is not None
    assert mcp.prompts["debug"]() is not None
    assert mcp.prompts["refactor"]() is not None

