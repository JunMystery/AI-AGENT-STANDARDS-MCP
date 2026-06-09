---
id: PROMPT-004
version: 1.0
author: AI Agent Coding Framework
last_updated: 2026-05-12
applicable_stack: [Node.js, Express, TypeScript]
category: Security
difficulty: Intermediate
---

# Prompt: Security Audit - Vulnerability Detection

**Purpose:** Audit code & model architecture to detect security vulnerabilities

---

## [CONTEXT]

- **Tech stack:** Node.js, Express, TypeScript, PostgreSQL
- **Code to audit:**
  ```javascript
  app.post('/api/search', (req, res) => {
    const query = req.body.q;
    const result = db.query("SELECT * FROM products WHERE name = '" + query + "'");
    res.send(result);
  });
  ```
- **Objective:** Detect & fix vulnerabilities (SQL Injection, XSS, etc.)

---

## [TASK]

**Objective:** Audit & provide fix recommendations

**Acceptance Criteria:**
- [ ] Detect all vulnerabilities
- [ ] Explain each issue (CWE reference)
- [ ] Provide fixed code
- [ ] All test cases verify fixes

---

## [CONSTRAINTS]

**REQUIRED:**
- ✓ Parameterized queries mandatory
- ✓ Input validation + sanitization
- ✓ Error handling must not reveal details
- ✓ Security comments

---

## [OUTPUT FORMAT]

- **Format:** Audit report + fixed code
- **Include:** Security checklist + recommendations

---

## 📝 Reference

- Security Constraints: [`../../risk-management/security-constraints.md`](../../risk-management/security-constraints.md)
- Error Reference: [`../../reference/error-reference-complete.md`](../../reference/error-reference-complete.md)
