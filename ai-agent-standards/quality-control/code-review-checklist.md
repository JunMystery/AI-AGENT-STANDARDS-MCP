# Code Review Checklist - AI Code Review Guide

**Mandatory when reviewing AI-generated code.**

---

## 🎯 Karpathy Principles Validation (Check First!)

**These 6 principles prevent the most common AI coding mistakes. Validate all before approving.**

### Principle 1: Think Before Coding ✓
- [ ] Were assumptions stated explicitly in the prompt?
- [ ] If multiple interpretations existed, were all presented?
- [ ] Success criteria were defined upfront (not vague)?
- [ ] No "creative reinterpretation" of the request?
- [ ] **→ If any fail, request clarification & re-implementation**

### Principle 2: Simplicity First ✓
- [ ] Code directly solves the problem—no extra features?
- [ ] No speculative abstractions or "future-proofing"?
- [ ] No defensive error handling for impossible cases?
- [ ] Could this be written simpler? (If yes, request changes)
- [ ] **→ If overly complex, request simplification**

### Principle 3: Surgical Changes ✓
- [ ] Git diff shows focused, minimal changes?
- [ ] No unrelated reformatting or refactoring?
- [ ] Pre-existing issues mentioned but NOT fixed?
- [ ] Only orphans created BY this change are removed?
- [ ] Every changed line traces directly to the request?
- [ ] **→ If scope-creeping, request surgical rework**

### Principle 4: Goal-Driven Execution ✓
- [ ] Success criteria from prompt are clearly met?
- [ ] Verification steps were performed?
- [ ] Self-Check Report documents verification results?
- [ ] Tests pass? Metrics improved? Observable outcome verified?
- [ ] **→ If criteria not met, ask AI to iterate**

### Principle 5: DRY & Reusability ✓
- [ ] No duplicated UI, logic, configs, schemas, types, or test setup?
- [ ] Existing helpers, components, and patterns were reused where appropriate?
- [ ] Any new abstraction is justified by real reuse, not speculation?
- [ ] **→ If duplication exists, request consolidation**

### Principle 6: Code Organization ✓
- [ ] Code lives in the correct layer/module for the existing architecture?
- [ ] No monolithic files or unrelated logic added to catch-all modules?
- [ ] Names are clear, general, and consistent with nearby project structure?
- [ ] **→ If organization is weak, request module/layer cleanup**

**⚠️ Decision:** If ANY principle fails → **Request changes**. All 6 must pass.

---

## 🎯 Quick Checklist (5 min)

**Check this list first:**

- [ ] **Self-Check Report** present & complete?
- [ ] **Requirements match?** Code fulfills the task requirements?
- [ ] **Security:** No hardcoded secrets (API keys, tokens, passwords)?
- [ ] **Error Handling:** Try-catch present? Null checks?
- [ ] **Tests:** Unit tests present? Coverage >= 80%?
- [ ] **No Breaking Changes:** Backward compatible?

**If all PASS → Approve. If any FAIL → Request changes.**

---

## 📋 Full Checklist (10-15 min — detailed review)

### Section 1: Alignment with Requirements
- [ ] Code implements exactly what was asked in prompt?
- [ ] No extra / unnecessary features added?
- [ ] All acceptance criteria from prompt are met?
- [ ] Task-specific constraints followed?

### Section 2: Security (CRITICAL 🔴)

**FORBIDDEN — Reject immediately if found:**
- [ ] ✗ NO hardcoded API keys, passwords, tokens
- [ ] ✗ NO SQL injection vulnerabilities (raw query strings)
- [ ] ✗ NO unvalidated user input
- [ ] ✗ NO console.log with sensitive data
- [ ] ✗ NO disabled security headers

**MUST HAVE:**
- [ ] ✓ Input validation / sanitization
- [ ] ✓ Parameterized SQL queries
- [ ] ✓ Error messages don't leak info
- [ ] ✓ Sensitive operations logged appropriately

**Reference:** [`../risk-management/security-constraints.md`](../risk-management/security-constraints.md)

### Section 3: Error Handling
- [ ] Try-catch blocks for risky operations?
- [ ] Null/undefined checks present?
- [ ] Fallback strategies defined?
- [ ] Error logging includes context (not PII)?
- [ ] Graceful degradation on failure?

### Section 4: Code Quality & Style
- [ ] Matches project's coding standards (naming, formatting)?
- [ ] ESLint / Prettier compliant?
- [ ] TypeScript: proper typing (no `any`)?
- [ ] Functions under 50 lines? (or justified)
- [ ] Comments explain "why", not "what"?
- [ ] No console.debug() left in production code?

### Section 5: Testing & Coverage
- [ ] Unit tests included for new functions?
- [ ] Test coverage >= 80% for new code?
- [ ] Tests cover edge cases & error paths?
- [ ] Mocks used appropriately (not over-mocked)?
- [ ] Test names are descriptive?

