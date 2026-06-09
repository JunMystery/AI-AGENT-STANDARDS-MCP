---
id: PROMPT-005
version: 1.0
author: AI Agent Coding Framework
last_updated: 2026-05-12
applicable_stack: [Node.js, TypeScript, PostgreSQL, Alembic]
category: Database_Management
difficulty: Intermediate
---

# Prompt: Database Migration - Safe Schema Changes

**Purpose:** Create safe database migrations for schema changes (add column, rename table, etc.)

---

## [CONTEXT]

- **Tech stack:** Node.js, TypeScript, PostgreSQL 14, Alembic migrations
- **Current Schema:**
  ```sql
  CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
  );
  ```
- **Migration Tool:** Alembic (Python) or db-migrate (Node.js)
- **Data:** ~500k existing users

---

## [TASK]

**Objective:** Add `phone` column to users table (optional, nullable)

**Acceptance Criteria:**
- [ ] Add `phone VARCHAR(20)` column (nullable)
- [ ] Rollback function created (down migration)
- [ ] Table lock must not exceed 1 second
- [ ] Migration scripts tested locally
- [ ] Data backup before migration

---

## [CONSTRAINTS]

**FORBIDDEN:**
- ❌ Do not drop existing data
- ❌ Do not make non-nullable columns nullable
- ❌ Do not remove constraints

**REQUIRED:**
- ✓ Down (rollback) migration mandatory
- ✓ Comments explaining schema change
- ✓ Test rollback locally

---

## [OUTPUT FORMAT]

- **Format:** Migration scripts (up + down)
- **Include:** Rollback test results
- **Length:** Code only

---

## 📝 Reference

- Risk Management: [`../../risk-management/`](../../risk-management/)
