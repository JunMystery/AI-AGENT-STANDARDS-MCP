# AI Self-Check Report Template

**Self-check report template — AI must fill in before producing output**

*Appendix C from original documentation | Updated with 6 Core Principles*

---

## 📋 Template

```markdown
## AI Self-Check Report

**Metadata:**
- Prompt ID: PROMPT-XXX
- Prompt Version: 1.0  
- Task: [Brief description of what was built]
- Date: [YYYY-MM-DD HH:MM]
- AI Iteration Count: [Number of Self-Fix rounds]

---

## 🎯 6 Core Principles Verification

### Principle 1: Think Before Coding ✓
- [ ] Assumptions stated explicitly in prompt or clarified before implementation?
- [ ] If ambiguous, were multiple interpretations presented?
- [ ] Success criteria were defined upfront (not vague)?
- [ ] Clarifying questions asked BEFORE coding started?
- **Status:** ✓ PASS / ⚠️ PARTIAL / ❌ FAIL
- **Notes:** [If not all pass, explain]

### Principle 2: Simplicity First ✓
- [ ] Code directly solves stated problem—no extra features?
- [ ] No speculative abstractions or "future-proofing"?
- [ ] No defensive error handling for impossible cases?
- [ ] Code could NOT reasonably be written simpler?
- [ ] Total lines: [count] | Necessary? Yes
- **Status:** ✓ PASS / ⚠️ PARTIAL / ❌ FAIL
- **Notes:** [If not all pass, explain]

### Principle 3: Surgical Changes ✓
- [ ] Git diff is minimal and focused?
- [ ] Every changed line traces directly to the request?
- [ ] No unrelated refactoring or reformatting?
- [ ] Pre-existing issues mentioned but not fixed (unless they're orphans from my changes)?
- [ ] Only orphans created BY these changes are removed?
- **Status:** ✓ PASS / ⚠️ PARTIAL / ❌ FAIL
- **Notes:** [If not all pass, explain]

### Principle 4: Goal-Driven Execution ✓
- [ ] Success criteria from prompt are clearly met?
- [ ] Verification steps were performed?
- [ ] Tests passing? [Count] / [Total] ✓
- [ ] Metrics verified? [If applicable: metric = before/after]
- [ ] Observable outcome confirmed?
- **Status:** ✓ PASS / ⚠️ PARTIAL / ❌ FAIL
- **Notes:** [If not all pass, explain]

### Principle 5: DRY & Reusability ✓
- [ ] No hardcoded or disjointed styles added?
- [ ] Existing design system components utilized?
- [ ] Logic duplicated across multiple files? No
- [ ] Shared logic extracted into pure, reusable functions?
- **Status:** ✓ PASS / ⚠️ PARTIAL / ❌ FAIL
- **Notes:** [If not all pass, explain]

**Overall Principles Assessment:** ✓ ALL PASS / ⚠️ MINOR ISSUES / ❌ REQUIRES REWORK

---

### Checklist ✓

**Security & Architecture:**
- [ ] Complies with Non-Negotiable Constraints?
  - No hardcoded secrets
  - Input validation implemented
  - Error handling complete
- [ ] Code compatible with current architecture?
- [ ] No security violations (SQLi, XSS, CSRF)?

**Code Quality:**
- [ ] Code duplication = 0?
- [ ] Complexity score acceptable?
- [ ] Dead code / unused imports = 0?
- [ ] All variables properly typed (TypeScript)?

**Error Handling:**
- [ ] Try-catch mandatory for async/DB operations?
- [ ] Null/undefined checks present?
- [ ] Error messages do not leak sensitive data?
- [ ] Logging appropriate (not verbose)?

**Testing:**
- [ ] Test coverage >= 80% (for new code)?
- [ ] Edge cases covered?
- [ ] Mock setup correct?

**Performance & Regression:**
- [ ] Database queries optimized (no N+1)?
- [ ] No memory leaks / dangling references?
- [ ] Regression risk assessment: LOW / MEDIUM / HIGH?
- [ ] Backward compatibility maintained?

---

### Self-Fix History

**Round 1:** [If needed - what was fixed]
- Issue: [Describe]
- Fix: [What changed]

**Round 2:** [If needed]
- Issue: [Describe]
- Fix: [What changed]

---

### Notes & Warnings

**Potential Issues:**
- [List any concerns AI couldn't self-fix]
- [Flag for human review]

**Recommendations:**
- [Performance improvement ideas]
- [Security hardening suggestions]

**References:**
- Constraint source: [Link to constraint doc]
- Test coverage tool: [jest/nyc]
- Linter used: [eslint/prettier]

---

### Final Status

**✅ READY FOR HUMAN REVIEW** 

All checklist items passed. Code ready for `code-review-checklist.md`

**OR**

**⚠️ REQUIRES ATTENTION**

Failed items:
- [ ] Item 1
- [ ] Item 2

Recommend: [Reject & iterate / Manual fix required]

---

**Generated at:** 2026-05-12 10:30 UTC
**AI Model:** Claude 3.5 Sonnet
**Total Duration:** X minutes
```

---

## 📝 How to Use

### For AI (when generating code)

1. **Fill in metadata** (Prompt ID, version, task)
2. **Run through each item** in the checklist
3. **Mark [x]** if pass, [ ] if fail
4. **Document Self-Fix history** if applicable
5. **Provide final status:** READY or REQUIRES ATTENTION

### For Human Reviewer

1. **Check "Failed items"** section if present
2. **Cross-check** critical items (Security, Testing)
3. **Verify** regression risk assessment
4. **Decide:** Approve → Merge, or Reject → Back to AI

---

## 🎯 Key Items (Absolutely Mandatory)

**If AI cannot pass these 3 items → Escalate immediately:**
1. ✓ Security constraints
2. ✓ Error handling
3. ✓ Test coverage >= 80%

---

## 📊 Metrics from Report

**Track over time:**
- Average iteration count per task
- Common fail items (pattern detection)
- Time to pass Self-Check
- Defect escape rate (% caught by human)

---

## 🔗 Reference

- Code Review Checklist: [`code-review-checklist.md`](code-review-checklist.md)
- Audit Full: [`audit-ai-code-full.md`](audit-ai-code-full.md)
- Appendix C: Original documentation "AI Agent Coding"

---

**Template Version:** 1.0 | **Last Updated:** 2026-05-12
