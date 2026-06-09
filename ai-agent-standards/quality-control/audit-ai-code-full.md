# AI Code Audit - Full Checklist (Comprehensive)

**For Senior Review or Security-Sensitive Modules**

---

## 🎯 Purpose

Detailed audit of AI-generated code to detect:
- Subtle bugs & logic errors
- Security vulnerabilities
- Performance issues
- Design & architecture problems
- Hallucinations & incorrect patterns

---

## 🔍 Audit Sections

### 1️⃣ Security Audit (CRITICAL)

#### Authentication & Authorization
- [ ] JWT tokens properly validated (signature, expiry)?
- [ ] Passwords hashed (bcrypt/argon2), not plaintext?
- [ ] Session management secure?
- [ ] CORS properly configured (not wildcard)?
- [ ] Rate limiting in place?

#### Input Validation & Sanitization
- [ ] All user input validated?
- [ ] SQL queries use parameterized statements?
- [ ] HTML/JSON input sanitized?
- [ ] File uploads validated (extension, size, type)?
- [ ] No eval() / new Function() on user input?

#### Data Protection
- [ ] Sensitive data encrypted at rest?
- [ ] HTTPS enforced?
- [ ] API keys not in code / not in git history?
- [ ] Secrets loaded from .env only?
- [ ] Sensitive logs redacted?

#### Common Vulnerabilities
- [ ] ✗ SQL Injection: Check raw SQL queries
- [ ] ✗ XSS: Check DOM manipulation, user input rendering
- [ ] ✗ CSRF: Check form tokens, CORS headers
- [ ] ✗ XXE: Check XML parsing
- [ ] ✗ Path Traversal: Check file access paths
- [ ] ✗ Command Injection: Check system commands

#### HTTP Security Headers
- [ ] Content-Security-Policy set?
- [ ] X-Frame-Options configured?
- [ ] X-Content-Type-Options set?
- [ ] Strict-Transport-Security enabled?

---

### 2️⃣ Code Logic Audit

#### Algorithm Correctness
- [ ] Algorithm matches requirements exactly?
- [ ] Edge cases handled (empty, null, single item)?
- [ ] Off-by-one errors checked?
- [ ] Loop conditions correct?
- [ ] Recursion has proper termination?

#### Business Logic
- [ ] Calculations correct (financial, percentages)?
- [ ] State transitions valid?
- [ ] Concurrency handled (race conditions)?
- [ ] Side effects documented?
- [ ] Idempotency considered (if needed)?

#### Error Paths
- [ ] Null pointer exceptions prevented?
- [ ] Array bounds checked?
- [ ] Type mismatches caught?
- [ ] Timeouts implemented for external calls?
- [ ] Fallbacks for missing data?

---

### 3️⃣ Performance Audit

#### Database Access
- [ ] ✗ N+1 queries: Check for loops within queries
- [ ] Indexes used appropriately?
- [ ] Query plans reviewed (EXPLAIN)?
- [ ] Pagination implemented for large result sets?
- [ ] Connection pooling configured?
- [ ] ✗ Missing indexes on foreign keys?

#### Memory Management
- [ ] No memory leaks (listeners removed)?
- [ ] Large arrays loaded efficiently?
- [ ] Streaming used for large files?
- [ ] Object pooling for frequently created objects?
- [ ] Proper garbage collection hints?

#### Caching Strategy
- [ ] Cache key collision avoided?
- [ ] TTL appropriate?
- [ ] Cache invalidation complete?
- [ ] Stale data handled gracefully?
- [ ] Cache overhead < benefit?

#### Complexity Analysis
- [ ] Time complexity reasonable?
- [ ] Space complexity acceptable?
- [ ] No unnecessary nested loops?
- [ ] Algorithms optimized (sorting, searching)?

---

### 4️⃣ Testing Audit

#### Test Coverage
- [ ] >= 80% code coverage for new code?
- [ ] Critical paths tested?
- [ ] Error paths tested?
- [ ] Boundary conditions tested?

#### Test Quality
- [ ] Tests actually verify behavior (not just "runs")?
- [ ] Mock objects used correctly?
- [ ] Fixtures isolated (tests independent)?
- [ ] Async/await in tests handled properly?
- [ ] Flaky tests identified?

#### Integration Tests
- [ ] Database interactions tested?
- [ ] External APIs mocked correctly?
- [ ] Transaction rollback tested?
- [ ] Concurrent operations tested?

---

### 5️⃣ Architecture & Design Audit

#### Architecture Adherence
- [ ] Follows project pattern (MVC, layers, etc)?
- [ ] Separation of concerns respected?
- [ ] Framework conventions followed?
- [ ] File structure organized correctly?

#### Design Patterns
- [ ] Appropriate patterns used?
- [ ] Over-engineering avoided?
- [ ] SOLID principles applied (S, O, L, I, D)?
- [ ] DRY principle (no duplication)?
- [ ] No God objects?

#### Dependency Management
- [ ] Dependencies injected (testable)?
- [ ] No circular dependencies?
- [ ] Import order correct?
- [ ] External dependencies vetted?
- [ ] Version compatibility checked?

---

### 6️⃣ Code Quality Audit

#### Readability
- [ ] Variable names descriptive?
- [ ] Function names reflect purpose?
- [ ] Code structure logical?
- [ ] Complex sections commented?
- [ ] Consistent formatting?

