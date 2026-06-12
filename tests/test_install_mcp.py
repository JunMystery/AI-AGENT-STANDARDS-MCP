from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path


def load_installer():
    script = Path(__file__).resolve().parents[1] / "scripts" / "install-mcp.py"
    spec = importlib.util.spec_from_file_location("install_mcp", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def local_tmp(name: str) -> Path:
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name)
    root = Path(__file__).resolve().parent / ".tmp_install_mcp" / safe_name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    return root


def test_json_merge_preserves_unrelated_servers_and_custom_env():
    installer = load_installer()
    config = {
        "mcpServers": {
            "other": {"command": "node", "args": ["server.js"]},
            installer.SERVER_ID: {
                "command": "old",
                "args": ["-m", installer.MODULE_NAME],
                "env": {"CUSTOM": "keep", "PYTHONPATH": "old-src"},
            },
        },
        "theme": "dark",
    }

    merged, notes, warnings = installer.merge_json_config(
        config, "mcpServers", "python", "new-src"
    )

    server = merged["mcpServers"][installer.SERVER_ID]
    assert server["command"] == "python"
    assert server["args"] == ["-m", installer.MODULE_NAME]
    assert server["env"] == {"CUSTOM": "keep", "PYTHONPATH": "new-src"}
    assert merged["mcpServers"]["other"] == {"command": "node", "args": ["server.js"]}
    assert merged["theme"] == "dark"
    assert notes == []
    assert warnings == []


def test_json_merge_migrates_legacy_and_removes_stale_owned_duplicates():
    installer = load_installer()
    config = {
        "mcpServers": {
            installer.LEGACY_SERVER_ID: {
                "command": "old",
                "args": ["-m", installer.LEGACY_MODULE_NAME],
                "env": {"EXTRA": "keep"},
            },
            "renamed-copy": {
                "command": "old",
                "args": ["-m", installer.MODULE_NAME],
            },
            "custom": {"command": "custom", "args": ["run"]},
        }
    }

    merged, notes, warnings = installer.merge_json_config(
        config, "mcpServers", "python", "src"
    )

    servers = merged["mcpServers"]
    assert installer.SERVER_ID in servers
    assert installer.LEGACY_SERVER_ID not in servers
    assert "renamed-copy" not in servers
    assert "custom" in servers
    assert servers[installer.SERVER_ID]["env"] == {"EXTRA": "keep", "PYTHONPATH": "src"}
    assert notes == [
        "migrated legacy 'ai-agent-standards-mcp' to 'agent-guidance-mcp'",
        "removed stale owned server 'renamed-copy'",
    ]
    assert warnings == []


def test_json_merge_leaves_custom_legacy_block_unchanged():
    installer = load_installer()
    config = {
        "mcpServers": {
            installer.LEGACY_SERVER_ID: {"command": "custom", "args": ["run"]},
        }
    }

    merged, _notes, warnings = installer.merge_json_config(
        config, "mcpServers", "python", "src"
    )

    assert installer.LEGACY_SERVER_ID in merged["mcpServers"]
    assert installer.SERVER_ID in merged["mcpServers"]
    assert warnings == ["left custom legacy 'ai-agent-standards-mcp' unchanged"]


def test_invalid_json_is_backed_up_and_replaced():
    installer = load_installer()
    tmp_path = local_tmp("invalid_json")
    config_path = tmp_path / "mcp.json"
    config_path.write_text("{bad json", encoding="utf-8")
    report = installer.InstallReport()

    installer.configure_json_target(
        "Test MCP",
        config_path,
        "mcpServers",
        "python",
        "src",
        options=installer.InstallOptions(),
        report=report,
        timestamp="20260612010203",
    )

    assert (tmp_path / "mcp.json.bak.20260612010203").read_text(encoding="utf-8") == "{bad json"
    data = json.loads(config_path.read_text(encoding="utf-8"))
    assert data["mcpServers"][installer.SERVER_ID]["command"] == "python"
    assert report.warnings
    assert report.backups == [str(tmp_path / "mcp.json.bak.20260612010203")]


def test_dry_run_does_not_write_json_config():
    installer = load_installer()
    tmp_path = local_tmp("dry_run")
    config_path = tmp_path / "mcp.json"
    report = installer.InstallReport()

    installer.configure_json_target(
        "Dry MCP",
        config_path,
        "mcpServers",
        "python",
        "src",
        options=installer.InstallOptions(dry_run=True),
        report=report,
        timestamp="20260612010203",
    )

    assert not config_path.exists()
    assert report.changed == ["Dry MCP (dry-run)"]


def test_json_config_update_is_idempotent():
    installer = load_installer()
    tmp_path = local_tmp("idempotent")
    config_path = tmp_path / "mcp.json"
    report = installer.InstallReport()
    options = installer.InstallOptions()

    for _ in range(2):
        installer.configure_json_target(
            "Idempotent MCP",
            config_path,
            "mcpServers",
            "python",
            "src",
            options=options,
            report=report,
            timestamp="20260612010203",
        )

    assert report.changed == ["Idempotent MCP"]
    assert report.unchanged == ["Idempotent MCP"]
    assert not list(tmp_path.glob("*.bak.*"))


def test_codex_toml_replaces_owned_blocks_and_preserves_unrelated():
    installer = load_installer()
    content = "\n".join(
        [
            "[general]",
            'model = "gpt"',
            "",
            "[mcp_servers.custom]",
            'command = "node"',
            "",
            f"[mcp_servers.{installer.LEGACY_SERVER_ID}]",
            'command = "old"',
            f'args = ["-m", "{installer.LEGACY_MODULE_NAME}"]',
            "",
            "[mcp_servers.renamed]",
            'command = "old"',
            f'args = ["-m", "{installer.MODULE_NAME}"]',
        ]
    )

    merged, notes = installer.merge_codex_toml(content, "python", "src")

    assert "[general]" in merged
    assert "[mcp_servers.custom]" in merged
    assert f"[mcp_servers.{installer.SERVER_ID}]" in merged
    assert f"[mcp_servers.{installer.LEGACY_SERVER_ID}]" not in merged
    assert "[mcp_servers.renamed]" not in merged
    assert notes == [
        "removed stale owned server 'ai-agent-standards-mcp'",
        "removed stale owned server 'renamed'",
    ]


def test_codex_invalid_toml_is_backed_up_and_replaced():
    installer = load_installer()
    tmp_path = local_tmp("invalid_toml")
    config_path = tmp_path / "config.toml"
    config_path.write_text("[broken\n", encoding="utf-8")
    report = installer.InstallReport()

    installer.configure_codex_target(
        "Codex",
        config_path,
        "python",
        "src",
        options=installer.InstallOptions(),
        report=report,
        timestamp="20260612010203",
    )

    assert (tmp_path / "config.toml.bak.20260612010203").read_text(encoding="utf-8") == "[broken\n"
    assert f"[mcp_servers.{installer.SERVER_ID}]" in config_path.read_text(encoding="utf-8")
    assert report.warnings
    assert report.backups == [str(tmp_path / "config.toml.bak.20260612010203")]
