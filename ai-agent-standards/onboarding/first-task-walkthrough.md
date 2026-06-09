# First Task Walkthrough - Step-by-Step Guide

**Detailed guide to completing your first AI-Assisted task.**

---

## 🎯 Example Task

> Create POST endpoint `/api/users/register` with:
> - Email validation
> - Password hashing (bcrypt)
> - Return user ID on success
> - Rate limiting: max 10 requests/minute

---

## 🚀 Step 1: Understand Requirements (5 min)

**Ask yourself:**
- What API does this create?
- What inputs? What outputs?
- What security concerns?
- What edge cases?

**For our example:**
- INPUT: { email, password }
- OUTPUT: { userId, email, createdAt }
- SECURITY: Hash password, validate email
- EDGE CASES: Email already exists, weak password

---

## 📝 Step 2: Prepare Context (10 min)

**Gather information:**
1. Tech stack: Node.js + Express + TypeScript
2. Database: PostgreSQL with User model
3. Existing code: Check User model methods
4. Constraints: Project's naming conventions

**Checklist:**
- [ ] Know existing User model?
- [ ] Know database connection?
- [ ] Know project folder structure?
- [ ] Know authentication approach?

---

## 🎨 Step 3: Design Before Code (5 min)

**Sketch the flow:**
```
POST /api/users/register
  ↓
Validate input (email format, password length)
  ↓
Check if email exists
  ↓
Hash password
  ↓
Save to DB
  ↓
Return userId + email
```

**Jot down:**
- Error scenarios (email exists, weak password)
- Response codes (201 success, 400 bad request, 409 conflict)
- Rate limiting library (express-rate-limit)

---

## 🔍 Step 4: Write Prompt (10 min)

**Using template from** [`../prompts/PROMPT-TEMPLATE.md`](../prompts/PROMPT-TEMPLATE.md):

```markdown
---
id: PROMPT-001
version: 1.0
author: [Your name]
last_updated: 2026-05-12
applicable_stack: [Node.js, Express, TypeScript, PostgreSQL]
category: API_Development
difficulty: Intermediate
---

### [CONTEXT]
- Tech stack: Express.js, TypeScript, PostgreSQL 14
- Database model: User { id, email, password, createdAt }
- Existing: User.findByEmail(), User.create()
- Libs available: bcrypt, express-rate-limit

### [TASK]
- Create POST /api/users/register endpoint
- Input: { email: string, password: string }
- Output: { userId: number, email: string, createdAt: date }
- Requirements:
  [ ] Hash password with bcrypt
  [ ] Validate email format
  [ ] Return 409 if email exists
  [ ] Rate limit: max 10 req/min per IP

### [CONSTRAINTS]
- FORBIDDEN:
  - No hardcoded JWT secrets
  - No plaintext passwords
  - No logging passwords/emails
- REQUIRED:
  - Try-catch for DB operations
  - Input validation with zod/joi
  - Unit tests (80%+ coverage)
  - Comments explain logic

### [OUTPUT]
- TypeScript file: src/controllers/auth.controller.ts
- Include: Function + Unit tests
- Format: ESLint + Prettier
- Include: Self-Check report
```

---

## 💬 Step 5: Paste to AI (2 min)

**Where:** Cursor IDE / Claude / ChatGPT

**Paste:** Your prompt (copy entire thing)

**Wait:** AI generates code + Self-Check report

---

## 🔍 Step 6: Review AI Output (10 min)

**Check Self-Check Report:**
```
✓ Security constraints met?
✓ Error handling complete?
✓ Tests >= 80%?
✓ No hardcoded secrets?
```

**Use Quick Checklist:**
- [ ] Code solves problem?
- [ ] Security OK?
- [ ] Error handling?
- [ ] Tests exist?
- [ ] No breaking changes?

**If Self-Check Report says ⚠️ REQUIRES ATTENTION:**
- Note the failed items
- Go to Step 7 (Iterate)

---

## ❌ Step 7: Iterate if Needed (10 min)

**If output has issues:**

1. **Identify the problem:**
   - "No try-catch on line 23"
   - "Email validation missing"
   - "Hallucination: bcrypt method wrong"

2. **Tell AI exactly:**
   ```
   "Issue: Missing try-catch on User.findByEmail() call
   Fix: Wrap with try-catch block
   Reference: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch"
   ```

3. **AI regenerates code + new Self-Check report**

4. **Repeat until PASS**

⚠️ **Limit:** If fails > 2 times → Escalate to mentor

---

## ✅ Step 8: Final Review Before Merge (5 min)

**Use** [`../quality-control/code-review-checklist.md`](../quality-control/code-review-checklist.md):

- [ ] Self-Check Report complete?
- [ ] Code matches requirements?
- [ ] Security: No secrets, input validation?
- [ ] Error handling: try-catch, null checks?
- [ ] Tests: 80%+ coverage?
- [ ] Comments clear?
- [ ] Backward compatible?

**Decision:** ✅ APPROVE or ❌ REQUEST CHANGES

---

## 🎉 Step 9: Merge & Log (5 min)

**Merge:**
```bash
git add src/controllers/auth.controller.ts src/controllers/auth.spec.ts
git commit -m "feat: add user registration endpoint with rate limiting"
git push
```

**Log Results:**
Record in your project's task tracker:
```
date,task_name,prompt_id,ai_iterations,test_coverage,time_mins
2026-05-12,user-registration,PROMPT-001,1,85,35
```

---

## 📊 Timeline

| Step | Duration | Task |
|------|----------|------|
| 1 | 5 min | Understand requirements |
| 2 | 10 min | Gather context |
| 3 | 5 min | Design flow |
| 4 | 10 min | Write prompt |
| 5 | 2 min | Paste to AI |
| 6 | 10 min | Review output |
| 7 | 10 min | Iterate (if needed) |
| 8 | 5 min | Final review |
| 9 | 5 min | Merge & log |
| **TOTAL** | **~60 min** | **Complete task** |

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| AI output not working | Check hallucination: [`../quality-control/hallucination-detection.md`](../quality-control/hallucination-detection.md) |
| Missing error handling | Tell AI: "Add try-catch on all DB calls" |
| Tests failing | Check test coverage: `npm run test:coverage` |
| Can't understand code | Ask mentor to review |
| AI keeps failing | Escalate after 2 attempts |

---

## 💡 Pro Tips

1. **Be specific in prompts** - More detail = better output
2. **Reference official docs** - Reduces hallucinations
3. **Test locally first** - Don't just review code
4. **Document decisions** - Helps others learn
5. **Ask for help early** - No penalty for asking

---

## ✨ After Completing First Task

You're ready to:
- ✓ Code alone with AI
- ✓ Review other's AI code
- ✓ Create new prompts
- ✓ Mentor new engineers

**Next:** Take 2-3 more tasks independently, then you're a pro! 🎯

---

**Walkthrough v1.0 | Estimated time: 60 minutes**

Questions? Slack your mentor → [`#ai-coding`]
