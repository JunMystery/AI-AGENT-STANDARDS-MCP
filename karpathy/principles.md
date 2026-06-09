# Karpathy Coding Principles

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

---

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" -> "Write tests for invalid inputs, then make them pass"
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. DRY & Reusability

**Never duplicate UI, logic, configurations, types, or any code. Always use shared systems.**

- **UI/Styling & Assets:** Always utilize the project's existing design system, shared assets, or global CSS variables. Do not hardcode disjointed styles or create duplicate UI components.
- **Logic & Functions:** Extract any logic or calculations used 2+ times into pure, reusable functions within the project's established shared directories. Do not repeat the same logic blocks.
- **Configurations & Metadata:** Centralize environment variables, configuration schemas, build scripts, and metadata. Avoid duplicating configurations across environments or services.
- **Types & Schemas:** Define models, interfaces, and schemas in shared folders. Reuse and extend existing types instead of recreating them.
- **Tests & Mock Data:** Share test utilities, mock data factories, and assertion helpers. Do not duplicate test setups or mock data structures.

## 6. Code Organization

**Don't put all code in one file. Separate into multiple files with general names.**

- **File Size Limit:** Keep files focused and readable. As a guideline, split files when they exceed **300 lines of code (LOC)**.
- **Concern Separation:** Separate distinct concerns (e.g. data schema, request handling, business logic, UI, utilities) into separate directories or files.
- **General & Suffix Naming:** Group similar functions in files with general, purpose-driven names and consistent suffixes (e.g. `auth.service.ts`, `math.helper.ts`, `user.model.ts`).
- **Co-locate Related Files:** Keep tests, styles, and local helpers close to their main component or module rather than in distant folders.

---

## How to Know These Guidelines Are Working

- **Fewer unnecessary changes in diffs** - Only requested changes appear
- **Fewer rewrites due to overcomplication** - Code is simple the first time
- **Clarifying questions come before implementation** - Not after mistakes
- **Clean, minimal PRs** - No drive-by refactoring or "improvements"

---

## Attribution

These principles are derived from [Andrej Karpathy's post](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls, adapted and integrated by the [andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) project (MIT License).
