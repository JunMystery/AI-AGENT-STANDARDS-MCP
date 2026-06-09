# Quality Control Pipeline

4-layer quality control system for all AI-generated code.

---

## 🔄 Pipeline Overview

```
[ REQUEST FROM ENGINEER ]
          ↓
┌─────────────────────────────────────────────────┐
│ 1. AI GENERATE - Generate code                   │
├─────────────────────────────────────────────────┤
│ 2. AI SELF-CHECK - Self-verification (Required)  │
│    - Security, duplication, error handling       │
│    - Regression risk, best practices             │
├─────────────────────────────────────────────────┤
│ 3. AI SELF-FIX - Auto-fix (Max 2 rounds)        │
│    - If Self-Check fails → Auto fix              │
│    - If still fails → Report & escalate          │
├─────────────────────────────────────────────────┤
│ 4. OUTPUT - Final code + report                  │
└─────────────────────────────────────────────────┘
          ↓
[ HUMAN GATE - CODE REVIEW BY ENGINEER ]
  ├─ Review with: code-review-checklist.md
  ├─ Audit with: audit-ai-code-full.md
  └─ Decision:
      [✓ APPROVE] → Merge + Checkpoint
      [✗ REJECT/REWORK] → Back to step 1
```

---

## 📋 Key Files in This Folder

| File | Purpose | Required? |
|------|---------|-----------|
| [`self-check-report-template.md`](self-check-report-template.md) | Self-check report template | ✓ **YES** |
| [`code-review-checklist.md`](code-review-checklist.md) | Code review checklist | ✓ **YES** |
| [`audit-ai-code-full.md`](audit-ai-code-full.md) | Detailed AI output audit | ✓ **YES** |
| [`hallucination-detection.md`](hallucination-detection.md) | Detecting AI errors | ✓ **YES** |
| [`ci-cd-gates.md`](ci-cd-gates.md) | CI/CD integration rules | ⚠️ Optional |

---

## ✅ Self-Check Report (AI-Generated)

**AI must produce this report before any output.**

See template: [`self-check-report-template.md`](self-check-report-template.md)

```markdown
### AI Self-Check Report
Prompt ID: PROMPT-001
Checklist:
- [x] Complies with Non-Negotiable Constraints
- [x] Code duplication = 0
- [x] Security check passed (no SQL injection, XSS)
- [x] Required error handling (try-catch, null checks)
- [x] Regression risk: LOW
- [x] Self-Fix rounds: 1 (if initial errors found)
Notes: [Optional - AI comments]
```

---

## 👤 Code Review Checklist (Human)

**Engineer must verify before merging AI code.**

See full checklist: [`code-review-checklist.md`](code-review-checklist.md)

### Quick Version
- [ ] Self-Check report completed?
- [ ] Code matches prompt requirements?
- [ ] No hardcoded secrets/credentials?
- [ ] Try-catch & error handling OK?
- [ ] Test coverage >= 80%?
- [ ] Comments explain complex logic?
- [ ] Backward compatibility maintained?

---

## 🔍 Audit AI Code (Detailed)

**For senior reviewers or security-sensitive modules.**

See details: [`audit-ai-code-full.md`](audit-ai-code-full.md)

### Areas Audited
- Security vulnerabilities (SQLi, XSS, CSRF)
- Performance bottlenecks
- Memory leaks, dangling references
- Code duplication & dead code
- Error handling completeness
- Test quality & coverage

---

## ⚠️ Hallucination Detection

**Detecting when AI generates non-existent code.**

Warning signs: [`hallucination-detection.md`](hallucination-detection.md)

```
❌ Import non-existent library
❌ Call non-existent API method
❌ Algorithm logic violates constraints
❌ Reference non-existent file/class
```

**How to fix:** Verify with official docs, update prompt, iterate

---

## 🚀 CI/CD Gates (Automated)

**Integrate with CI/CD pipeline for automated checks.**

See: [`ci-cd-gates.md`](ci-cd-gates.md)

```bash
# Example GitHub Actions
- Run ESLint + Prettier
- Run unit tests (jest)
- Run SAST (SonarQube, Snyk)
- Check test coverage >= 80%
- Flag: AI-Assisted code (special handling)
```

---

## 📊 Pipeline Metrics

Track from Self-Check Reports:
- **Defect Escape Rate:** % of errors not detected by AI
- **Human Review Time:** Time spent reviewing code
- **Iteration Count:** Average Self-Fix rounds
- **Hallucination Rate:** % of output containing hallucinations

---

## 🔗 Integration Points

| With | Purpose |
|------|---------|
| Jira | Label task `[AI-Assisted]`, attach Self-Check report |
| Git | Commit hooks validate Self-Check presence |
| Metrics System | Track review time, iteration count |
| Alerting | Flag high defect rate or regression |

---

## 🎯 Best Practices

1. **Always run Self-Check** — no exceptions
2. **Code review is mandatory** — humans make the final decision
3. **Track metrics** — identify which patterns are failing
4. **Document hallucinations** — improve prompts
5. **Escalate when needed** — see [`risk-management/escalation-workflow.md`](../risk-management/escalation-workflow.md)

---

## 📝 Timeline

Total time from prompt → merged code:

```
1. Prompt → AI Generate:        5-30 min (depends on complexity)
2. Self-Check:                  < 5 min
3. Self-Fix (if needed):        5-10 min (max 2 rounds)
4. Human Review:                10-30 min
─────────────────────────────────────
Total:                          20-75 min
```

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|---------|
| AI fails Self-Check 3+ times | Escalate, review prompt, possibly code manually |
| Reviewer rejects frequently | Improve prompt clarity, add more constraints |
| High hallucination rate | Update prompt with more doc references |
| CI/CD gate fails | Check linter rules, coverage threshold |

---

## 📌 New Setup Checklist

- [ ] Created team Slack channel `#ai-code-review`?
- [ ] Set up Jira label `[AI-Assisted]`?
- [ ] Briefed team on Self-Check requirement?
- [ ] Updated CI/CD pipeline (if applicable)?
- [ ] Assigned primary reviewer?

---

**Reference:** Section III.4 — Quality Control Pipeline (original documentation)

**Last updated:** 2026-05-12
