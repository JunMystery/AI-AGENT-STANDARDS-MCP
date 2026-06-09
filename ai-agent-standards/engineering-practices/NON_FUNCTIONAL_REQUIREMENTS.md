# Non-Functional Requirements (NFRs)

This document outlines the performance, scalability, and reliability standards that code must meet.

> **When to use this skill:** `@reference` this file when the AI is optimizing code, designing database schemas, or writing API endpoints.

---

## 1. Performance Budgets

Applications must adhere to strict performance limitations to ensure a high-quality user experience.

- **API Response Time:** P95 response time MUST be `< 200ms`. Critical APIs should aim for `< 50ms`.
- **Frontend Bundle Size:** Core JS bundles MUST be `< 200KB` (minified and gzipped). Use code-splitting and lazy loading.
- **Web Vitals:** Web applications must pass Google's Core Web Vitals (LCP < 2.5s, FID < 100ms, CLS < 0.1).

## 2. Database Query Optimization

AI Agents are prone to writing inefficient queries if not strictly guided. 

- **No N+1 Queries:** Always use JOINs, Eager Loading, or DataLoader patterns to resolve related entities. N+1 queries are strictly forbidden.
- **Indexing:** Any column used in a `WHERE`, `ORDER BY`, or `JOIN` clause on a large table MUST have an appropriate index.
- **Pagination:** Never return unbounded lists. Always implement limit/offset or cursor-based pagination for collections.

## 3. Caching Strategy

To meet performance budgets and scale effectively, apply caching at appropriate layers:

- **Client-Side:** Utilize HTTP Cache-Control headers, ETags, or Service Workers.
- **Application Level (Memory):** Use Redis or Memcached for frequently accessed, rarely changing data (e.g., user profiles, configuration).
- **CDN:** Serve all static assets (images, CSS, JS) via a Content Delivery Network.

**Cache Invalidation:** Always define a clear cache expiration (TTL) or event-driven invalidation strategy when implementing caching.

## 4. Concurrency & Race Conditions

Code must be thread-safe and resilient to concurrent requests.

- **Idempotency:** Non-GET API endpoints (POST, PUT, DELETE, PATCH) should be idempotent where possible to safely handle retries.
- **Locking:** Use optimistic locking (version columns) or pessimistic locking (Redis distributed locks / DB row locks) when updating shared state (e.g., account balances, inventory).
- **Async Processing:** Offload heavy computational tasks or slow third-party API calls to background workers (e.g., RabbitMQ, Celery, Kafka) instead of blocking the HTTP thread.
