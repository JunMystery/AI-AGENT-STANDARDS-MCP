# Common Mistakes 

**Frequent Errors When Working with AI: Prevention and Solutions.**

---

## 🚫 Mistake 1: Skipping the Self-Check Report

**What:** Copy AI code directly without reviewing Self-Check report

**Why bad:**
- Miss security issues
- Tests not done
- Errors not handled
- Hallucinations not caught

**Fix:**
1. Always read Self-Check Report FIRST
2. Check: Security ✓, Tests ✓, Errors ✓
3. If any ⚠️ → Request fixes

**Example:**
```javascript
// ❌ BAD: AI said "pass" but it lied
const secret = process.env.API_KEY;  // Hardcoded by accident!

// ✅ GOOD: Self-Check caught it
// ⚠️ Issue: Environment variable access - verify .env setup
```

---

## 🚫 Mistake 2: Hardcoding Secrets

**What:** Leaving API keys, passwords, tokens in code

**Why bad:**
- Security breach
- Keys exposed on GitHub
- Attackers use them
- Won't pass code review

**Fix:**
- Use: `process.env.SECRET_KEY` (from .env)
- Never: Paste real secrets in prompt
- Check: No hardcoded values in output

**Example:**
```javascript
// ❌ BAD
const apiKey = "sk-abc123xyz789";  // Public on GitHub!

// ✅ GOOD
const apiKey = process.env.OPENAI_API_KEY;  // From .env file
```

---

## 🚫 Mistake 3: Missing Error Handling

**What:** AI generates code without try-catch blocks

**Why bad:**
- Crashes in production
- User sees error page
- No logs to debug
- Bad experience

**Fix:**
- Always check: try-catch present?
- For: Database calls, API calls, file access
- Include: Meaningful error messages

**Example:**
```javascript
// ❌ BAD
const user = await User.findById(id);  // What if fails?

// ✅ GOOD
try {
  const user = await User.findById(id);
  if (!user) throw new Error('User not found');
  return user;
} catch (error) {
  logger.error('Failed to find user:', error);
  throw error;  // Propagate to caller
}
```

---

## 🚫 Mistake 4: No Input Validation

**What:** Not checking user input before processing

**Why bad:**
- SQL injection vulnerability
- XSS attacks possible
- System crashes on bad data
- Corrupted database

**Fix:**
- Validate BEFORE processing
- Use: zod, joi, validator libraries
- Check: Type, length, format

**Example:**
```javascript
// ❌ BAD
const query = req.body.search;
const results = db.query("SELECT * FROM products WHERE name = '" + query + "'");

// ✅ GOOD
const schema = z.object({ search: z.string().min(1).max(100) });
const { search } = schema.parse(req.body);
const results = db.query('SELECT * FROM products WHERE name = $1', [search]);
```

---

## 🚫 Mistake 5: Insufficient Test Coverage

**What:** AI generates code but tests < 80%

**Why bad:**
- Can't verify correctness
- Edge cases missed
- Regressions not caught
- Hard to maintain

**Fix:**
- Require: >= 80% coverage
- Test: Normal cases + edge cases + error cases
- Check: `npm run test:coverage`

**Example:**
```javascript
// ❌ BAD: Only happy path
test('add numbers', () => {
  expect(add(2, 3)).toBe(5);  // Only one test
});

// ✅ GOOD: All paths
test('add positive numbers', () => expect(add(2, 3)).toBe(5));
test('add negative numbers', () => expect(add(-2, -3)).toBe(-5));
test('add zero', () => expect(add(0, 0)).toBe(0));
test('add mixed', () => expect(add(-2, 3)).toBe(1));
```

---

## 🚫 Mistake 6: Hallucinations (Non-existent Code)

**What:** AI references packages/methods that don't exist

**Why bad:**
- Code won't run
- `npm install` fails
- Methods not found
- Tests fail

**Fix:**
- Verify in docs: https://npmjs.com
- Check TypeScript: `npm ls [package]`
- Run code locally: `node -e "require('lib')"`

