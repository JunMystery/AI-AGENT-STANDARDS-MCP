---
id: PROMPT-003
version: 1.0
author: AI Agent Coding Framework
last_updated: 2026-05-12
applicable_stack: [Node.js, Jest, TypeScript]
category: Testing
difficulty: Simple
---

# Prompt: Generate Unit Tests - Jest Test Suite Generation

**Purpose:** Auto-generate unit tests for a business logic module

---

## [CONTEXT]

- **Tech stack:** Node.js 18, Jest 29.x, TypeScript
- **Module to test:**
  ```typescript
  // src/utils/calculator.ts
  export class Calculator {
    add(a: number, b: number): number { return a + b; }
    subtract(a: number, b: number): number { return a - b; }
    divide(a: number, b: number): number {
      if (b === 0) throw new Error('Division by zero');
      return a / b;
    }
  }
  ```
- **Test setup:** Jest already configured, test runner ready

---

## [TASK]

**Objective:** Create unit tests covering the `Calculator` class

**Acceptance Criteria:**
- [ ] 100% code coverage (add, subtract, divide methods)
- [ ] Test normal cases (valid inputs)
- [ ] Test edge cases (zero, negative numbers)
- [ ] Test error cases (division by zero)
- [ ] Each method has minimum 3 test cases
- [ ] Test naming: `describe()` + `it()` descriptive
- [ ] File: `src/utils/calculator.spec.ts`

---

## [CONSTRAINTS]

**REQUIRED:**
- ✓ Use Jest + TypeScript
- ✓ Each test case must be independent
- ✓ Use `expect()` assertions
- ✓ Comments explaining test purpose
- ✓ No mocking unless necessary

**FORBIDDEN:**
- ❌ Do not test private methods
- ❌ Do not skip tests (`it.skip()`)

---

## [OUTPUT FORMAT]

- **Format:** TypeScript Jest spec file
- **Include:** Coverage report (screenshot or metrics)
- **Length:** Code only

---

## 📝 Reference

- Testing Best Practices: [`../../reference/use-case-cookbook.md`](../../reference/use-case-cookbook.md)
