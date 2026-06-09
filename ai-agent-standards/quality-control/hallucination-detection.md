# Hallucination Detection

**How to identify when AI generates non-existent or incorrect code.**

---

## 🎯 Definition

**Hallucination:** AI generates code/references that don't actually exist in:
- Installed packages
- Official documentation
- Available APIs/methods
- Project codebase

---

## 🚩 Red Flags (Warning Signs)

### 1. Import Non-Existent Packages

```javascript
// ❌ HALLUCINATION
import { magic } from 'magical-lib-that-doesnt-exist';
import { SuperCache } from '@enterprise/cache'; // Not in package.json
```

**How to detect:**
```bash
# Check what's installed
npm ls

# Or check package.json for dependency
grep '"magical-lib"' package.json

# Try importing in REPL
node -e "require('magical-lib')"  # Will throw
```

**Fix:** Verify in [npm registry](https://npmjs.com/) or use real packages

---

### 2. Non-Existent Methods/Properties

```typescript
// ❌ HALLUCINATION
const user = await User.findByMagicId(123);  // Method doesn't exist
const count = result.magicalLength;  // Property doesn't exist

// Should be:
const user = await User.findById(123);
const count = result.length;
```

**How to detect:**
- Check official documentation for actual API
- Check TypeScript definitions (.d.ts files)
- Run TypeScript compiler: `tsc --noEmit`

---

### 3. Using Deprecated/Removed APIs

```javascript
// ❌ HALLUCINATION (Node 18+)
const { startServer } = require('http').listen();  // API changed

// ❌ HALLUCINATION (Express 5.0+)
app.use(express.static(path)); // Parameter format changed
```

**How to detect:**
- Check package release notes
- Check [DeprecationWarning](https://nodejs.org/api/process.html#process_event_deprecation) logs
- Compare with official examples

---

### 4. Incorrect Syntax/API Patterns

```typescript
// ❌ HALLUCINATION
async function() {
  await User.find().then(() => {
    // Mixed promise & async/await (works but wrong pattern)
  });
}

// ❌ HALLUCINATION
const result = await Promise.all([  // Missing await keyword context
  fetch(url1),
  fetch(url2)
].map(async res => res.json());
```

**How to detect:**
- Run code → TypeError
- Check framework/library docs for proper patterns
- Use linter rules (ESLint)

---

### 5. Using Non-Existent Modules/Classes

```javascript
// ❌ HALLUCINATION
const { DatabaseConnection } = require('./models/database');
// File doesn't exist in project

// ❌ HALLUCINATION
import User from '@models/User';  // Path alias doesn't exist in tsconfig.json
```

**How to detect:**
```bash
# Check if file exists
ls -la src/models/database.js  # Not found

# Check TypeScript paths
grep '"@models"' tsconfig.json  # Not configured
```

---

### 6. Incorrect Parameter Types/Formats

```javascript
// ❌ HALLUCINATION
db.query("SELECT * FROM users", [userId, 'wrongType']);
// Second param should be number, not string

// ❌ HALLUCINATION
res.json({ data }, 200);  // Second param doesn't exist
// Correct: res.status(200).json({ data })
```

**How to detect:**
- Check method signature in docs
- Enable TypeScript strict mode
- Run code & check error messages

---

### 7. Wrong Configuration / Environment Variables

```javascript
// ❌ HALLUCINATION
const apiKey = process.env.MAGICAL_API_KEY;  // Never set in .env
// Should reference actual env var

// ❌ HALLUCINATION
const config = require('./config.magical.js');  // File doesn't exist
```

**How to detect:**
```bash
# Check .env
cat .env | grep API_KEY

# Check config files
ls -la config/
```

---

## ✅ Detection Checklist

### Before Merging AI Code

- [ ] **Run code locally** - Errors? → Hallucination
- [ ] **Check imports** - `npm ls [package]` exists?
- [ ] **TypeScript check** - `tsc --noEmit` passes?
- [ ] **Linter** - `eslint .` clean?
- [ ] **Verify APIs** - Check official docs
- [ ] **File paths** - Do they exist? `ls -la [file]`
- [ ] **Env variables** - Check .env.example

### Automated Detection

```bash
# TypeScript strict checking
tsc --strict --noEmit

# ESLint with type checking
eslint . --ext .ts

# Runtime test
node -e "require('./src/your-file.js')"

# Import analysis
npm audit  # Dependency issues
```

---

## 🔧 How to Fix

### Step 1: Identify the Hallucination

```
Error message → Look for:
- "Cannot find module"
- "is not a function"
- "Cannot read property X of undefined"
- "TypeError: X is not defined"
```

### Step 2: Verify Reality

```bash
# For packages
npm search [package-name]

# For methods
grep -r "methodName" node_modules/[package]/

# For files
find . -name "[filename]" -type f
```

### Step 3: Update Prompt

"Use [real-package] instead of [fake-package]. API reference: [link]"

### Step 4: Re-run AI

Ask AI to regenerate with correction.

---

## 📋 Common Hallucinations by Category

| Type | Example | Fix |
|------|---------|-----|
| **Package** | `import from 'lib-xyz'` | Verify in npm registry |
| **Method** | `user.findMagic()` | Check User model definition |
| **Path** | `@config/app` | Verify tsconfig.json paths |
| **API** | `res.magical()` | Check Express.Response API |
| **Field** | `user.magicalId` | Check database schema |
| **Const** | `process.env.MAGIC_KEY` | Check .env.example |

---

## 🎯 Prevention Strategies

### 1. Provide Accurate Context

❌ Don't:
```
"Add user authentication"
```

✅ Do:
```
"Add JWT authentication using `jsonwebtoken` package (v9.0.0).
User model methods: findById(), comparePassword().
See: src/models/User.ts"
```

### 2. Include Code Samples

```
"Implement password hashing:

Example pattern:
import bcrypt from 'bcrypt';
await bcrypt.hash(password, 10);
```

### 3. Reference Official Docs

```
"Use Express middleware pattern: https://expressjs.com/en/guide/using-middleware.html
Current middlewares in src/middlewares/"
```

### 4. Specify Constraints Clearly

```
"MUST use: bcrypt for hashing (already installed)
MUST NOT: Create custom crypto functions"
```

---

## 🚨 What If Hallucination Happens?

**Escalation Path:**

1. **Document** → Create issue: "AI hallucination: X doesn't exist"
2. **Fix manually** or **escalate to AI with clear docs**
3. **Update prompt library** → Improve similar prompts
4. **Track** → Log in project issue tracker

---

## 📚 Resources

- [NPM Package Registry](https://npmjs.com/)
- [Node.js Docs](https://nodejs.org/docs/)
- [Express.js Guide](https://expressjs.com/)
- Official package documentation (usually in GitHub README)

---

**Detection Guide Version:** 1.0 | **Last Updated:** 2026-05-12