**Example:**
```javascript
// ❌ HALLUCINATION
import { magicalCache } from '@lib/cache-pro';  // Doesn't exist!

// ✅ REAL
import redis from 'redis';  // Actual package
```

---

## 🚫 Mistake 7: Breaking Changes

**What:** AI changes API without backward compatibility

**Why bad:**
- Client code breaks
- Existing users affected
- Migration pain
- Bad reputation

**Fix:**
- Keep old API working
- Add new API separately
- Deprecate gradually
- Document changes

**Example:**
```javascript
// ❌ BAD: Breaking change
// OLD: GET /api/users/123
// NEW: GET /api/v2/users/id/123  // Path changed!

// ✅ GOOD: Backward compatible
// OLD still works: GET /api/users/123
// NEW also works: GET /api/v2/users/123
```

---

## 🚫 Mistake 8: Over-Iteration (Too Many Attempts)

**What:** Asking AI to fix the same thing 5+ times

**Why bad:**
- Wastes time
- AI goes in circles
- Better to code manually
- Costs money (tokens)

**Fix:**
- Limit: Max 2 Self-Fix rounds
- If fails 3rd time → Escalate
- Log in: AI Failure Log
- Code manually or ask mentor

**Decision tree:**
```
AI output has issue?
├─ Round 1: Tell AI to fix
│  └─ Passes? → Merge ✓
├─ Round 2: More specific fix
│  └─ Passes? → Merge ✓
└─ Round 3: STOP → Escalate ✗
   └─ Code manually yourself
```

---

## 🚫 Mistake 9: No Comments on Complex Logic

**What:** AI code lacks explanation of "why"

**Why bad:**
- Next person won't understand
- Hard to maintain
- Can't debug issues
- Blocks code review

**Fix:**
- Ask AI: "Add comments explaining why"
- Focus on: Business logic, edge cases
- Comments: Explain reasoning, not syntax

**Example:**
```javascript
// ❌ BAD: No comments
if (value > 100 && user.role !== 'admin') {
  throw new Error('Limit exceeded');
}

// ✅ GOOD: Clear comments
// Non-admin users have limit of 100 items
// This prevents database overload
if (value > 100 && user.role !== 'admin') {
  logger.warn(`User ${user.id} exceeded limit`);
  throw new Error('Item limit exceeded for non-admin users');
}
```

---

## 🚫 Mistake 10: Not Using Code Review Checklist

**What:** Skip checklist before merging

**Why bad:**
- Issues slip to production
- Bugs harder to catch later
- Team frustrated
- Reputation damage

**Fix:**
- ALWAYS use: [`../quality-control/code-review-checklist.md`](../quality-control/code-review-checklist.md)
- Check each item
- Only merge if PASS

**Checklist summary:**
- [ ] Security OK (no secrets)?
- [ ] Error handling complete?
- [ ] Tests >= 80%?
- [ ] No breaking changes?
- [ ] Comments clear?

---

## ✅ Lessons Summary

| Mistake | Cause | Prevention |
|---------|-------|-----------|
| Skip Self-Check | Rushing | Always read first |
| Hardcode secrets | Forget | Use .env only |
| No error handling | Lazy | Ask AI explicitly |
| No input validation | Oversight | Add validation |
| Low test coverage | Accepted | Require >= 80% |
| Hallucinations | Trust AI blindly | Verify with docs |
| Breaking changes | Don't think ahead | Plan migration |
| Too many iterations | Perfectionism | Limit to 2 tries |
| No comments | Copy-paste | Ask for comments |
| Skip checklist | Hurry | Make it mandatory |

---

## 🎯 Before Merge Checklist

```
[ ] Self-Check report present & complete?
[ ] Code runs without errors?
[ ] Security: No hardcoded secrets?
[ ] Error handling: Try-catch present?
[ ] Input validation: Sanitized?
[ ] Tests: >= 80% coverage?
[ ] Comments: Explain complex logic?
[ ] No breaking changes?
[ ] Code review checklist passed?
[ ] Ready to merge!
```

---

**Common Mistakes v1.0 | Last updated: 2026-05-12**

**Next:** Keep a copy handy during your first week! 📌