#### Type Safety (TypeScript)
- [ ] No `any` types (or justified)?
- [ ] Strict null checks enabled?
- [ ] Type definitions complete?
- [ ] Generics used appropriately?
- [ ] Union types preferred over `any`?

#### Standards Compliance
- [ ] ESLint rules pass?
- [ ] Prettier formatting applied?
- [ ] Naming conventions consistent?
- [ ] No console.log() left?
- [ ] No debug statements?

---

### 7️⃣ Hallucination Detection

**AI may create things that don't actually exist:**

- [ ] ✗ Import non-existent libraries (check package.json)
- [ ] ✗ Call methods that don't exist (verify docs)
- [ ] ✗ Reference files/classes not in codebase
- [ ] ✗ Use deprecated APIs
- [ ] ✗ Incorrect TypeScript syntax
- [ ] ✗ Wrong package versions in requirements

**How to verify:**
```bash
npm ls [package]  # Check installed packages
grep -r "className" src/  # Verify file exists
```

---

### 8️⃣ Maintainability Audit

#### Documentation
- [ ] Function signatures documented (JSDoc)?
- [ ] Complex logic explained?
- [ ] API changes noted?
- [ ] Breaking changes highlighted?
- [ ] Examples provided if useful?

#### Evolvability
- [ ] Code easy to modify?
- [ ] Configuration parameterized?
- [ ] Hard to break by accident?
- [ ] Plugin-friendly architecture?
- [ ] Versioning strategy clear?

---

### 9️⃣ Integration Audit

#### External Integrations
- [ ] API calls resilient (retries, timeouts)?
- [ ] Error responses handled?
- [ ] Webhooks validated?
- [ ] Rate limits respected?
- [ ] Polling not excessive?

#### Deployment
- [ ] Configuration environment-specific?
- [ ] No environment-specific code?
- [ ] Migrations present (if DB changes)?
- [ ] Feature flags for gradual rollout?
- [ ] Rollback plan defined?

---

### 🔟 RAG Pipeline Audit

#### Retrieval Quality
- [ ] Embedding model specified and version-pinned?
- [ ] Vector DB query includes similarity threshold?
- [ ] Chunk size appropriate for domain (not too large/small)?
- [ ] Top-K results reasonable (not returning entire DB)?
- [ ] Retrieval latency acceptable (< target SLA)?

#### Source Grounding
- [ ] Every generated response cites source documents?
- [ ] Citations include verifiable references (doc name, page)?
- [ ] No fabricated citations (source documents actually exist)?
- [ ] Context window not exceeded by retrieved documents?

#### Fallback Handling
- [ ] Empty retrieval results trigger safe fallback (not LLM generation)?
- [ ] Fallback message is a constant string (not AI-generated)?
- [ ] Failed queries logged for analysis?
- [ ] Low-confidence results flagged or disclaimed?

---

### 1️⃣1️⃣ AI Output Safety Audit

#### Hallucination Prevention
- [ ] LLM temperature set low (≤ 0.3) for factual domains?
- [ ] System prompt explicitly forbids fabrication?
- [ ] Output validated against retrieved sources?
- [ ] Confidence score calculated and exposed in response?

#### Domain-Specific Safety
- [ ] Medical/legal/financial disclaimers present where needed?
- [ ] No diagnosis, treatment, or legal advice generated?
- [ ] PII redacted from logs and responses?
- [ ] Content moderation applied to user inputs?

#### Output Boundaries
- [ ] Response length bounded (max tokens)?
- [ ] Structured output format enforced (JSON/Pydantic)?
- [ ] Error responses don't leak internal system details?

---

## 📊 Severity Scale

| Level | Definition | Action |
|-------|-----------|--------|
| 🔴 **Critical** | Security risk or crash | Reject, must fix |
| 🟠 **High** | Major bug or design flaw | Request changes |
| 🟡 **Medium** | Code quality issue | Nice to fix |
| 🟢 **Low** | Style / preference | Optional |

---

## 📋 Audit Report Template

```markdown
## Code Audit Report

**Auditor:** [Name] | **Date:** [YYYY-MM-DD]
**Module:** [What was audited]
**Overall Risk:** LOW / MEDIUM / HIGH

---

### 🔴 Critical Issues (Must Fix)
1. [Issue] - Line X - [Why it matters]
2. [Issue] - Line Y

### 🟠 High Priority
1. [Issue]

### 🟡 Medium Priority
1. [Issue]

### 🟢 Low Priority (Optional)
1. [Issue]

---

### Verdict: [SAFE / NEEDS FIXES / REJECT]

---

### Sign-off
- Approved by: [Name]
- Date: [YYYY-MM-DD]
```

---

## 🎯 Quick Audit (10 min)

**If time-limited, audit these first:**
1. Security constraints (hardcoded secrets?)
2. Error handling (try-catch present?)
3. Input validation (sanitized?)
4. N+1 queries (loop + query?)
5. Test coverage (>= 80%?)
6. RAG fallback (empty results handled?)
7. AI output grounded (sources cited?)

---

## 🔗 Reference Docs

- Security Constraints: [`../risk-management/security-constraints.md`](../risk-management/security-constraints.md)
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Error Reference: [`../reference/error-reference-complete.md`](../reference/error-reference-complete.md)

---

**Audit Checklist Version:** 1.1 | **Last Updated:** 2026-05-13
