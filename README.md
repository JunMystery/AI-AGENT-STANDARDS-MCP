# AI Agent Standards MCP (v3.0.2)

Model Context Protocol server for the AI Agent Coding Standards corpus (supporting skill set `v3.0.2`).

This server exposes the standards corpus, local skills (v3.0.2), and recommendation
workflows as MCP resources, tools, and prompts.
The standards and skills are bundled in this repository so it can run as an
independent checkout. This repo intentionally excludes direct AI-agent
auto-discovery instruction files such as `AGENTS.md`, `CLAUDE.md`, and
`.cursorrules`; clients should consume the content through MCP.

## Install

### Automatic Installation (Recommended)
This script automatically sets up the python virtual environment, installs dependencies, and registers the server with your Claude Desktop configuration:

- **Linux / macOS**:
  ```bash
  python3 scripts/install-mcp.py
  ```
- **Windows**:
  ```powershell
  python scripts/install-mcp.py
  ```

### Manual Installation
If you prefer to set up manually:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\pip install -e ".[dev]"
# On Linux / macOS:
.venv/bin/pip install -e ".[dev]"
```

## Run

From this directory:

```bash
python -m ai_agent_standards_mcp
```

Or run directly from the source checkout with the cross-platform python script:

```bash
python scripts/run-mcp.py
```

Other platform-specific launcher scripts are also available in `scripts/`:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run-mcp.ps1
```

```cmd
scripts\run-mcp.cmd
```

```bash
./scripts/run-mcp.sh
```

Do not double-click the stdio launchers above. `stdio` is for MCP clients and expects JSON-RPC messages on stdin.

For manual Windows use, open CMD or PowerShell first, then run the command from that terminal.

> [!TIP]
> **Recommended for MCP Client Configurations (like Claude Desktop / VS Code / Cursor)**:
> Run python directly with `-m ai_agent_standards_mcp` within the virtual environment `.venv` for the most robust cross-platform Stdio setup. This avoids shell-wrapper anomalies (such as PowerShell pipeline newlines).
>
> **Linux / macOS configuration**:
> ```json
> {
>   "mcpServers": {
>     "ai-agent-standards-mcp": {
>       "command": "/absolute/path/to/repo/.venv/bin/python",
>       "args": ["-m", "ai_agent_standards_mcp"],
>       "env": {
>         "PYTHONPATH": "/absolute/path/to/repo/src"
>       }
>     }
>   }
> }
> ```
>
> **Windows configuration**:
> ```json
> {
>   "mcpServers": {
>     "ai-agent-standards-mcp": {
>       "command": "C:\\absolute\\path\\to\\repo\\.venv\\Scripts\\python.exe",
>       "args": ["-m", "ai_agent_standards_mcp"],
>       "env": {
>         "PYTHONPATH": "C:\\absolute\\path\\to\\repo\\src"
>       }
>     }
>   }
> }
> ```

By default the server uses stdio transport and indexes the bundled standards
corpus in this repository. To point at another standards checkout:

```bash
$env:AI_AGENT_STANDARDS_ROOT="C:\path\to\AI-Agent-Standards"
python -m ai_agent_standards_mcp
```

For Streamable HTTP:

```bash
python -m ai_agent_standards_mcp --transport streamable-http
```

The HTTP host and port can be changed:

```bash
python -m ai_agent_standards_mcp --transport streamable-http --host 127.0.0.1 --port 41731
```

## MCP Surface

Resources:

- `standards://manifest` - JSON catalog summary.
- `standards://document/{slug}` - Markdown standards and framework documents.
- `standards://skill/{name}` - On-demand skill capsules.

Tools:

- `list_entries(category=None, kind=None)` - list indexed content.
- `get_entry(identifier)` - fetch content by slug, skill name, agent key, or path.
- `search_entries(query, limit=10, kind=None)` - keyword search with snippets.
- `recommend_context(task, limit=8)` - recommend standards and skills for a task.

Prompts:

- `apply_standards(task, focus="general")` - produce a standards-aware work prompt.
- `review_ai_code(scope="the current diff")` - produce a review prompt grounded in the framework.
- `init(project_name="")` - start a new project workflow (AWF `/init`).
- `plan(task)` - plan a feature design (AWF `/plan`).
- `design(feature)` - technical architecture design (AWF `/design`).
- `visualize(ui_description="")` - UI/UX mockup design (AWF `/visualize`).
- `code(task)` - high-quality coding implementation (AWF `/code`).
- `run(environment="local")` - launch/run application checks (AWF `/run`).
- `test(test_target="")` - test code & write test suites (AWF `/test`).
- `deploy(target="production")` - product deployment safety checks (AWF `/deploy`).
- `debug(error_message)` - systematic debugging protocol (AWF `/debug`).
- `refactor(target_file)` - safe code refactoring guidelines (AWF `/refactor`).
- `audit(scope="security")` - health & security audits (AWF `/audit`).
- `rollback(revision="")` - emergency state rollback (AWF `/rollback`).
- `recap(session_id="")` - workspace context restoration (AWF `/recap`).

### How to Invoke Prompts (Slash Commands) in MCP Clients

- **Claude Desktop**: Type `/` in the chat input box to show the list of available slash command prompts (e.g., `/plan`, `/code`, `/debug`). Select the prompt, fill in its arguments, and run.
- **VS Code & Cursor Extensions (Cline / Roo-Code)**:
  - Access registered prompts directly via the MCP Prompts UI list.
  - Or, instruct the agent directly in the chat, for example: *"Chạy prompt `plan` thiết kế hệ thống đăng nhập"* (Run prompt `plan` to design login system) or *"Gọi prompt `debug` lỗi database connection refused"*.
- **Auto-Discovery**: Since individual detailed skills (like `accessibility`, `api-design`, etc.) are registered as resources and tools, the AI agent will automatically search and load them on-demand when it detects matching keywords in your prompt. You do not need to manually call them most of the time.

#### Forcing Auto-Discovery in VS Code Extensions (Cline, Roo-Code, Cursor)

If your VS Code AI agent doesn't automatically call the MCP tools, you can force it by configuring its **Custom System Prompt** or **Custom Instructions**:

1. **In Cline / Roo-Code Settings:** Add this instruction to the *Custom System Prompt* field:
   ```text
   Before starting any coding, refactoring, or debugging task, you MUST invoke the `recommend_context(task)` tool from the `ai-agent-standards` MCP server. You must use the returned standards and skills to ground your work.
   ```
2. **In Cursor (.cursorrules):** Add the same directive to your project's custom rules or global settings.
3. **Keyword triggers:** Alternatively, always start your prompt with keywords related to the skills (e.g. "Run a security audit on..." or "Check accessibility of...") to trigger auto-discovery.


## Bundled Corpus

The repository carries its own copy of:

- `skills/` - on-demand skill capsules.
- `ai-agent-standards/` - standards, prompts, compliance, and review docs.
- `karpathy/` - core principle source files.
- `docs/` - maintainer-facing notes for the standards corpus.

Wheel builds include this corpus under the package's bundled data fallback, while
editable/source checkouts index the top-level files directly.

Direct agent instruction files are intentionally excluded from this MCP-only
distribution.

## Development

```bash
python -m pytest
```

The test suite covers catalog discovery, lookup, search, and task-context
recommendations without needing to launch an MCP client.
