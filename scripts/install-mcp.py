#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from pathlib import Path

def main():
    repo_root = Path(__file__).resolve().parents[1]
    venv_dir = repo_root / ".venv"
    
    print("=== AI Agent Standards MCP Auto-Installer ===")
    
    # 1. Setup virtual environment
    if not venv_dir.exists():
        print("Creating virtual environment (.venv)...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    
    # Determine python executable path in venv
    if os.name == "nt":
        pip_exe = venv_dir / "Scripts" / "pip.exe"
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:
        pip_exe = venv_dir / "bin" / "pip"
        python_exe = venv_dir / "bin" / "python"
        
    # 2. Install dependencies
    print("Installing packages and dependencies in editable mode...")
    subprocess.run([str(pip_exe), "install", "-e", "."], cwd=str(repo_root), check=True)
    
    # 3. Locate and configure targets
    if sys.platform == "win32":
        appdata = Path(os.environ.get("APPDATA", ""))
        claude_path = appdata / "Claude" / "claude_desktop_config.json"
        code_path = appdata / "Code" / "User" / "globalStorage"
        cursor_path = appdata / "Cursor" / "User" / "globalStorage"
    elif sys.platform == "darwin":
        home = Path.home()
        claude_path = home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        code_path = home / "Library" / "Application Support" / "Code" / "User" / "globalStorage"
        cursor_path = home / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage"
    else: # Linux
        home = Path.home()
        claude_path = home / ".config" / "Claude" / "claude_desktop_config.json"
        code_path = home / ".config" / "Code" / "User" / "globalStorage"
        cursor_path = home / ".config" / "Cursor" / "User" / "globalStorage"

    targets = []
    # Always attempt to configure Claude Desktop and Antigravity IDE (create folders if missing)
    targets.append(("Claude Desktop", claude_path, True))
    
    # Antigravity IDE config path (cross-platform)
    antigravity_path = Path.home() / ".gemini" / "config" / "mcp_config.json"
    targets.append(("Antigravity IDE", antigravity_path, True))

    # Cline & Roo-Code for VS Code and Cursor
    extensions = [
        ("VS Code Cline", code_path / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"),
        ("VS Code Roo-Code", code_path / "roovet.roo-cline" / "settings" / "cline_mcp_settings.json"),
        ("Cursor Cline", cursor_path / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"),
        ("Cursor Roo-Code", cursor_path / "roovet.roo-cline" / "settings" / "cline_mcp_settings.json"),
    ]
    
    for name, path, *rest in [e + (False,) for e in extensions]:
        # Only configure if the parent directory exists (extension is installed)
        if path.parent.parent.exists():
            targets.append((name, path, False))

    print("\nConfiguring MCP Clients...")
    for name, path, force_create in targets:
        print(f"  Configuring {name}...")
        
        # Load or initialize config
        config = {}
        if path.exists():
            try:
                config = json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"    Warning: Failed to read existing config: {e}. Starting fresh.")
                
        if "mcpServers" not in config:
            config["mcpServers"] = {}
            
        # Configure the server using direct venv python execution (Option A)
        pythonpath = str(repo_root / "src")
        config["mcpServers"]["ai-agent-standards-mcp"] = {
            "command": str(python_exe),
            "args": ["-m", "ai_agent_standards_mcp"],
            "env": {
                "PYTHONPATH": pythonpath
            }
        }
        
        # Write back config
        try:
            if force_create:
                path.parent.mkdir(parents=True, exist_ok=True)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(config, indent=2), encoding="utf-8")
            print(f"    Success: Configured 'ai-agent-standards-mcp' server.")
        except Exception as e:
            print(f"    Error: Failed to write config file: {e}")
            
    # 4. Configure Codex (config.toml)
    configure_codex(python_exe, repo_root)
            
    print("\n=== Installation Completed Successfully! ===")
    print("Restart your IDE / MCP Client to start using the server.")

def configure_codex(python_exe, repo_root):
    codex_dir = Path.home() / ".codex"
    config_path = codex_dir / "config.toml"
    
    python_exe_str = str(python_exe).replace("\\", "\\\\")
    pythonpath_str = str(repo_root / "src").replace("\\", "\\\\")
    
    new_block = [
        "[mcp_servers.ai-agent-standards-mcp]",
        f'command = "{python_exe_str}"',
        'args = ["-m", "ai_agent_standards_mcp"]',
        f'env = {{ PYTHONPATH = "{pythonpath_str}" }}',
        ""
    ]
    
    print("  Configuring Codex...")
    try:
        codex_dir.mkdir(parents=True, exist_ok=True)
        content = ""
        if config_path.exists():
            content = config_path.read_text(encoding="utf-8")
            
        # Parse and replace the block if it exists
        lines = content.splitlines()
        new_lines = []
        in_block = False
        block_found = False
        
        for line in lines:
            stripped = line.strip()
            if stripped == "[mcp_servers.ai-agent-standards-mcp]":
                in_block = True
                block_found = True
                new_lines.extend(new_block[:-1]) # add new block without the trailing newline
                continue
            if in_block:
                if stripped.startswith("["):
                    in_block = False # exited the block
                    new_lines.append(line)
                continue
            new_lines.append(line)
            
        if not block_found:
            if new_lines and new_lines[-1] != "":
                new_lines.append("")
            new_lines.extend(new_block)
            
        config_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print("    Success: Configured 'ai-agent-standards-mcp' server in Codex config.toml.")
    except Exception as e:
        print(f"    Error: Failed to configure Codex: {e}")

if __name__ == "__main__":
    main()
