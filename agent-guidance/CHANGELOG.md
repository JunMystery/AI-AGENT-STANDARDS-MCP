# CHANGELOG - AI Agent Coding Standards

Track versions and updates for the AI Agent Coding Standards framework.

## [3.2.0] - 2026-06-12

### Added
- **Safe universal RTK optimization** - Added a pure-Python MCP response optimizer with conservative defaults, TTL cache, content detection, metrics, and safe truncation metadata for structured responses.
- **RTK runtime monitoring tools** - Added `get_rtk_stats(detailed)` and `reset_rtk_stats()` for live MCP server optimization telemetry.
- **Installer re-run update flow** - Hardened `scripts/install-mcp.py` with config backups, merge-safe JSON/TOML updates, stale owned-server cleanup, dry-run/skip-install/no-backup flags, and a startup smoke check.

### Fixed
- **RTK robustness** - Hardened per-call `rtk_max_tokens` parsing, content-equality based `modified` reporting, and cap accounting when required RTK metadata pushes tiny responses over the configured cap.

### Changed
- **RTK and installer documentation** - Documented conservative RTK behavior, per-call overrides, CLI startup stats, installer re-run behavior, and runtime stats tooling across the MCP docs.
- **Version synchronization** - Updated framework and package release surfaces to v3.2.0.

## [3.1.0] - 2026-06-12

### Added
- **Project-context MCP tools** - Added bounded project tree, code search, file read, and snapshot export tools so AI agents can inspect codebases quickly without broad file reads.
- **Focused documentation set** - Split detailed setup, usage, MCP surface, project-context, and development guidance into dedicated docs under `docs/`.

### Changed
- **README landing page** - Reduced the root README to the essential project overview, installation, quick start, documentation links, MCP summary, and development command.
- **Version synchronization** - Updated framework and package release surfaces to v3.1.0.

## [3.0.3] - 2026-06-11

### Added
- **Cursor Native Auto-Installation:** Updated `scripts/install-mcp.py` to automatically detect and configure the `agent-guidance-mcp` server inside the global Cursor configuration file `~/.cursor/mcp.json` (for Cursor Native MCP).

## [3.0.2] - 2026-06-11

### Added
- **Codex Auto-Installation:** Updated `scripts/install-mcp.py` to automatically detect and configure the `agent-guidance-mcp` server inside the global Codex config file `~/.codex/config.toml` (for Codex CLI & VS Code/Codex App extension).

## [3.0.1] - 2026-06-11

### Fixed
- **VS Code MCP Client Activation:** Fixed `scripts/run-mcp.cmd` false-positive Explorer-click detection that triggered HTTP transport instead of stdio, and executed `pause`, causing VS Code to hang during extension activation. Stdin is now verified using `timeout` before invoking interactive launcher behavior.

## [3.0.0] - 2026-06-11

### Fixed
- **Large-file refactor audit scope** - Updated `skills/large-file-refactor/SKILL.md` to use tracked project files as the candidate source and exclude `.venv`, `.vscode`, cache, build, vendor, generated, and binary/media files from broad audits.

### Changed
- **7-step pipeline documentation** - Updated README and onboarding/review docs so the pipeline reflects all 6 Core Principles, 12 security constraints, quality gates, Human Gate checklists, and optional multi-agent collaboration.
- **Review checklist parity** - Added DRY & Reusability and Code Organization checks to reviewer-facing documentation and the PR checklist.
- **Version bump** - Updated framework versioning to v3.0.0 across current project metadata, generated instruction sources, install docs, skill references, index, and multi-agent files.

## [2.6.0] - 2026-06-05

### Added
- **Single source rules generation** - Added `scripts/generate-rules.py`, `rules/agent-manifest.json`, and agent templates so instruction files are generated from shared sources instead of maintained by hand.
- **Rules generation docs** - Added `docs/rules-generation.md` and `docs/repo-map-for-agents.md` for maintainer and agent onboarding.
- **Large-file refactor skill** - Added `skills/large-file-refactor/SKILL.md` and wired it into the skill indexes for responsibility-based file splitting guidance.

### Changed
- **Setup manifest wiring** - `scripts/setup.py` now reads supported agent instruction files from `rules/agent-manifest.json`.
- **Version Bump** - Updated framework versioning to v2.6.0 across current project metadata, generated instruction surfaces, skill references, index, install docs, and multi-agent files.

### Removed
- **Redundant project standards example file** - Removed `PROJECT-STANDARDS-EXAMPLE.md` because `PROJECT-STANDARDS.md` now includes the editable template directly.

