---
id: PROMPT-002
version: 1.0
author: AI Agent Coding Framework
last_updated: 2026-05-12
applicable_stack: [Node.js, Express, TypeScript, Redis, MongoDB]
category: Performance_Optimization
difficulty: Intermediate
---

# Prompt: Refactor Cache Strategy - Redis Caching Implementation

**Purpose:** Optimize performance with Redis caching for frequently accessed database queries

---

## [CONTEXT]

- **Tech stack:** Node.js 18, Express, TypeScript, Redis 7.x, MongoDB
- **Current issue:**
  - Endpoint GET `/api/products` has N+1 query problem
  - Response time > 500ms, need to optimize to < 100ms
  - Database can't handle peak load
- **Database Queries:**
  ```javascript
  // Current (slow)
  const products = await Product.find();
  for (const product of products) {
    product.category = await Category.findById(product.categoryId);
  }
  ```
- **Traffic Pattern:** 80% read, 20% write
- **Cache Invalidation:** Products update infrequently (~1x/hour)

---

## [TASK]

**Objective:** Implement Redis caching + cache invalidation strategy

**Acceptance Criteria:**
- [ ] GET `/api/products` returns response < 100ms (95th percentile)
- [ ] Cache hit rate > 80% after 5 minutes
- [ ] Cache TTL = 1 hour (configurable)
- [ ] Cache invalidation when product/category is updated
- [ ] Fallback to DB if cache miss or Redis is down
- [ ] Cache key format: `products:list` (clear convention)
- [ ] Support cache warming (pre-populate cache on startup)
- [ ] Log cache hit/miss metrics

---

## [CONSTRAINTS]

**FORBIDDEN:**
- ❌ Do not hardcode Redis URL — must come from .env
- ❌ Do not cache sensitive data (passwords, tokens)
- ❌ Do not cache entire response if it contains user-specific data
- ❌ Do not modify database schema

**REQUIRED:**
- ✓ Try-catch for Redis operations
- ✓ Graceful fallback when Redis is unavailable
- ✓ Implement cache invalidation logic
- ✓ Log cache performance metrics
- ✓ Unit tests for cache layer
- ✓ Comments explaining TTL & invalidation strategy

**Process:**
- ✓ Run Self-Check
- ✓ Include test cases for cache hit/miss scenarios

---

## [OUTPUT FORMAT]

- **Format:** TypeScript files:
  - `src/cache/redis.service.ts` (Redis wrapper)
  - `src/services/product.service.ts` (caching logic)
  - `src/controllers/product.controller.ts` (updated endpoint)
- **Include:** Unit tests + cache strategy diagram
- **Length:** Code only (no explanations)

---

## 📝 Reference

- Performance Best Practices: [`../../reference/use-case-cookbook.md`](../../reference/use-case-cookbook.md)
