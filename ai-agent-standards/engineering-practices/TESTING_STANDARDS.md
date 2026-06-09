# Testing Standards

This document defines the automated testing standards to ensure code reliability and prevent regressions.

> **When to use this skill:** `@reference` this file when the AI is asked to write tests, configure testing frameworks, or analyze test coverage.

---

## 1. The Test Pyramid

We advocate for a balanced Test Pyramid approach to optimize feedback speed and confidence:

- **Unit Tests (70%):** Fast, isolated tests for individual functions and classes. These should run in milliseconds. Mock all external dependencies.
- **Integration Tests (20%):** Tests that verify the interaction between components (e.g., API endpoints interacting with a test database).
- **End-to-End (E2E) Tests (10%):** Slow, comprehensive tests simulating user journeys in a browser or device emulator (e.g., Cypress, Playwright). Use sparingly for critical paths.

## 2. Coverage Thresholds

All projects MUST configure CI/CD to block merges if coverage falls below strict thresholds:

- **Line Coverage:** Minimum `80%`
- **Branch/Condition Coverage:** Minimum `70%`

*Note: 100% coverage is often a vanity metric. Focus on testing critical business logic and edge cases rather than boilerplate code.*

## 3. F.I.R.S.T. Principles

All tests written by AI or Human Engineers MUST adhere to the FIRST principles:

- **Fast:** Tests should execute rapidly to encourage frequent running.
- **Isolated (Independent):** Tests must not depend on each other or run in a specific order. State must be reset between tests.
- **Repeatable:** Tests must yield the same result every time, across all environments (no flaky tests).
- **Self-validating:** Tests must automatically detect pass/fail without manual inspection.
- **Timely:** Tests should be written just before or alongside the production code (TDD approach).

## 4. Test-Driven Development (TDD)

We strongly encourage TDD. When prompting the AI to build a feature:

1. **Ask the AI to write the tests first**, defining the expected behavior.
2. Verify the tests fail.
3. Ask the AI to write the minimum code necessary to make the tests pass.
4. Refactor.

## 5. Mocking Rules

- **Do not mock the system under test.**
- **Mock at the boundaries:** Only mock external I/O (Database, Network, File System, Time).
- **Avoid Over-mocking:** If a mock is larger than the implementation, consider an integration test.
