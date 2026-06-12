#!/usr/bin/env python3
"""Install or refresh Agent Guidance MCP client configuration."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:  # pragma: no cover - Python < 3.11 fallback.
    tomllib = None


SERVER_ID = "agent-guidance-mcp"
LEGACY_SERVER_ID = "ai-agent-standards-mcp"
MODULE_NAME = "agent_guidance_mcp"
LEGACY_MODULE_NAME = "ai_agent_standards_mcp"
OWNED_MODULES = (MODULE_NAME, LEGACY_MODULE_NAME)


@dataclass
class InstallReport:
    changed: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    backups: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    migrations: list[str] = field(default_factory=list)

    def print_summary(self) -> None:
        print("\nInstall report:")
        for label, values in (
            ("Changed", self.changed),
            ("Unchanged", self.unchanged),
            ("Backups", self.backups),
            ("Migrations", self.migrations),
            ("Warnings", self.warnings),
            ("Errors", self.errors),
        ):
            if values:
                print(f"  {label}:")
                for value in values:
                    print(f"    - {value}")


@dataclass(frozen=True)
class InstallOptions:
    dry_run: bool = False
    skip_install: bool = False
    backup: bool = True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install or refresh Agent Guidance MCP.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned changes without creating venv, installing packages, or writing configs.",
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Update MCP client configs without running pip install -e .",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create .bak.<timestamp> files before changing existing configs.",
    )
    return parser.parse_args()


def owns_json_server_config(server_config: Any) -> bool:
    if not isinstance(server_config, dict):
        return False
    args = server_config.get("args", [])
    return isinstance(args, list) and any(module in args for module in OWNED_MODULES)


def build_json_server_config(
    existing: Any,
    command: str,
    pythonpath: str,
) -> dict[str, Any]:
    env = {}
    if isinstance(existing, dict) and isinstance(existing.get("env"), dict):
        env.update(existing["env"])
    env["PYTHONPATH"] = pythonpath
    return {
        "command": command,
        "args": ["-m", MODULE_NAME],
        "env": env,
    }


def merge_json_config(
    config: Any,
    config_key: str,
    command: str,
    pythonpath: str,
) -> tuple[dict[str, Any], list[str], list[str]]:
    if not isinstance(config, dict):
        config = {}
    merged = dict(config)
    servers = merged.get(config_key)
    if not isinstance(servers, dict):
        servers = {}
    servers = dict(servers)

    notes: list[str] = []
    warnings: list[str] = []
    canonical_existing = servers.get(SERVER_ID)

    for server_id, server_config in list(servers.items()):
        if server_id == SERVER_ID:
            continue
        if server_id == LEGACY_SERVER_ID:
            if owns_json_server_config(server_config):
                servers.pop(server_id)
                notes.append(f"migrated legacy '{LEGACY_SERVER_ID}' to '{SERVER_ID}'")
                if canonical_existing is None:
                    canonical_existing = server_config
            else:
                warnings.append(f"left custom legacy '{LEGACY_SERVER_ID}' unchanged")
            continue
        if owns_json_server_config(server_config):
            servers.pop(server_id)
            notes.append(f"removed stale owned server '{server_id}'")
            if canonical_existing is None:
                canonical_existing = server_config

    servers[SERVER_ID] = build_json_server_config(canonical_existing, command, pythonpath)
    merged[config_key] = servers
    return merged, notes, warnings


def json_text(config: dict[str, Any]) -> str:
    return json.dumps(config, indent=2, sort_keys=False) + "\n"


def backup_path_for(path: Path, timestamp: str) -> Path:
    return path.with_name(f"{path.name}.bak.{timestamp}")


def write_if_changed(
    path: Path,
    content: str,
    *,
    options: InstallOptions,
    report: InstallReport,
    timestamp: str,
    label: str,
    backup_existing: bool = True,
) -> None:
    old_content = path.read_text(encoding="utf-8") if path.exists() else None
    if old_content == content:
        report.unchanged.append(label)
        print("    Unchanged.")
        return

    if options.dry_run:
        report.changed.append(f"{label} (dry-run)")
        print("    Would update config.")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    if backup_existing and options.backup and old_content is not None:
        backup_path = backup_path_for(path, timestamp)
        backup_path.write_text(old_content, encoding="utf-8")
        report.backups.append(str(backup_path))
        print(f"    Backup: {backup_path}")
    path.write_text(content, encoding="utf-8")
    report.changed.append(label)
    print(f"    Success: configured '{SERVER_ID}'.")


def configure_json_target(
    name: str,
    path: Path,
    config_key: str,
    command: str,
    pythonpath: str,
    *,
    options: InstallOptions,
    report: InstallReport,
    timestamp: str,
) -> None:
    print(f"  Configuring {name}...")
    config: Any = {}
    invalid_config_backed_up = False
    if path.exists():
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            warning = f"{name}: invalid JSON backed up/replaced: {exc}"
            report.warnings.append(warning)
            print(f"    Warning: {warning}")
            if not options.dry_run and options.backup:
                backup_path = backup_path_for(path, timestamp)
                backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
                report.backups.append(str(backup_path))
                invalid_config_backed_up = True
                print(f"    Backup: {backup_path}")

    merged, notes, warnings = merge_json_config(config, config_key, command, pythonpath)
    report.migrations.extend(f"{name}: {note}" for note in notes)
    report.warnings.extend(f"{name}: {warning}" for warning in warnings)
    for note in notes:
        print(f"    {note}.")
    for warning in warnings:
        print(f"    Warning: {warning}.")
    write_if_changed(
        path,
        json_text(merged),
        options=options,
        report=report,
        timestamp=timestamp,
        label=name,
        backup_existing=not invalid_config_backed_up,
    )


def toml_server_id(header: str) -> str | None:
    prefix = "[mcp_servers."
    if not header.startswith(prefix) or not header.endswith("]"):
        return None
    return header[len(prefix) : -1].strip()


def build_codex_block(command: str, pythonpath: str) -> list[str]:
    command = command.replace("\\", "\\\\")
    pythonpath = pythonpath.replace("\\", "\\\\")
    return [
        f"[mcp_servers.{SERVER_ID}]",
        f'command = "{command}"',
        f'args = ["-m", "{MODULE_NAME}"]',
        f'env = {{ PYTHONPATH = "{pythonpath}" }}',
        "",
    ]


def merge_codex_toml(
    content: str,
    command: str,
    pythonpath: str,
) -> tuple[str, list[str]]:
    new_block = build_codex_block(command, pythonpath)
    lines = content.splitlines()
    new_lines: list[str] = []
    block_found = False
    notes: list[str] = []

    index = 0
    while index < len(lines):
        line = lines[index]
        server_id = toml_server_id(line.strip())
        if server_id is None:
            new_lines.append(line)
            index += 1
            continue

        block_lines = [line]
        index += 1
        while index < len(lines) and not lines[index].strip().startswith("["):
            block_lines.append(lines[index])
            index += 1

        block_text = "\n".join(block_lines)
        owned_by_id = server_id == SERVER_ID
        owned_legacy = server_id == LEGACY_SERVER_ID and any(
            module in block_text for module in OWNED_MODULES
        )
        stale_owned = server_id not in {SERVER_ID, LEGACY_SERVER_ID} and any(
            module in block_text for module in OWNED_MODULES
        )
        if owned_by_id or owned_legacy or stale_owned:
            if not block_found:
                block_found = True
                new_lines.extend(new_block[:-1])
            if server_id != SERVER_ID:
                notes.append(f"removed stale owned server '{server_id}'")
            continue
        new_lines.extend(block_lines)

    if not block_found:
        if new_lines and new_lines[-1] != "":
            new_lines.append("")
        new_lines.extend(new_block[:-1])

    return "\n".join(new_lines).rstrip() + "\n", notes


def validate_toml(content: str) -> str | None:
    if tomllib is None:
        return None
    try:
        tomllib.loads(content)
    except Exception as exc:
        return str(exc)
    return None


def configure_codex_target(
    name: str,
    path: Path,
    command: str,
    pythonpath: str,
    *,
    options: InstallOptions,
    report: InstallReport,
    timestamp: str,
) -> None:
    print(f"  Configuring {name}...")
    content = ""
    invalid_config_backed_up = False
    if path.exists():
        content = path.read_text(encoding="utf-8")
        parse_error = validate_toml(content)
        if parse_error:
            warning = f"{name}: invalid TOML backed up/replaced: {parse_error}"
            report.warnings.append(warning)
            print(f"    Warning: {warning}")
            if not options.dry_run and options.backup:
                backup_path = backup_path_for(path, timestamp)
                backup_path.write_text(content, encoding="utf-8")
                report.backups.append(str(backup_path))
                invalid_config_backed_up = True
                print(f"    Backup: {backup_path}")
            content = ""

    merged, notes = merge_codex_toml(content, command, pythonpath)
    report.migrations.extend(f"{name}: {note}" for note in notes)
    for note in notes:
        print(f"    {note}.")
    write_if_changed(
        path,
        merged,
        options=options,
        report=report,
        timestamp=timestamp,
        label=name,
        backup_existing=not invalid_config_backed_up,
    )


def python_executable_for(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def client_base_paths(repo_root: Path) -> tuple[Path, Path, Path]:
    if sys.platform == "win32":
        appdata = Path(os.environ.get("APPDATA", ""))
        return (
            appdata / "Claude" / "claude_desktop_config.json",
            appdata / "Code" / "User" / "globalStorage",
            appdata / "Cursor" / "User" / "globalStorage",
        )
    if sys.platform == "darwin":
        home = Path.home()
        return (
            home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",
            home / "Library" / "Application Support" / "Code" / "User" / "globalStorage",
            home / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage",
        )
    home = Path.home()
    return (
        home / ".config" / "Claude" / "claude_desktop_config.json",
        home / ".config" / "Code" / "User" / "globalStorage",
        home / ".config" / "Cursor" / "User" / "globalStorage",
    )


def json_targets(repo_root: Path) -> list[tuple[str, Path, str, bool]]:
    claude_path, code_path, cursor_path = client_base_paths(repo_root)
    targets = [
        ("Claude Desktop", claude_path, "mcpServers", True),
        ("Gemini MCP config", Path.home() / ".gemini" / "config" / "mcp_config.json", "mcpServers", True),
        ("Cursor Native", Path.home() / ".cursor" / "mcp.json", "mcpServers", True),
        ("VS Code Native (User)", code_path.parent / "mcp.json", "servers", True),
        ("VS Code Native (Workspace)", repo_root / ".vscode" / "mcp.json", "servers", True),
    ]
    extensions = [
        ("VS Code Cline", code_path / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"),
        ("VS Code Roo-Code", code_path / "roovet.roo-cline" / "settings" / "cline_mcp_settings.json"),
        ("Cursor Cline", cursor_path / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"),
        ("Cursor Roo-Code", cursor_path / "roovet.roo-cline" / "settings" / "cline_mcp_settings.json"),
    ]
    for name, path in extensions:
        if path.parent.parent.exists():
            targets.append((name, path, "mcpServers", False))
    return targets


def command_for_target(name: str, python_exe: Path, repo_root: Path) -> tuple[str, str]:
    if name == "VS Code Native (Workspace)":
        if os.name == "nt":
            return "${workspaceFolder}/.venv/Scripts/python.exe", "${workspaceFolder}/src"
        return "${workspaceFolder}/.venv/bin/python", "${workspaceFolder}/src"
    return str(python_exe), str(repo_root / "src")


def configure_json_targets(
    repo_root: Path,
    python_exe: Path,
    *,
    options: InstallOptions,
    report: InstallReport,
    timestamp: str,
) -> None:
    print("\nConfiguring MCP clients...")
    for name, path, config_key, _force_create in json_targets(repo_root):
        command, pythonpath = command_for_target(name, python_exe, repo_root)
        configure_json_target(
            name,
            path,
            config_key,
            command,
            pythonpath,
            options=options,
            report=report,
            timestamp=timestamp,
        )


def configure_codex(
    python_exe: Path,
    repo_root: Path,
    *,
    options: InstallOptions,
    report: InstallReport,
    timestamp: str,
) -> None:
    targets = [
        ("Global Codex config", Path.home() / ".codex" / "config.toml"),
        ("Project-local Codex config", repo_root / ".codex" / "config.toml"),
    ]
    for name, path in targets:
        configure_codex_target(
            name,
            path,
            str(python_exe),
            str(repo_root / "src"),
            options=options,
            report=report,
            timestamp=timestamp,
        )


def ensure_venv_and_install(repo_root: Path, options: InstallOptions, report: InstallReport) -> Path:
    venv_dir = repo_root / ".venv"
    python_exe = python_executable_for(venv_dir)
    if options.dry_run:
        print(f"Dry-run: would ensure virtual environment at {venv_dir}.")
        if not options.skip_install:
            print("Dry-run: would run pip install -e .")
        return python_exe

    if not venv_dir.exists():
        print("Creating virtual environment (.venv)...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

    if not options.skip_install:
        print("Installing packages and dependencies in editable mode...")
        subprocess.run(
            [str(python_exe), "-m", "pip", "install", "-e", "."],
            cwd=str(repo_root),
            check=True,
        )
    else:
        print("Skipping package installation (--skip-install).")
    return python_exe


def run_smoke_check(
    python_exe: Path,
    repo_root: Path,
    options: InstallOptions,
    report: InstallReport,
) -> bool:
    if options.dry_run:
        print("Dry-run: would run post-install smoke check.")
        return True
    print("\nRunning post-install smoke check...")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    result = subprocess.run(
        [str(python_exe), "-m", MODULE_NAME, "--show-stats"],
        cwd=str(repo_root),
        env=env,
        text=True,
        capture_output=True,
    )
    if result.returncode == 0:
        print("  Success: MCP module starts and reports RTK startup stats.")
        return True
    report.errors.append("post-install smoke check failed")
    print("  Error: post-install smoke check failed.")
    if result.stderr.strip():
        print(result.stderr.strip())
    elif result.stdout.strip():
        print(result.stdout.strip())
    return False


def main() -> int:
    args = parse_args()
    options = InstallOptions(
        dry_run=args.dry_run,
        skip_install=args.skip_install,
        backup=not args.no_backup,
    )
    repo_root = Path(__file__).resolve().parents[1]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    report = InstallReport()

    print("=== Agent Guidance MCP Auto-Installer ===")
    try:
        python_exe = ensure_venv_and_install(repo_root, options, report)
    except subprocess.CalledProcessError as exc:
        report.errors.append(f"package installation failed: {exc}")
        report.print_summary()
        return exc.returncode or 1

    configure_json_targets(
        repo_root,
        python_exe,
        options=options,
        report=report,
        timestamp=timestamp,
    )
    configure_codex(
        python_exe,
        repo_root,
        options=options,
        report=report,
        timestamp=timestamp,
    )

    smoke_ok = run_smoke_check(python_exe, repo_root, options, report)
    report.print_summary()
    if report.errors or not smoke_ok:
        print("\n=== Installation completed with errors. ===")
        return 1

    print("\n=== Installation completed successfully. ===")
    print("Restart your IDE / MCP client to use the refreshed server.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
