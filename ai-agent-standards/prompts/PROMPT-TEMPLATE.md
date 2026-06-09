---
id: PROMPT-TEMPLATE
version: 1.0
author: [Your Name]
last_updated: 2026-05-12
applicable_stack: [NodeJS, React, etc]
category: General
difficulty: Intermediate
---

# Standard Prompt Template

Use this template as the basis for every new prompt.

---

## 📋 Structure

### [CONTEXT]
Provide necessary information about:
- **Tech stack:** Framework, libraries, versions
- **Current state:** Brief technical description
- **Schema/Interfaces:** Relevant data structures
- **Existing Code:** Code snippets for reference if needed

*Example:*
```
- Tech stack: React v18, Node.js 18, PostgreSQL 14
- Current state: Auth module exists, need to add role-based access control
- Schema: User { id, email, role }, Role { id, name, permissions }
```

### [TASK]
Describe a single feature in detail & independently:
- **Objective:** What to create/modify
- **Input/Output:** Input data & expected output
- **Acceptance Criteria:** List of clear conditions

*Example:*
```
- Objective: Create endpoint POST /api/posts with validation
- Input: { title: string, content: string, userId: number }
- Output: { id, title, content, userId, createdAt }
- Acceptance:
  [x] Title max 200 chars, content max 5000 chars
  [x] userId must exist in DB
  [x] Return 400 if input invalid, 201 if success
```

### [CONSTRAINTS]
**Non-negotiable baseline:**
- **FORBIDDEN ACTIONS:** What AI must NOT do
  - ❌ Do not modify .env files
  - ❌ Do not import libraries outside [list]
  - ❌ Do not use recursive approach for large datasets
- **REQUIRED:** What AI MUST do
  - ✓ Try-catch mandatory for async operations
  - ✓ Input validation with zod/joi mandatory
  - ✓ 80%+ test coverage mandatory
- **Process:**
  - ✓ Must run Self-Check before output (Section III.4)
  - ✓ Output must include Self-Check report

*Example:*
```
FORBIDDEN:
- Do not modify database schema
- Do not use any type in TypeScript
- Do not hardcode API endpoints

REQUIRED:
- Try-catch for all API calls
- Validate input before processing
- Log errors & return meaningful messages

Process:
- Run Self-Check checklist before outputting code
- Include Self-Check Report
```

### [OUTPUT FORMAT]
Clearly define expected format & presentation:
- Code only / Code + explanation?
- Single file / Multiple files?
- JSON / Markdown / Plain text?
- Include Self-Check report?

*Example:*
```
- Output only changed code (no lengthy explanations)
- Format: Single TypeScript file
- Include: Self-Check report (checklist style)
- Code format: ESLint + Prettier compatible
```

---

## ✅ Self-Check Checklist

**AI must complete before producing output:**

```markdown
### AI Self-Check Report
- Prompt ID: [ID]
- Checklist:
  [ ] Complies with Non-Negotiable Constraints (Security, No hardcode)?
  [ ] Code duplication = 0?
  [ ] Security check passed (SQLi, XSS, info leak)?
  [ ] Exception handling (null, timeout, errors)?
  [ ] Regression risk low (no breaking existing code)?
- Notes: [Optional]
```

---

## 🎯 Best Practices

1. **Clarity:** Each section clear and unambiguous
2. **Conciseness:** Brief, provide enough info but not too much
3. **Specificity:** Include examples, code snippets, not just descriptions
4. **Testability:** Output must be verifiable
5. **Traceability:** Record context for later debugging if needed

---

## 📊 Template Structure

| Section | Required? | Length |
|---------|-----------|--------|
| CONTEXT | ✓ | 5-10 lines |
| TASK | ✓ | 5-10 lines |
| CONSTRAINTS | ✓ | 10-15 lines |
| OUTPUT FORMAT | ✓ | 3-5 lines |
| Self-Check | ✓ | Auto-generated |

---

## 🔗 Reference

- Full Standards: Original documentation "AI Agent Coding — Section III.2"
- Sample Prompts: [`sample-use-cases/`](sample-use-cases/)
- Self-Check Report: [`../quality-control/self-check-report-template.md`](../quality-control/self-check-report-template.md)

---

**Note:** Copy this template & fill in details for your specific use case. Don't forget the YAML header at the top!
