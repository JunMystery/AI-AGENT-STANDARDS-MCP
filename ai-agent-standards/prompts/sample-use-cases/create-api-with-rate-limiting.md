---
id: PROMPT-001
version: 1.0
author: AI Agent Coding Framework
last_updated: 2026-05-12
applicable_stack: [Node.js, Express, TypeScript, PostgreSQL]
category: API_Development
difficulty: Intermediate
---

# Prompt: Create API Endpoint with Rate Limiting & Authentication

**Purpose:** Create POST `/api/login` endpoint with JWT authentication + rate limiting, suitable for authentication flow

---

## [CONTEXT]

- **Tech stack:** Node.js 18, Express, TypeScript, PostgreSQL, jsonwebtoken, express-rate-limit
- **Current state:** Project has existing folder structure (`src/controllers`, `src/services`, `src/models`)
- **Database Schema:**
  ```typescript
  User {
    id: number (primary key)
    email: string (unique)
    password: string (hashed)
    created_at: timestamp
  }
  ```
- **Existing Code:**
  - Database connection already set up
  - User model has `findByEmail()`, `comparePassword()` methods
  - Global auth middleware available

---

## [TASK]

**Objective:** Create a secure login endpoint with JWT authentication

**Input:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Output (Success - 200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

**Output (Error - 400/401):**
```json
{
  "error": "Invalid email or password"
}
```

**Acceptance Criteria:**
- [ ] Validate email format & password length (min 8 chars)
- [ ] Rate limiting: Max 5 attempts per 15 minutes per IP
- [ ] Return 429 (Too Many Requests) when limit exceeded
- [ ] Password hashing — NEVER store plaintext
- [ ] JWT token with expiry = 24 hours
- [ ] Log login attempts (success & failure)
- [ ] Return 400 if email/password missing
- [ ] Return 401 if email not found or password incorrect

---

## [CONSTRAINTS]

**FORBIDDEN:**
- ❌ Do not hardcode JWT secret — must come from .env
- ❌ Do not store plaintext passwords
- ❌ Do not log sensitive data (passwords, tokens)
- ❌ Do not modify database schema
- ❌ Do not use `any` type in TypeScript

**REQUIRED:**
- ✓ Try-catch for all database queries
- ✓ Input validation with zod or joi
- ✓ Rate limiter must use `express-rate-limit`
- ✓ Error messages must not reveal sensitive info
- ✓ Unit tests mandatory (min 80% coverage)
- ✓ Comments explaining business logic

**Process:**
- ✓ Run Self-Check before output
- ✓ Include Self-Check report & unit test examples

---

## [OUTPUT FORMAT]

- **Format:** TypeScript code for `src/controllers/auth.controller.ts`
- **Include:** Service method `src/services/auth.service.ts` if logic is complex
- **Style:** ESLint + Prettier
- **Length:** Code only (no lengthy explanations)
- **Include:** Self-Check report + unit test skeleton

---

## 📝 Reference

- Section III.2: Standard Prompt Template
- Section IV.5: Cost Control
- Code Review Checklist: [`../../quality-control/code-review-checklist.md`](../../quality-control/code-review-checklist.md)
