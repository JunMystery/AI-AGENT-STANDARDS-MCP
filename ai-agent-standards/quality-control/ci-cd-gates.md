# CI/CD Gates — Quality Control Pipeline Integration

**How to integrate quality control into Continuous Integration.**

---

## 🎯 Overview

Automate AI code quality control using gates in the CI/CD pipeline.

```
┌─ Git Push
│
├─ Pre-commit checks (local)
│  ├─ Prettier (format)
│  ├─ ESLint (lint)
│  └─ Type check (tsc)
│
├─ GitHub Actions / CI Server
│  ├─ Unit Tests (Jest)
│  ├─ Test Coverage (>80%)
│  ├─ SAST (SonarQube, Snyk)
│  └─ Special AI-Assisted flag
│
└─ Manual Approval Gate (Code Review)
```

---

## 🔧 Setup Guide

### 1. GitHub Actions Workflow

**File: `.github/workflows/ai-code-check.yml`**

```yaml
name: AI-Assisted Code Quality Gate

on:
  pull_request:
    paths-ignore:
      - 'docs/**'
      - '**.md'

jobs:
  ai-code-quality:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      # Format check
      - name: Check Prettier formatting
        run: npm run prettier:check
      
      # Lint check
      - name: Run ESLint
        run: npm run lint
      
      # Type check
      - name: TypeScript type check
        run: npm run type-check
      
      # Unit tests
      - name: Run unit tests
        run: npm run test:unit
      
      # Coverage
      - name: Check test coverage
        run: |
          npm run test:coverage
          if [ $(cat coverage/coverage-summary.json | jq '.total.lines.pct') -lt 80 ]; then
            echo "Coverage below 80%"
            exit 1
          fi
      
      # Security scan
      - name: SAST - SonarQube scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      
      # Check for AI flag
      - name: Check AI-Assisted label
        if: contains(github.event.pull_request.labels.*.name, 'AI-Assisted')
        run: |
          echo "⚠️ This PR contains AI-assisted code"
          echo "Requires: 2 reviewers + Self-Check report"
      
      # FAIL if any gate failed
      - name: Summary
        if: failure()
        run: |
          echo "❌ AI Code Quality Gate FAILED"
          echo "Please fix: formatting, linting, tests, coverage"
          exit 1
      
      # PASS
      - name: Success
        if: success()
        run: echo "✅ All gates passed - ready for review"
```

---

### 2. Local Pre-commit Hook

**File: `.husky/pre-commit`**

```bash
#!/bin/sh

echo "🔍 Running pre-commit checks..."

# Format
npm run prettier:fix || exit 1

# Lint
npm run lint || exit 1

# Type check
npm run type-check || exit 1

# Short unit tests
npm run test:quick || exit 1

echo "✅ Pre-commit checks passed"
```

---

### 3. PR Template with AI Checklist

**File: `.github/pull_request_template.md`**

```markdown
## Description
[Brief description of changes]

## Type of Change
- [ ] AI-Assisted code
- [ ] Manual code review only
- [ ] Refactor
- [ ] Bug fix

---

## ✅ AI Code Checklist (if AI-Assisted)

- [ ] Self-Check Report included?
- [ ] Test coverage >= 80%?
- [ ] No hardcoded secrets?
- [ ] Error handling complete?
- [ ] Code review checklist passed?

---

## Reviewers
[Assign reviewers]

## Labels
[Add: AI-Assisted, if applicable]
```

---

## 🚦 Gate Requirements

### Mandatory Gates (Always Run)

| Gate | Tool | Pass Criteria | Impact |
|------|------|--------------|--------|
| **Format** | Prettier | 0 format errors | Block if fail |
| **Lint** | ESLint | 0 errors (warnings OK) | Block if fail |
| **Type Check** | TypeScript | 0 type errors | Block if fail |
| **Unit Tests** | Jest | All pass + >= 80% coverage | Block if fail |
| **Security** | Snyk / SonarQube | 0 critical vulnerabilities | Block if fail |

### AI-Specific Gates (if `AI-Assisted` label)

| Gate | Check | Pass Criteria | Impact |
|------|-------|--------------|--------|
| **Self-Check Report** | Presence | Included in PR | Block if missing |
| **Reviewer Count** | Manual | 2 reviewers | Block if < 2 |
| **AI Audit Checklist** | Manual | Completed | Block if incomplete |

---

## 📋 Configuration Files

### `prettier.json`
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

### `.eslintrc.js`
```javascript
module.exports = {
  extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended'],
  rules: {
    'no-any': 'warn',
    'no-console': 'warn',
    '@typescript-eslint/no-explicit-any': 'error',
  }
};
```

### `jest.config.js`
```javascript
module.exports = {
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

---

## 🎯 Decision Logic

```
Is this AI-Assisted code?
├─ YES
│  ├─ Self-Check report present? → Continue
│  ├─ All mandatory gates pass? → Continue
│  ├─ 2+ reviewers approve? → Continue
│  ├─ Audit checklist complete? → MERGE ✅
│  └─ Otherwise → REQUEST CHANGES ❌
│
└─ NO
   ├─ All mandatory gates pass? → Code review only
   ├─ 1 reviewer approves? → MERGE ✅
   └─ Otherwise → REQUEST CHANGES ❌
```

---

## 📊 Metrics Collection

**Log from CI/CD:** (Store in datastore)

```json
{
  "pr_id": "PR-123",
  "is_ai_assisted": true,
  "gates_passed": {
    "prettier": true,
    "eslint": true,
    "tsc": true,
    "tests": true,
    "coverage": true,
    "security": true
  },
  "coverage_percentage": 85,
  "test_count": 42,
  "review_time_minutes": 25,
  "iterations_needed": 2,
  "timestamp": "2026-05-12T10:30:00Z"
}
```

---

## 🚨 Troubleshooting Gates

| Gate Failure | Cause | Solution |
|--------------|-------|----------|
| Prettier | Format mismatch | Run `npm run prettier:fix` |
| ESLint | Linting errors | Run `npm run lint:fix` |
| TypeScript | Type errors | Update types or assertions |
| Tests | Failing tests | Debug & fix logic |
| Coverage | Below 80% | Add unit tests |
| Security | Vulnerabilities | Update dependencies or fix |

---

## 🔗 Integration Points

### Jira / Linear
```
PR → Auto-update ticket:
- Add link to PR
- Set status: "In Review"
- Require: AI-Assisted label if needed
```

### Slack Notification
```
GitHub → Slack Bot:
- Notify on gate fail
- Link to PR & logs
- Mention reviewers
```

### Email Alerts
```
CI → Email on critical failures:
- Security vulnerabilities detected
- Multiple coverage failures
```

---

## 🎓 Best Practices

1. **Run locally first** - Use pre-commit hooks
2. **Clear failure messages** - Log tells what to fix
3. **Fast feedback** - Gates should complete in < 5 min
4. **No false positives** - Avoid noisy warnings
5. **Document exceptions** - If must skip gate, log reason

---

## 📚 Reference

- GitHub Actions Docs: https://docs.github.com/en/actions
- ESLint Docs: https://eslint.org/docs/rules/
- Jest Coverage: https://jestjs.io/docs/coverage
- SonarQube: https://docs.sonarqube.org/

---

**CI/CD Gates Version:** 1.0 | **Last Updated:** 2026-05-12
