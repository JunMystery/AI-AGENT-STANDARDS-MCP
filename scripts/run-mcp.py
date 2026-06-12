#!/usr/bin/env python
"""Cross-platform launcher for the Agent Guidance MCP server.

This script works on both Windows and Linux/macOS. It automatically detects 
the local virtual environment (.venv) if present, sets up the python path 
to include the development source directories, and executes the server.
"""

from __future__ import annotations

import os
import subprocess
import sys


def main() -> None:
    # Resolve repository directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    src_path = os.path.join(repo_root, "src")

    # Determine interpreter (prefer local .venv)
    if os.name == "nt":
        venv_python = os.path.join(repo_root, ".venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join(repo_root, ".venv", "bin", "python")

    python_exe = venv_python if os.path.exists(venv_python) else sys.executable

    # Configure PYTHONPATH to include src
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    if existing_pythonpath:
        env["PYTHONPATH"] = f"{src_path}{os.pathsep}{existing_pythonpath}"
    else:
        env["PYTHONPATH"] = src_path

    # Construct execution command
    cmd = [python_exe, "-m", "ai_agent_standards_mcp"] + sys.argv[1:]

    # Run the server process
    try:
        if os.name != "nt" and hasattr(os, "execve"):
            # Clean handoff (Unix-like systems)
            os.execve(python_exe, cmd, env)
        else:
            # Fallback for Windows
            sys.exit(subprocess.call(cmd, env=env))
    except Exception as e:
        sys.stderr.write(f"Error launching MCP server: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
