# Escalation Workflow

**How to handle when AI fails to cooperate after 2 iterations**

---

## 🔄 Decision Tree

```
AI Output
├─ Self-Check PASS?
│  └─ YES → Code Review → Merge ✓
│
└─ NO (or Code Review fail)
   ├─ Round 1: Self-Fix
   │  ├─ PASS → Merge ✓
   │  └─ FAIL
   │
   ├─ Round 2: Self-Fix
   │  ├─ PASS → Merge ✓
   │  └─ FAIL
   │
   └─ ESCALATE ↓ (Don't retry 3rd time)
      ├─ Log in: AI Failure Log
      ├─ Decision Point (choose one):
      │  ├─ [A] Code manually yourself
      │  ├─ [B] Wait for mentor review
      │  └─ [C] Rework prompt & restart
      └─ Document lesson learned
```

---

## 🎯 Escalation Path

### Level 1: Self-Help

**When:** AI fails 2nd time

**What to do:**
1. Log incident in: [`ai-failure-log-template.md`](ai-failure-log-template.md)
2. Analyze: Why did AI fail?
   - Hallucination? (wrong API)
   - Unclear prompt? (ambiguous requirement)
   - Missing context? (didn't have enough info)
   - Architecture mismatch? (AI doesn't understand pattern)
3. Decide: What's next?
   - [ ] Code manually (fastest for simple tasks)
   - [ ] Rework prompt (if clearly fixable)
   - [ ] Escalate to Level 2

---

### Level 2: Mentor / Team Lead

**When:** Can't resolve at Level 1 (> 1 hour spent)

**How to escalate:**
```
Message to mentor:
"Task: [name]
Prompt: PROMPT-XXX
AI failed 2x on: [specific issue]
Root cause: [hallucination/ambiguous/missing context]
Time spent: [X min]
Question: Should I code manually or rework prompt?"
```

**Mentor decisions:**
- [ ] "Code manually, we'll improve prompt later"
- [ ] "Let me revise prompt with you"
- [ ] "Escalate to architect (if design issue)"

---

### Level 3: Technical Lead / Architect

**When:** Requires architectural decision or major prompt redesign

**Involved if:**
- Design pattern fundamentally misaligned
- New prompt needed (not covered in library)
- AI model seems inadequate for task
- Security/compliance concern

**Typical resolution:**
- Redesign task decomposition
- Create new prompt template
- Possibly assign to senior engineer

---

## ⏱️ Time Budget

**Don't exceed per task:**

| Stage | Budget | Status |
|-------|--------|--------|
| Initial attempt | 10 min | 🟢 OK |
| Round 1 iterate | +10 min | 🟢 OK |
| Round 2 iterate | +10 min | 🟢 OK |
| Escalation prep | +10 min | 🟡 Warn |
| **Total** | **~40 min** | 🚨 Stop! |

**If you've spent 40+ minutes → ESCALATE NOW**

---

## 📋 Escalation Checklist

Before escalating, verify:

- [ ] Tried 2 full iterations with AI?
- [ ] Checked [`hallucination-detection.md`](../quality-control/hallucination-detection.md)?
- [ ] Read error messages carefully?
- [ ] Searched existing prompts for similar case?
- [ ] Documented in [`ai-failure-log-template.md`](ai-failure-log-template.md)?
- [ ] Have specific question for mentor?

---

## 👥 Escalation Contacts

**Update with your team info:**

| Role | Name | Slack | Hours |
|------|------|-------|-------|
| Mentor | [Name] | @[slack] | [Times] |
| Tech Lead | [Name] | @[slack] | [Times] |
| Architect | [Name] | @[slack] | [Times] |

---

## 📞 How to Reach Out

**Message format (copy this):**

```
🆘 AI Task Escalation

Task: [name]
Prompt: PROMPT-XXX v1.0
Status: ❌ FAILED after 2 iterations

Issue: [Describe specifically]
AI said: [Quote the error/issue]
I tried: [What fix did you attempt]

Time spent: [X min]
Next step: [What would you recommend?]

Logs: [Link to failure log]
```

---

## 🔄 Possible Outcomes

| Outcome | Action | Timeframe |
|---------|--------|-----------|
| **Code manually** | Write it yourself | Immediate |
| **Revise prompt** | Mentor helps rewrite | +15 min |
| **New prompt** | Create template | +30 min |
| **Task reassign** | Give to senior eng | +1 day |
| **Defer task** | Put on backlog | Later |

---

## 📊 Track Escalations

**Monthly:**
```
Escalation rate: [# escalations] / [# total AI tasks]
Target: < 10%
If > 20%: Review prompt library & training
```

**Per engineer:**
```
Track: Who escalates most often?
Action: Extra coaching / mentoring
Goal: Reduce escalations over time
```

---

## 🎯 Learning from Escalations

**After escalation, document:**

1. **What went wrong?**
   - Prompt clarity? Context? AI limitation?

2. **What would fix it?**
   - Better prompt? Different approach? Different AI model?

3. **Update library:**
   - Improve similar prompts?
   - Create new template?
   - Update documentation?

4. **Team learning:**
   - Share finding with team
   - Update onboarding docs
   - Prevent similar failures

---

## 🚫 What NOT to Do

❌ **Don't:**
- Keep retrying AI endlessly (wastes time & tokens)
- Escalate without logging failure first
- Escalate without clear description
- Ignore mentor's advice
- Code bad solution without trying hard first

✅ **Do:**
- Escalate decisively after 2 failures
- Document for team learning
- Follow mentor's guidance
- Code manually if that's faster
- Share improvements with library

---

## 🔗 Related Resources

- Failure Log: [`ai-failure-log-template.md`](ai-failure-log-template.md)
- Hallucination Detection: [`../quality-control/hallucination-detection.md`](../quality-control/hallucination-detection.md)
- Prompt Library: [`../prompts/`](../prompts/)
- Security Constraints: [`security-constraints.md`](security-constraints.md)

---

**Escalation Workflow v1.0 | Last updated: 2026-05-12**

**Remember: It's OK to escalate! That's what teammates are for. 🤝**
