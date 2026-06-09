---
name: large-file-refactor
description: Workflow for refactoring large or monolithic files by responsibility, not by line-count alone. Use when splitting files over 300 LOC, extracting modules, reducing mixed responsibilities, or breaking React components into hooks/subcomponents.
origin: AI-Agent-Standards
---

# Large-File Refactor

Use this skill when a task asks to split a large file, reduce a monolithic module, extract services/controllers/helpers, or bring files closer to the 300 LOC guideline.

## Core Rule

Split by responsibility, not by line count alone.

Do not cut a file into arbitrary chunks just to satisfy a numeric target. A 320-line cohesive algorithm may be better left intact, while a 260-line file with unrelated validation, persistence, and notification logic may deserve extraction.

## Audit Scope

Audit only project-owned source files and project documentation, or a specific file path the user explicitly provided.

When discovering candidate files yourself, use `git ls-files` or an equivalent tracked-file list as the source of truth. Do not use a raw filesystem walk as the primary source unless repository ignore rules and the exclusions below have already been applied.

Always exclude:

- `.git/`, `.venv/`, `venv/`, `env/`, `.vscode/`, `.idea/`
- `node_modules/`, `__pycache__/`, `.pytest_cache/`, `.cache/`
- `build/`, `dist/`, `htmlcov/`, coverage reports, and test artifacts
- generated files, vendored files, externally synchronized files, and binary/media files

If the user provides a specific path, audit that path only. If the path is ignored, vendored, generated, or outside normal project scope, warn about that status and continue only when the user clearly requested that exact file.

For broad requests such as "AI Audit large-file-refactor violations", report only in-scope project candidates. Do not list excluded environment, editor, cache, build, vendor, generated, or binary/media files as violations.

## Decision Thresholds

- `<300 LOC`: keep the file unless it clearly mixes unrelated responsibilities.
- `300-500 LOC`: recommend splitting only when the file has more than one durable responsibility.
- `>500 LOC`: perform an explicit split analysis before implementation.

Count meaningful code first. Ignore blank lines and comments when judging whether the file is truly large.

## Workflow

1. Select candidate files.
   - Prefer `git ls-files` or an equivalent tracked-file list.
   - Keep only in-scope source/project documentation files.
   - Exclude ignored, environment, editor, cache, build, vendor, generated, external, and binary/media files before counting LOC.
   - If the user gave an exact path, keep the audit limited to that path and apply the warning rule from Audit Scope when needed.

2. Analyze responsibilities.
   - List the functional blocks: classes, functions, handlers, JSX sections, data access, validation, transformation, side effects.
   - Name what each block owns and what can change independently.

3. Cluster cohesive code.
   - Keep code together when it is called together most of the time or shares one domain responsibility.
   - Prefer domain/package-local extraction over distant shared folders.

4. Map dependencies before extracting.
   - Identify imports, globals, shared types, callbacks, side effects, and public API callers.
   - Check for circular import risk before creating new files.
   - If splitting creates a cycle, choose a different boundary, introduce dependency inversion, or keep the code together.

5. Extract with compatibility.
   - Preserve behavior and public API unless the user explicitly approved an API change.
   - Keep orchestration in the original file when that makes migration safer.
   - Use existing project naming, file layout, test helpers, and module style.

6. Verify after refactor.
   - Run existing tests without changing their intent.
   - Check imports and circular dependency warnings when tooling exists.
   - Confirm new files remain focused and generally under 300 meaningful LOC.

## Common Boundaries

- Services/controllers: split validation, domain logic, persistence, notification, and logging only when they are separate responsibilities.
- React/UI: extract stateful hooks, repeated subcomponents, and dense table/chart sections; keep the parent as orchestration.
- Pipelines: split extract, transform, load, validation, retry, metrics, and notification when dependencies flow one way.
- Algorithms: extract helpers or preprocessing only if the core algorithm remains easier to understand.

## Exceptions

Do not split by default when:

- The file is generated, vendored, or externally synchronized.
- The file is mostly constants or configuration that changes together.
- A cohesive algorithm would become harder to reason about across files.
- Splitting would create circular imports or tighter coupling.
- The change would require broad public API migration outside the user's request.

## Output Expectation

When this skill is active, provide:

- Scope source used, such as `git ls-files`, a tracked-file list, or the exact user-provided path.
- Excluded categories when relevant, such as `.venv`, `.vscode`, cache, build, vendor, generated, or binary/media files.
- Responsibility analysis for the large file.
- Split/keep decision with the threshold applied.
- Proposed module boundaries and dependency direction.
- Circular dependency risk and mitigation.
- Files to create/change and public API impact.
- Verification evidence: tests/checks run, import-cycle checks when available, and any residual risk.
