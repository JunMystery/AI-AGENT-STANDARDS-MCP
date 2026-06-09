# Skill Reference - Quick Lookup

**Which files to reference for each type of task.**

Copy the `@file` references into your prompt to activate the relevant skills.
This repository uses agent-specific Markdown instruction files, not a shared skill layer.

---

## Everyday Coding (no extra reference needed)

Your AI agent **already loaded** the 6 Core Principles from the root instruction file (`CLAUDE.md`, `GEMINI.md`, etc.). Just describe your task normally.

*(Note: If you have project-specific rules, add them to `PROJECT-STANDARDS.md`. The AI will automatically read it.)*

---

##  Dynamic Skill Auto-Discovery

Modern AI agents (Cursor, Windsurf, Claude Code, Gemini with tools) are now equipped with **Auto-Discovery**. If your prompt mentions keywords like "Write tests", "Fix accessibility", or "Check security", the AI will *autonomously* read the relevant standard files below without you needing to manually `@reference` them.

Manual `@reference` is only required if you are using a standard web chatbot (without file-reading tools) or if you want to strictly force the AI to read a specific cookbook.

The root instruction file for each agent should still be the primary entrypoint; these references are task-specific additions, not a shared instruction surface.

## Local Skills Implemented Here

The following on-demand skill capsules are available in [skills/](./skills/):

- [coding-standards](./skills/coding-standards/SKILL.md)
- [tdd-workflow](./skills/tdd-workflow/SKILL.md)
- [verification-loop](./skills/verification-loop/SKILL.md)
- [security-review](./skills/security-review/SKILL.md)
- [codebase-onboarding](./skills/codebase-onboarding/SKILL.md)
- [context-budget](./skills/context-budget/SKILL.md)
- [documentation-lookup](./skills/documentation-lookup/SKILL.md)
- [browser-qa](./skills/browser-qa/SKILL.md)
- [prompt-optimizer](./skills/prompt-optimizer/SKILL.md)
- [skill-scout](./skills/skill-scout/SKILL.md)
- [codex-vscode](./skills/codex-vscode/SKILL.md)
- [large-file-refactor](./skills/large-file-refactor/SKILL.md)
- [accessibility](./skills/accessibility/SKILL.md)
- [api-design](./skills/api-design/SKILL.md)
- [architecture-decision-records](./skills/architecture-decision-records/SKILL.md)
- [database-migrations](./skills/database-migrations/SKILL.md)
- [error-handling](./skills/error-handling/SKILL.md)
- [git-workflow](./skills/git-workflow/SKILL.md)
- [production-audit](./skills/production-audit/SKILL.md)
- [search-first](./skills/search-first/SKILL.md)
- [skill-stocktake](./skills/skill-stocktake/SKILL.md)
- [rules-distill](./skills/rules-distill/SKILL.md)

---

## By Task Type

### Security-Sensitive Code
> Auth, payments, encryption, user data, API keys

```
@ai-agent-standards/risk-management/security-constraints.md
```

### RAG / AI Pipeline
> Vector DB retrieval, LLM generation, embeddings

```
@ai-agent-standards/prompts/sample-use-cases/rag-implementation-cookbook.md
```

### Writing a Complex Prompt
> Multi-step tasks, strict constraints, specific output format

```
@ai-agent-standards/prompts/PROMPT-TEMPLATE.md
```

### Code Review / Audit
> Reviewing AI-generated code before merge

```
@ai-agent-standards/quality-control/audit-ai-code-full.md
@ai-agent-standards/quality-control/code-review-checklist.md
```

### Large File Refactor
> Splitting large files, reducing monolithic modules, extracting React hooks/components, or bringing files closer to the 300 LOC guideline

```
@skills/large-file-refactor/SKILL.md
```

### Detecting Hallucinations
> AI imports fake libraries, calls non-existent APIs

```
@ai-agent-standards/quality-control/hallucination-detection.md
```

### Database Migrations
> Schema changes, data migration, rollback strategy

```
@ai-agent-standards/prompts/sample-use-cases/database-migration.md
```

### Caching & Performance
> Redis, cache invalidation, query optimization

```
@ai-agent-standards/prompts/sample-use-cases/refactor-cache-strategy.md
```

### Unit Test Generation
> Writing tests for existing or new code

```
@ai-agent-standards/prompts/sample-use-cases/generate-unit-tests.md
```

### Security Audit
> Scanning for vulnerabilities in existing code

```
@ai-agent-standards/prompts/sample-use-cases/security-audit.md
```

### API Development
> REST endpoints, rate limiting, authentication

```
@ai-agent-standards/prompts/sample-use-cases/create-api-with-rate-limiting.md
```

### Mobile Development
> Android, iOS, Flutter, React Native - lifecycle, permissions, offline

```
@ai-agent-standards/prompts/sample-use-cases/mobile-development-cookbook.md
```

### Documentation & Changelogs
> Writing README, API Specs, Docstrings, or Changelogs

```
@ai-agent-standards/engineering-practices/DOCUMENTATION_STANDARDS.md
```

### Release & Branching Strategy
> Bumping versions (SemVer), Gitflow, or pre-release checks

```
@ai-agent-standards/engineering-practices/RELEASE_PROCESS.md
```

### Testing Strategy & TDD
> Setting up test pyramids, coverage bounds, or adhering to FIRST principles

```
@ai-agent-standards/engineering-practices/TESTING_STANDARDS.md
```

### Performance & DB Optimization
> Caching strategy, N+1 queries, concurrency, response time budgets

```
@ai-agent-standards/engineering-practices/NON_FUNCTIONAL_REQUIREMENTS.md
```

### Industry Compliance
> OWASP, NIST, or CISA alignment checks

```
@ai-agent-standards/compliance/COMPLIANCE.md
```

### UI Accessibility (A11Y)
> Reviewing HTML/React for WCAG 2.1 AA, ARIA, and Keyboard Navigation

```
@ai-agent-standards/compliance/A11Y_CHECKLIST.md
```

---

## Multi-Agent Setup

Assign the appropriate file as system instructions for each agent:

| Agent | File to load |
|-------|-------------|
| Coder | `@ai-agent-standards/multi-agent/coder-agent.md` |
| Test | `@ai-agent-standards/multi-agent/test-agent.md` |
| Reviewer | `@ai-agent-standards/multi-agent/reviewer-agent.md` |
| Documentation | `@ai-agent-standards/multi-agent/documentation-agent.md` |

---

## Combining References

For complex tasks, combine multiple references:

```
# Example: Build a secure API with tests

@ai-agent-standards/risk-management/security-constraints.md
@ai-agent-standards/prompts/sample-use-cases/create-api-with-rate-limiting.md
@ai-agent-standards/prompts/PROMPT-TEMPLATE.md

Build POST /api/v1/register with email validation,
bcrypt password hashing, and JWT response.
Include unit tests and Self-Check report.
```

---

## Verify Agent Skills

At any time, ask your agent:

> **"What coding standards are you following?"** or type **`/standards`**

Expected:
> [OK] AI-Coding-Standards v2.6.1 with 6 Core Principles active.
