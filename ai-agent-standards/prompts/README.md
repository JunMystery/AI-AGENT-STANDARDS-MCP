# Prompt Library - Usage Guide

This directory contains standardized prompt templates for common software development use cases.

---

## 📋 Directory Structure

```
prompts/
├── README.md                          (this file)
├── HEADER-TEMPLATE.yaml               (YAML header template)
├── PROMPT-TEMPLATE.md                 (standard prompt template)
├── indexed-by-category.md             (categorized index)
└── sample-use-cases/
    ├── create-api-with-rate-limiting.md
    ├── refactor-cache-strategy.md
    ├── generate-unit-tests.md
    ├── security-audit.md
    └── database-migration.md
```

---

## 🚀 How to Use Prompts

### 1. Find the Right Prompt
- See [`indexed-by-category.md`](indexed-by-category.md) to find your use case
- Or browse [`sample-use-cases/`](sample-use-cases/) for direct examples

### 2. Copy the Prompt Template
```bash
# Copy prompt content into your IDE or chat interface
# Example: Copy contents of create-api-with-rate-limiting.md
```

### 3. Customize for Your Project
- Update `[CONTEXT]` section with your specific tech stack
- Modify constraints if needed (e.g., different framework)
- Keep `[TASK]` as-is or customize as needed

### 4. Send to AI & Process Output
- Paste prompt into Claude / ChatGPT / Copilot
- AI will run Self-Check (if instructed in prompt)
- See [`quality-control/self-check-report-template.md`](../quality-control/self-check-report-template.md) to verify

### 5. Save Results
Log: `prompt_id`, `prompt_version`, `ai_iteration_count` in your project's task tracker

---

## 📝 Header Template (YAML)

Each prompt file must begin with:

```yaml
---
id: PROMPT-001                                    # Unique ID
version: 1.0                                      # Version
author: [Engineer name]                           # Creator
last_updated: 2026-05-12                         # Last update date
applicable_stack: [React, Node.js, PostgreSQL]   # Applicable tech stack
category: API_Development                        # Category
difficulty: Intermediate                         # Difficulty: Simple/Intermediate/Complex
---
```

---

## 🎯 Standard Prompt Template (Section III.2)

```markdown
### [CONTEXT]
- Tech stack: [e.g., React v18, Node.js, PostgreSQL]
- Current state: [Brief technical description]
- Schema/Interfaces: [Provide data structures]

### [TASK]
- Objective: [Detailed & independent single feature description]
- Acceptance Criteria: [List of clear conditions]

### [CONSTRAINTS]
- FORBIDDEN ACTIONS: [e.g., Do not modify .env files]
- REQUIRED: [e.g., Try-catch mandatory, add comments]
- Process: Must run Self-Check (Section III.4)

### [OUTPUT FORMAT]
- [e.g., Code changes only, with Self-Check report]
```

---

## ✨ Best Practices

### Writing New Prompts

1. **Single-Task Prompting:** 1 prompt = 1 clear feature
   - ❌ Wrong: "Build the entire authentication module"
   - ✅ Right: "Create POST /login endpoint with JWT + rate limiting"

2. **Optimal Context:** Provide enough context but not too much
   - Include schema, interfaces, existing code snippets
   - Don't paste entire codebase (wastes tokens)

3. **Clear Constraints:** List what AI must NOT do
   - "Do not import libraries outside [list]"
   - "Must use [specific pattern]"

4. **Specific Output Format:** Define expected format
   - "Code only, no explanations"
   - "JSON format + Self-Check report"

### Using Prompts

1. **Update YAML header** with specific info (author, version)
2. **Test prompt** on one model first (e.g., Claude)
3. **Save prompt version** when proven effective
4. **Update indexed-by-category.md** for new prompts

---

## 📊 Prompt Library Stats

| Type | Count | Status |
|------|-------|--------|
| Sample Use Cases | 5 | ✓ Ready |
| Template Templates | 2 | ✓ Ready |
| Advanced Prompts | TBD | Upcoming |

---

## 🔄 Prompt Lifecycle

```
1. CREATE (Engineer creates new prompt)
   ↓
2. TEST (Try on model, verify output)
   ↓
3. SAVE (Commit to repo, update indexed-by-category.md)
   ↓
4. TRACK (Log prompt_id when used in tasks)
   ↓
5. ITERATE (Improve based on metrics)
```

---

## 📋 Available Use Cases

1. **`create-api-with-rate-limiting.md`** — API endpoint + auth + rate limit
2. **`refactor-cache-strategy.md`** — Caching optimization & performance
3. **`generate-unit-tests.md`** — Auto-generate unit tests
4. **`security-audit.md`** — Security vulnerability check
5. **`database-migration.md`** — Safe schema migration

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|---------|
| AI output doesn't match | Review [CONSTRAINTS] section, may need more detail |
| Output too long | Add "Output Format: Code only, no explanations" |
| AI doesn't follow pattern | Add specific examples in context |
| Same error repeats | Update prompt, save new version, track metrics |

---

## 🔗 Reference

- Template: [`PROMPT-TEMPLATE.md`](PROMPT-TEMPLATE.md)
- Header: [`HEADER-TEMPLATE.yaml`](HEADER-TEMPLATE.yaml)
- Index: [`indexed-by-category.md`](indexed-by-category.md)
- Self-Check: [`../quality-control/self-check-report-template.md`](../quality-control/self-check-report-template.md)
- Full Standards: Original documentation "AI Agent Coding — Sections II & III"

---

**Note:** This prompt library will expand as experience grows. Contribute new prompts to this directory & commit to the repo.