## [2.5.0] - 2026-05-30

### Added
- **OpenAI Codex / Codex VS Code support** - Added `AGENTS.md` as the Codex instruction surface and a `codex-vscode` on-demand skill capsule.
- **Codex discovery wiring** - Updated setup, install docs, README, and skill indexes so Codex instructions are installed with the rest of the framework.
- **Agent-specific setup menu** - `scripts/setup.py` now lets users install one agent instruction file, choose all, or press `0` to cancel.

### Fixed
- **Cross-drive setup on Windows** - `scripts/setup.py` now falls back to absolute Markdown link prefixes when standards and target projects are on different Windows drives.

### Changed
- **Version Bump** - Updated framework versioning to v2.5.0 across the primary docs, instruction surfaces, skill references, index, install docs, and multi-agent files.
- **Cleaner default installs** - Setup no longer copies every instruction file unless the user chooses all or passes `--agent all`.

## [2.4.0] - 2026-05-28

### Added
- **6th Core Principle (Code Organization):** Added code organization and file structure as the 6th Core Principle (`karpathy/principles.md`), including file splitting guidelines (<300 LOC limit), role-based suffixes, barrel exports, and colocation.
- **DRY & Reusability Expansion:** Generalised Principle 5 to apply to all code categories (including configurations, TypeScript types, schemas, and test mocks) instead of just UI and business logic.

### Changed
- **System-wide Principle Count:** Updated principle references from 5 to 6 core principles across all tool config files, multi-agent templates, checklists, and documentation.
- **Version Bump:** Upgraded version to v2.4.0 across the framework.

## [2.3.0] - 2026-05-25

### Added
- **General on-demand skills** - Added accessibility, API design, ADRs, database migrations, error handling, Git workflow, production audit, search-first, skill stocktake, and rules distillation skill capsules adapted from ECC.
- **Agent discovery wiring** - Documented the expanded skill set so supported AI agents can load the new capsules only when relevant.
- **ECC Credit** - Credited ECC as the source for the expanded general skill-set ideas and on-demand structure.

### Changed
- **Version Bump** - Updated repo versioning to v2.3.0 across the primary docs, instruction surfaces, skill references, index, install docs, and multi-agent files.

## [2.2.0] - 2026-05-24

### Added
- **`skills/`** - On-demand skill capsules ported from ECC and wired into the framework docs as task-specific references.
- **ECC Credit** - Explicit attribution added for the imported skill capsules and their on-demand usage model.

### Changed
- **Version Bump** - Updated repo versioning to v2.2.0 across the primary docs and instruction surfaces.
- **`README.md` / `SKILL-REFERENCE.md` / `INDEX.md`** - Updated version strings and skill-loading guidance to reflect on-demand skill capsules.

### Fixed
- **Version parity** - Synchronized the release metadata and verification prompts with the new v2.2.0 release.

## [2.1.0] - 2026-05-20

### Added
- **`scripts/setup.py`** - Automated setup script: copies rule files to any project root and auto-rewrites internal links to match the actual folder path. Supports auto-detection of project root and custom path arguments.

### Fixed
- **Link Architecture** - Reverted all internal paths in root instruction files to bare relative paths (`agent-guidance/...`) so they resolve correctly when used directly inside the repo. The `setup.py` script now adds the folder prefix dynamically when copying to external projects.
- **ASCII Bell characters** - Cleaned up `\x07` control characters in Auto-Discovery paths caused by Python escape sequences.
- **Principle 5 parity** - Added DRY & Reusability to `.cursorrules` and `.cursor/rules/karpathy-guidelines.mdc`.
- **Version parity** - Synchronized version to v2.1 across all config, documentation, and multi-agent files.

### Changed
- **`INSTALL.md`** - Rewritten with automated setup as primary installation method.
- **`README.md`** - Quick Start now shows `python Agent-Guidance/scripts/setup.py`.

---

## [2.0.0] - 2026-05-17

### Added (Enterprise Engineering & Compliance)
- **`engineering-practices/`** - New module for Software Engineering Standards:
  - `DOCUMENTATION_STANDARDS.md` (README, Changelog, JSDoc, OpenAPI)
  - `RELEASE_PROCESS.md` (SemVer, Gitflow, pre-release checklists)
  - `TESTING_STANDARDS.md` (Test Pyramid, 80% coverage bounds, FIRST principles)
  - `NON_FUNCTIONAL_REQUIREMENTS.md` (Performance budgets, No N+1, Caching)