### Section 6: Performance & Scalability
- [ ] No N+1 database queries?
- [ ] Caching strategy implemented (Redis, HTTP)?
- [ ] Concurrency handled safely (no race conditions)?
- [ ] Performance budgets met (e.g. response time < 200ms)?
- [ ] Loops optimized (no unnecessary iteration)?
- [ ] Memory usage reasonable?
- [ ] No blocking operations on main thread?

### Section 7: Maintainability & Documentation
- [ ] Complex logic has comments?
- [ ] Function parameters documented (types, meaning)?
- [ ] Dependencies are explicit (imports at top)?
- [ ] Dead code removed?
- [ ] No hardcoded values (use constants/config)?

### Section 8: Architecture & Design
- [ ] Code follows project's architecture pattern (MVC, layered, etc)?
- [ ] Responsibilities properly separated?
- [ ] DRY principle applied (no duplication)?
- [ ] Design patterns used appropriately (not over-engineered)?
- [ ] Coupling minimized, cohesion maximized?

### Section 9: Integration & Dependencies
- [ ] All imports resolved (packages exist)?
- [ ] Version conflicts avoided?
- [ ] External APIs called correctly?
- [ ] Configuration injected (not hardcoded)?
- [ ] No circular dependencies?

### Section 10: Backward Compatibility & Risk
- [ ] Breaking changes avoided or documented?
- [ ] Database migrations have rollback paths?
- [ ] API changes backward compatible?
- [ ] Deprecation warnings added if needed?
- [ ] Regression risk: LOW / MEDIUM / HIGH?

### Section 11: Compliance & Accessibility (A11Y)
- [ ] OWASP LLM top 10 risks mitigated?
- [ ] Follows WCAG 2.1 AA accessibility standards?
- [ ] Semantic HTML used instead of nested divs?
- [ ] ARIA labels and keyboard navigation supported?

---

## 🚨 Red Flags (Auto Reject if Found)

**Reject immediately, ask for rewrite:**

| 🚫 Issue | Reason |
|---------|--------|
| Hardcoded secrets | Security risk |
| No error handling | Will crash in production |
| No input validation | Vulnerability |
| >90% test coverage gaps | Can't verify correctness |
| SQL injection pattern | Critical security |
| Console.log() with secrets | Info leak |
| Breaking API changes undocumented | Will break clients |
| Infinite loops or memory leaks | Performance/stability |

---

## 🟡 Yellow Flags (Request Changes)

**Ask for improvement, don't block if justified:**

| ⚠️ Flag | Improvement |
|--------|-------------|
| Functions > 100 lines | Refactor into smaller functions |
| No comments on complex logic | Add explanatory comments |
| Over-engineered design | Simplify if possible |
| Inconsistent naming | Align with project conventions |
| Duplicated code | Extract to utility function |

---

## ✅ Approved Signs

**Good code has these characteristics:**

- ✓ Clear purpose, solves stated problem
- ✓ Proper error handling
- ✓ Security constraints followed
- ✓ Tests included & passing
- ✓ Follows project conventions
- ✓ Maintainable & documented
- ✓ Backward compatible
- ✓ Reviewable complexity

---

## 📝 Decision Template

```markdown
## Code Review Decision

**Reviewer:** [Your name]
**Date:** [YYYY-MM-DD]
**Prompt ID:** PROMPT-XXX

### Verdict: [APPROVE / REQUEST CHANGES / REJECT]

---

### Approved Items
- [ ] Security constraints met
- [ ] Error handling complete
- [ ] Tests > 80% coverage
- [ ] No breaking changes

---

### Issues Found

#### 🔴 Critical (Must fix)
1. [Issue 1] - [Why it matters]
2. [Issue 2]

#### 🟡 Minor (Nice to fix)
1. [Issue 1]
2. [Issue 2]

---

### Comments
[Additional context or suggestions]

---

### Next Steps
- [ ] Author addresses critical issues
- [ ] Resubmit for review
- [ ] Merge after approval
```

---

## 💡 Tips for Reviewers

1. **Read Self-Check Report first** - see what AI already checked
2. **Focus on critical items** - security, errors, tests
3. **Test locally if possible** - don't just read code
4. **Be specific** - "Add try-catch on line 42" not "Add error handling"
5. **Approve if concerns addressed** - don't be perfectionist
6. **Document decision** - helps with metrics & learning

---

## 🔄 If Multiple Reviewers

**For sensitive modules (auth, payments, security):**
- [ ] Requires 2 independent reviews
- [ ] Reviews must agree on critical issues
- [ ] Senior engineer has final say on disputes

---

## 📊 Metrics to Track

**From each review:**
- Time spent
- # of critical issues found
- # of iteration rounds needed
- Defect escape rate (issues found after merge)

---

## 🔗 Related Resources

- Self-Check Template: [`self-check-report-template.md`](self-check-report-template.md)
- Full Audit: [`audit-ai-code-full.md`](audit-ai-code-full.md)
- Security Constraints: [`../risk-management/security-constraints.md`](../risk-management/security-constraints.md)
- Error Reference: [`../reference/error-reference-complete.md`](../reference/error-reference-complete.md)

---

**Checklist Version:** 1.0 | **Last Updated:** 2026-05-12
