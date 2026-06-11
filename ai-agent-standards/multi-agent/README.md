# Multi-Agent Framework

**Status:** [OK] Implemented (v3.0.2)
**Framework:** AI-Coding-Standards v3.0.2 with 6 Core Principles

---

## Architecture

4 specialized agents with strict role isolation. Human engineer retains final authority.

```
Coder Agent -> Test Agent -> Reviewer Agent -> Human Engineer
                                                   v
                                         Documentation Agent
```

---

## Agents

| Agent | File | Scope | Forbidden |
|-------|------|-------|-----------|
| **Coder** | [coder-agent.md](./coder-agent.md) | Write implementation code | DB schemas, env vars, architecture decisions |
| **Test** | [test-agent.md](./test-agent.md) | Write tests independently | Modify production code |
| **Reviewer** | [reviewer-agent.md](./reviewer-agent.md) | Security audit & optimize | Add new features, change business logic |
| **Documentation** | [documentation-agent.md](./documentation-agent.md) | API docs, READMEs, changelogs | Modify source code or tests |

---

## How to Use

### Single-Agent (default)
No setup needed. Your AI agent loads rules from its own root instruction file (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `COPILOT.md`, `.instructions.md`, etc.) automatically.

There is no shared cross-agent skill layer in this framework; each agent uses its own Markdown instruction surface.

### Multi-Agent
Assign the appropriate file as system instructions for each agent in your orchestration tool:

```
Agent A -> load coder-agent.md as system prompt
Agent B -> load test-agent.md as system prompt
Agent C -> load reviewer-agent.md as system prompt
Agent D -> load documentation-agent.md as system prompt
```

Works with: Claude API, OpenAI API, LangChain, CrewAI, or any tool that accepts custom system prompts.

---

## Key Rules (All Agents)

1. **Human engineer has final authority** - no agent can override
2. **6 Core Principles enforced** - Think, Simplicity, Surgical, Goal-Driven, DRY, Code Organization
3. **12 security constraints active** - see [security-constraints.md](../risk-management/security-constraints.md)
4. **Self-Check report required** - every agent output includes verification

---

## Reference

- [SKILL-REFERENCE.md](../../SKILL-REFERENCE.md) - Quick lookup for all skills
- [security-constraints.md](../risk-management/security-constraints.md) - 12 non-negotiable security rules
- [karpathy/principles.md](../../karpathy/principles.md) - The 6 principles
