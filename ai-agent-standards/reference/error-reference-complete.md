# Error Reference — Common AI Errors & Fixes

**Appendix B — Expanded from original documentation**

---

## 🚫 Type 1: Hallucinated Packages

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find module 'magical-lib'` | AI imported non-existent package | Check npm registry, use real package |
| Import from `@enterprise/cache` | Fake scoped package | Verify in package.json |
| Using `lodash-pro` | Premium version doesn't exist | Use standard `lodash` |

**Prevention:**
- Provide installed packages list in context
- Ask: "Only use packages in package.json"

---

## 🚫 Type 2: Hallucinated Methods

| Error | Cause | Fix |
|-------|-------|-----|
| `user.findMagicId()` not a function | Method doesn't exist | Check model definitions, verify docs |
| `result.magicalLength` undefined | Property doesn't exist | Use actual property names |
| `redis.getWithTTL()` | Non-existent redis API | Reference: https://redis.io/commands |

**Prevention:**
- Include code sample of actual methods
- Link to official API docs

---

## 🚫 Type 3: Incorrect Async/Await

| Error | Cause | Fix |
|-------|-------|-----|
| Mixed `.then()` and `await` | Inconsistent promise handling | Use one style consistently |
| Forgot `await` | Promise not resolved | Add `await` before async call |
| Unhandled promise rejection | Error not caught | Wrap in try-catch |

**Fix:**
```javascript
// ❌ WRONG
const data = fetch(url);  // Missing await
const json = data.json();

// ✅ RIGHT
const data = await fetch(url);
const json = await data.json();
```

---

## 🚫 Type 4: Wrong Parameter Types

| Error | Cause | Fix |
|-------|-------|-----|
| `db.query(sql, userId)` | Missing parameterized placeholder | Use `$1, $2` and array |
| `res.json(data, 200)` | Wrong parameter order | Use `res.status(200).json(data)` |
| `func(undefined)` | Missing required param | Verify function signature |

---

## 🚫 Type 5: Configuration Not Found

| Error | Cause | Fix |
|-------|-------|-----|
| `process.env.MAGIC_KEY` is undefined | Wrong var name | Check .env.example file |
| Cannot load `./config.xyz.js` | File doesn't exist | Use actual config file names |
| Missing database connection | URL not configured | Verify DATABASE_URL in .env |

**Prevention:**
- Link .env.example in context
- Show config file structure

---

## 🚫 Type 6: Deprecated APIs

| Error | Cause | Fix |
|-------|-------|-----|
| `util.promisify()` | Old Node version API | Check min Node.js version |
| `express.static()` params changed | API evolution | Check Express release notes |
| Callback-based instead of Promise | Old pattern | Use modern async/await |

---

## 🚫 Type 7: Schema/Type Mismatches

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot read property of null` | Null pointer exception | Add null check |
| Type `string` but got `number` | TypeScript error | Fix type or convert |
| Field doesn't exist on interface | Wrong schema | Verify database/interface |

**Fix:**
```typescript
// ❌ WRONG
const name = user.fullName;  // Doesn't exist

// ✅ RIGHT
const name = user.firstName + ' ' + user.lastName;
```

---

## 🚫 Type 8: Security Issues

| Error | Cause | Fix |
|-------|-------|-----|
| SQL injection possible | Raw query | Use parameterized: `$1, $2` |
| Password logged | Hardcoded password | Never log sensitive data |
| API key in code | Hardcoded secret | Use .env file |

**Prevention:**
- Emphasize: "Zero hardcoded secrets"
- Include security constraints

---

## 🚫 Type 9: Missing Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Uncaught Error: ... | No try-catch | Wrap in try-catch block |
| Silent failure | No error logging | Add logger.error() |
| No fallback | Resource unavailable | Add graceful degradation |

**Fix:**
```javascript
// ❌ WRONG
const user = await User.findById(id);

// ✅ RIGHT
try {
  const user = await User.findById(id);
  if (!user) throw new Error('User not found');
  return user;
} catch (error) {
  logger.error('Find user failed:', error);
  throw error;
}
```

---

## ✅ Solutions Summary

| Category | Common Fix | Resources |
|----------|-----------|-----------|
| **Packages** | Check npm registry | https://npmjs.com |
| **APIs** | Read official docs | [Relevant docs link] |
| **Async** | Add await, use try-catch | MDN: async/await |
| **Config** | Reference .env.example | Check project root |
| **Security** | Parameterized queries, .env | OWASP Top 10 |
| **Errors** | Try-catch + logging | Node.js docs |
| **Types** | Check schema definitions | Schema files |

---

## 🎯 Prevention Checklist

Before asking AI:
- [ ] Include API examples in context
- [ ] Link to official documentation
- [ ] Show config file structure
- [ ] List allowed packages
- [ ] Specify security requirements
- [ ] Show schema/interface definitions

---

## 📞 When to Escalate

After trying 2 fixes and still failing:
1. Log in [`../risk-management/ai-failure-log-template.md`](../risk-management/ai-failure-log-template.md)
2. Escalate to mentor
3. Code manually or update prompt

---

**Error Reference v1.0 | Last updated: 2026-05-12**

Based on: Appendix B, Original documentation "AI Agent Coding"

*Add new errors as they are discovered!*
