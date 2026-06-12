# 🛠️ Project-Specific AI Agent Standards

This file contains standards, conventions, and rules specific to this project. AI Agents MUST adhere to the rules herein, in parallel with the core standards (like `GEMINI.md`, `CLAUDE.md`).

> **💡 Instructions:**
> - **Independent operation:** Simply create/edit this file, and the AI Agent will automatically detect it.
> - **Fully customizable:** You can add new fields (e.g., "Reviewer", "Effective Date") if necessary. Just keep it in a bulleted list format.
> - Use this file to define: project architecture, preferred libraries, naming conventions, error handling flows, etc.

---

## 🏗️ Template

*(Copy the block below to add a new standard. You can add/remove any fields according to your needs)*

### [Standard Name / Category]
- **Rule (Required):** [Clear description of the rule the AI must follow]
- **Reason (Required):** [Brief explanation of why this rule exists]
- **Do / Good Example (Optional):** [Example of correct code/behavior]
- **Don't / Bad Example (Optional):** [Example of incorrect code/behavior]
- **Scope (Optional):** [e.g.: Only applies to Frontend code, or only .ts files]
- **Reference (Optional):** [Link or path to documentation, design file, issue...]
- **Exceptions (Optional):** [Cases where this rule does not apply]
- **Terminal Command (Optional):** [Commands to run, e.g.: npm run lint]
- **How to Test (Optional):** [How to know this rule has been followed?]

---

## 📋 Project Standards List (Customize below)

<!-- ADD YOUR STANDARDS BELOW -->

### MCP Context Grounding
- **Rule (Required):** At the start of each coding session, the AI Agent MUST call `recommend_context(task)` and `get_project_tree(project_path)`. For large refactors, upgrades, audits, or unfamiliar code, it MUST also use `search_project_code(project_path, query)` and `export_project_snapshot(project_path)` when a reusable overview is useful. Before editing any file, it MUST inspect the current target file with `read_project_file(project_path, relative_path)` or an equivalent file-read tool. Avoid repeated broad scans during the same session unless the project changed significantly.
- **Reason (Required):** To ground implementation work in current standards and current project structure while preventing broad, repeated, token-heavy code scans.
- **Do / Good Example:** Start a session by calling `recommend_context("implement rate limiting for Auth API")` and `get_project_tree(project_path)`, then use `search_project_code` and `read_project_file` to inspect only relevant files before editing.
- **Don't / Bad Example:** Coding from assumptions, stale snapshots, or broad repeated scans without checking the current target file first.
- **How to Test (Optional):** Ask the agent to list the standards/skills it loaded, the project tree scan it used, and the exact files it inspected before editing.
