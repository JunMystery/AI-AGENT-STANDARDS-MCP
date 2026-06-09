# AI Failure Log - Template

**Record when AI cannot complete a task (> 2 Self-Fix rounds)**

---

## 📝 Template Entry

```markdown
---
date: 2026-05-12
time: 10:30 UTC
engineer: [Your name]
---

## Incident Report

**Prompt:** PROMPT-001 v1.0
**Task:** [Brief description]

### Failure Summary
- **Rounds:** 2 (failed on attempt 3)
- **Root Cause:** [Why did it fail?]
- **Category:** [Security / Hallucination / Logic / Performance / Other]

### Details

**Attempt 1:** 
- Issue: [What was wrong]
- Fix Applied: [What we told AI]

**Attempt 2:**
- Issue: [What was wrong]
- Fix Applied: [What we told AI]

**Attempt 3 (ESCALATION):**
- Issue: [What failed again]
- Why Escalated: AI can't seem to grasp requirement

### Root Cause Analysis

**Technical Issue:**
[Describe the technical problem]

**AI Limitation:**
[Why AI struggled - hallucination? Architecture mismatch? Doc not clear?]

**Prompt Issue:**
[Was the prompt not detailed enough?]

### Resolution

**Action Taken:**
- [ ] Coded manually
- [ ] Updated prompt & re-submitted
- [ ] Escalated to: [Team lead name]
- [ ] Other: [Describe]

**Result:**
- Task: [Completed / In Progress / Blocked]
- Time Wasted: [X hours]
- Learning: [What to improve]

### Improvement Notes

**Next Time:**
1. [Specific improvement to prompt]
2. [Process change]
3. [Documentation update]

**Update Prompt Library:**
- [ ] Updated PROMPT-001 with fix?
- [ ] Created new prompt for similar case?
- [ ] Documented pattern to avoid?
```

---

## 📊 Example Entry

```markdown
---
date: 2026-05-12
time: 14:15 UTC
engineer: John Doe
---

## Incident Report

**Prompt:** PROMPT-002 (Cache Strategy)
**Task:** Implement Redis caching with TTL invalidation

### Failure Summary
- **Rounds:** 2 failed, escalated
- **Root Cause:** AI hallucinated Redis API methods
- **Category:** Hallucination

### Details

**Attempt 1:**
- Issue: Used non-existent `redis.getWithTTL()` method
- Fix Applied: "Use real redis API: `redis.get()` and separate TTL logic"

**Attempt 2:**
- Issue: Referenced `@redis-enterprise/cache` package (doesn't exist)
- Fix Applied: "Use only `redis` package from npm, not enterprise version"

**Attempt 3 (ESCALATION):**
- Issue: Still using wrong API (`redis.magic.cache()`)
- Why Escalated: AI clearly doesn't know redis API well

### Root Cause Analysis

**Technical Issue:**
- AI doesn't have correct Redis API in training data
- Generated plausible-sounding but non-existent methods

**AI Limitation:**
- Hallucination of package APIs
- Common problem with less popular libraries

**Prompt Issue:**
- Didn't include redis docs link in context
- Should have provided example usage

### Resolution

**Action Taken:**
- [x] Coded manually (30 min to write correct version)
- [ ] Updated prompt & re-submitted
- [x] Escalated to: Alice (Tech Lead)
- [x] Documented pattern

**Result:**
- Task: Completed manually
- Time Wasted: 45 minutes
- Learning: Need to provide API examples for less-known libs

### Improvement Notes

**Next Time:**
1. Add Redis docs link & API example to context
2. Specifically forbid non-existent methods
3. Include test that would catch hallucination early

**Update Prompt Library:**
- [x] Created PROMPT-002-v2 with redis examples
- [x] Added hallucination detection guide
- [x] Documented redis-specific gotchas
```

---

## 📌 When to Log

**Log ONLY when:**
- ✓ AI self-check FAILED > 1 time
- ✓ Escalated beyond 2 iterations
- ✓ Required manual override

**Don't log:**
- ✗ Successful tasks (use metrics instead)
- ✗ Minor issues caught in self-check

---

## 📊 Monthly Analysis

**Run query on failure logs:**
```
SELECT 
  category, 
  COUNT(*) as incidents,
  AVG(time_wasted_hours) as avg_time,
  ARRAY_AGG(DISTINCT prompt_id) as affected_prompts
FROM ai_failures
WHERE date > DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY category
ORDER BY incidents DESC;
```

**Actions:**
- Top failures → Improve prompts
- Common patterns → Team training
- Persistent issues → Consider different AI model

---

## 🔗 Links

- Report: Store as: `./ai-failure-log-[YYYY-MM].md`
- Reference: [`escalation-workflow.md`](escalation-workflow.md)
- Improvement: Update [`../prompts/`](../prompts/) as needed

---

**Failure Log Template v1.0 | Last updated: 2026-05-12**

Start logging now! 📝