- **`compliance/`** - New module for Industry Standards:
  - `COMPLIANCE.md` (OWASP Top 10 for LLM, NIST RMF, CISA alignment)
  - `A11Y_CHECKLIST.md` (WCAG 2.1 AA accessibility checklist)

### Added (Dynamic Skill Auto-Discovery)
- **Auto-Discovery Block** - Injected into all root instruction files (`GEMINI.md`, `CLAUDE.md`, `.cursorrules`, etc.). Modern AI agents will now self-load relevant standards dynamically based on the task prompt without requiring manual `@reference`.

### Changed
- **Version Bump** - Upgraded framework globally to v2.0.0.
- **`SKILL-REFERENCE.md`** - Updated with Dynamic Auto-Discovery instructions and new Engineering & Compliance references.
- **`code-review-checklist.md`** - Added Section 11 for Compliance & Accessibility, and expanded Section 6 for Performance budgets.

---

## [1.4.0] - 2026-05-13

### Added (P0 - 12 Security Constraints)
- **`security-constraints.md` v2.0** - Expanded from 6 to 12 non-negotiable constraints:
  - Constraint 7: Secure Authentication & Authorization
  - Constraint 8: Secure Cryptography
  - Constraint 9: No Hallucinated Dependencies (Slopsquatting)
  - Constraint 10: No Instruction File Poisoning
  - Constraint 11: Infrastructure-as-Code Security
  - Constraint 12: AI Agent Access Control & Tool Governance
- **`scripts/security-audit.sh`** - Local/CI security scan covering all 12 constraints

### Added (P1 - Mobile Development Cookbook)
- **`prompts/sample-use-cases/mobile-development-cookbook.md`** - General mobile cookbook: Android, iOS, Flutter, React Native (PROMPT-007)
- **Mobile Development** category in `prompts/indexed-by-category.md`

### Added (Multi-Agent Expansion)
- **`multi-agent/test-agent.md`** - Test Agent (writes tests independently, no production code changes)
- **`multi-agent/documentation-agent.md`** - Documentation Agent (API docs, READMEs, changelogs)

### Added (Developer Experience)
- **`SKILL-REFERENCE.md`** - Quick lookup: which files to @reference per task type
- **`SKILL-REFERENCE_VI.md`** - Vietnamese version with skill explanations

### Changed
- **All auto-discovery files** - Added security constraints + SKILL-REFERENCE references to: CLAUDE.md, GEMINI.md, COPILOT.md, .instructions.md, .cursorrules
- **`ai-code-audit.yml`** - Added `security-scan` job running `scripts/security-audit.sh`
- **`README.md`** - Updated repo structure, key files, version to 1.4.0
- **`Development_doc_VI.md`** - Roadmap updated with all completed items

---

## [1.2.0] - 2026-05-13

### Added (P0 - Prompt Engineering Cookbook)
- **`prompts/sample-use-cases/rag-implementation-cookbook.md`** - RAG pipeline prompt for safe medical data retrieval (PROMPT-006)
- **RAG / AI Pipeline** category in `prompts/indexed-by-category.md`

### Added (P0 - Systematic Code Audit)
- **`.github/pull_request_template.md`** - PR audit checklist with Zero-Trust, Simplicity, Two-Pair Eyes sections
- **`.github/workflows/ai-code-audit.yml`** - Automated SAST quality gate (SonarCloud + dependency scan)
- **Section 10: RAG Pipeline Audit** in `audit-ai-code-full.md`
- **Section 11: AI Output Safety Audit** in `audit-ai-code-full.md`

### Added (P2 - Multi-Agent Orchestration)
- **`multi-agent/coder-agent.md`** - Coder Agent (implementation only, no DB/env changes)
- **`multi-agent/reviewer-agent.md`** - Reviewer Agent (audit & optimize, no new features)

### Changed
- **`README.md`** - Updated to v1.2.0 with CI/CD, multi-agent, and expanded key files sections
- **`Development_doc_VI.md`** - Roadmap updated with P0/P2 completion status and deliverable links

---

## [1.1.0] - 2026-05-13

### Added
- **Karpathy Skills Integration:** Merged content from [andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) into the core framework
- **`karpathy/` module:** Single source of truth for the 4 Karpathy Principles
  - `karpathy/principles.md` - The 4 principles (source of truth)
  - `karpathy/examples.md` - Real-world anti-patterns and correct approaches
