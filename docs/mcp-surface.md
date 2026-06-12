# MCP Surface Reference

[Back to README](../README.md)

This page lists the MCP resources, tools, and prompts exposed by the server.

## Resources

| Resource | Description |
|---|---|
| `standards://manifest` | JSON manifest for indexed standards, docs, skills, and root reference files. |
| `standards://document/{identifier}` | Markdown content for a standards document by slug or identifier. |
| `standards://skill/{name}` | Markdown content for a local on-demand skill capsule by name. |

## Standards Tools

| Tool | Description |
|---|---|
| `list_entries(category, kind)` | List indexed standards catalog entries, optionally filtered by category or kind. |
| `get_entry(identifier)` | Fetch one entry by slug, skill name, agent key, URI, or relative path. |
| `search_entries(query, limit, kind)` | Search standards entries and return ranked snippets. |
| `recommend_context(task, limit)` | Recommend standards, skills, and references for a coding task. |
| `get_rtk_stats(detailed)` | Return RTK optimization metrics for this server process. |
| `reset_rtk_stats()` | Reset RTK optimization metrics and cache for this server process. |

## Project Context Tools

| Tool | Description |
|---|---|
| `get_project_tree(project_path, max_depth)` | Return a bounded source tree for a project. |
| `search_project_code(project_path, query, limit)` | Search project source files and return bounded snippets. |
| `read_project_file(project_path, relative_path, start_line, max_lines)` | Read a bounded line range from one project text file. |
| `export_project_snapshot(project_path, output_path, max_file_bytes, max_total_bytes)` | Export bounded project tree and code content for AI agent context. |

Project-context tools also accept optional `rtk_enabled`, `rtk_level`, and `rtk_max_tokens` arguments. Defaults are conservative: exact file-read content is preserved unless a hard RTK cap is hit, and any modified structured response includes an `rtk` metadata field with truncation and token counts.

See [Project Context Tools](project-context-tools.md) for detailed usage and safety notes.

## Prompts

| Prompt | Slash Command | Description |
|---|---|---|
| `apply_standards` | - | Generate a standards-aware system instructions prompt. |
| `review_ai_code` | - | Review code against the Karpathy principles framework. |
| `init` | `/init` | Initialize a new project workflow. |
| `plan` | `/plan` | Plan feature design and workflow layout. |
| `design` | `/design` | Technical architectural design guidelines. |
| `visualize` | `/visualize` | Create UI/UX mockups and design guides. |
| `code` | `/code` | Write high-quality compliant code implementations. |
| `run` | `/run` | Build, run, and verify the application environment. |
| `test` | `/test` | Write and execute unit/integration test suites. |
| `deploy` | `/deploy` | Check safety checklists before deployment. |
| `debug` | `/debug` | Systematic troubleshooting and error-solving protocol. |
| `refactor` | `/refactor` | Safe code refactoring instructions. |
| `audit` | `/audit` | Execute security and system-health audits. |
| `rollback` | `/rollback` | Execute emergency recovery/rollback steps. |
| `recap` | `/recap` | Rebuild workspace and context session state. |

## Recommended Ordering

For coding tasks, a good default order is:

1. `recommend_context(task)`
2. `get_project_tree(project_path)`
3. `search_project_code(project_path, query)`
4. `read_project_file(project_path, relative_path)`
5. Edit only the files needed.
6. Run targeted verification.

## Related Docs

- [Usage Guide](usage.md)
- [Project Context Tools](project-context-tools.md)
- [Client Configuration](client-configuration.md)