- **Auto-discovery instruction files** for all major AI tools:
  - `CLAUDE.md` - Claude Code
  - `GEMINI.md` - Gemini Code Assist / CLI
  - `COPILOT.md` - GitHub Copilot
  - `.instructions.md` - VS Code Copilot (rewritten in English)
  - `.cursor/rules/karpathy-guidelines.mdc` - Cursor
  - `.cursorrules` - Cursor/Windsurf fallback
- **Verification Prompt:** Each instruction file includes a verification block - users can ask `/standards` to confirm the AI loaded the correct skills
- **`INSTALL.md`** - 1-step installation guide with verification instructions
- **Root `.gitignore`** - Moved from `.agent-guidance/`

### Changed
- **Renamed `.agent-guidance/` -> `agent-guidance/`** - Removed dot prefix for visibility across all OS/tools
- **`README.md`** - Rewritten in English with AI Tool Support Matrix and simplified Quick Start
- **All instruction files** - Converted to 100% English

### Removed
- **`andrej-karpathy-skills/`** - Deleted after content was integrated into the main framework
- **`.agent-guidance/.cursor/`** - Moved to root `.cursor/`
- **`.agent-guidance/.cursorrules`** - Merged into root `.cursorrules`
- **`.agent-guidance/.gitignore`** - Moved to root `.gitignore`

---

## [1.0.0] - 2026-05-12

### Added
- **Initial Release:** Complete framework built from the original methodology document
- **8 functional domains:**
  - `prompts/` - Standard prompt template library
  - `quality-control/` - Quality control pipeline
  - `risk-management/` - Risk management & escalation
  - `onboarding/` - Training & onboarding materials
  - `multi-agent/` - Placeholder for P2 roadmap
  - `reference/` - Reference documentation & error tables

- **Core Files:**
  - `.cursorrules` - Default Cursor/Windsurf rules
  - `README.md` - Quick-start guide
  - `INDEX.md` - Master file index
  - `CHANGELOG.md` - This file

- **Sample Prompts (5 use cases):**
  - API with rate limiting
  - Cache strategy refactor
  - Unit test generation
  - Security audit
  - Database migration

---

## Update Log

| Version | Date | Changes | Status |
|---------|------|---------|--------|
| 3.2.0 | 2026-06-12 | Safe RTK optimization, RTK stats tools, robust installer re-run flow, docs and regression tests | Released |
| 3.0.3 | 2026-06-11 | Add Cursor Native auto-installation support in scripts/install-mcp.py | Released |
| 3.0.2 | 2026-06-11 | Add Codex auto-installation support in scripts/install-mcp.py | Released |
| 3.0.1 | 2026-06-11 | Fix VS Code MCP client activation hang in run-mcp.cmd wrapper script | Released |
| 3.0.0 | 2026-06-11 | Major release: Pipeline documentation parity, review checklist parity, large-file audit scope filtering | Released |
| 2.6.1 | 2026-06-05 | Pipeline documentation parity, review checklist parity, large-file audit scope filtering | Released |
| 2.6.0 | 2026-06-05 | Generated rule files, manifest-based setup, large-file refactor skill, repo map docs | Released |
| 2.3.0 | 2026-05-25 | Expanded ECC-derived general on-demand skill set, agent discovery wiring, version synchronization | Released |
| 2.2.0 | 2026-05-24 | On-demand ECC skill capsules, skill-loading docs, release metadata synchronization | Released |
| 2.1.0 | 2026-05-20 | Automated setup script, link architecture fix, version & principle synchronization | [OK] Released |
| 2.0.0 | 2026-05-17 | Enterprise Engineering Standards, Industry Compliance, Dynamic Skill Auto-Discovery | [OK] Released |
| 1.4.0 | 2026-05-13 | 12 Security Constraints, 4-Agent Architecture, Mobile Cookbook, Skill Reference, CI/CD hardening | [OK] Released |
| 1.1.0 | 2026-05-13 | Karpathy Skills Integration, English conversion, auto-discovery files | [OK] Released |
| 1.0.0 | 2026-05-12 | Initial release | [OK] Released |

---

## How to Update

When making changes:
1. Add a new entry at the top (after the CHANGELOG header)
2. Specify: Version, Date, Changes, Status
3. Commit to Git alongside source code changes
4. Update version in `README.md` for official releases

**Version Format:** Major.Minor.Patch (e.g., 1.0.0 -> 1.0.1 -> 1.1.0 -> 2.0.0)
