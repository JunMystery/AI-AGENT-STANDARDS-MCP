# Glossary

**Term definitions used in the framework.**

---

## A

**Agentic Coding**
- Approach using AI as an assistant under strict control
- Contrasts with "Vibe Coding" (uncontrolled AI delegation)

**Acceptance Criteria**
- List of clear conditions a task must meet
- Written in the [TASK] section of the prompt

---

## B

**Backward Compatibility**
- New code does not break existing code
- API endpoints not changed unexpectedly
- Database schemas support migration

---

## C

**CI/CD (Continuous Integration/Deployment)**
- Automated pipeline for building, testing, deploying
- Gates control quality before deployment

**Code Review**
- Human review of AI code before merge
- Uses [`code-review-checklist.md`](../quality-control/code-review-checklist.md)

**Constraints**
- Technical rules AI must follow
- Forbidden behaviors + Required behaviors

---

## D

**Definition of Done (DoD)**
- Criteria for a task to be considered complete
- Includes: tests, review, documentation

**Defect**
- Bug found after merge (regression)
- Tracked in metrics

**Duplication (Code)**
- Unnecessary repetition of code patterns
- Target: 0% duplication

---

## E

**Escalation**
- Reporting to a higher level when a problem can't be resolved
- Path: Self → Mentor → Tech Lead → Architect

**Error Handling**
- Try-catch + graceful fallback
- Meaningful error messages

---

## F

**Failure Log**
- Record when AI fails > 2 times
- Uses: [`ai-failure-log-template.md`](../risk-management/ai-failure-log-template.md)

---

## G

**Gate (CI/CD)**
- Automated checkpoint in the pipeline
- Format, lint, tests, security scans

**Glossary**
- This file — term definitions

---

## H

**Hallucination**
- AI generates code/references that don't exist
- Example: importing a non-existent library
- Detection: [`hallucination-detection.md`](../quality-control/hallucination-detection.md)

---

## I

**Input Validation**
- Check user input before processing
- Prevents injection attacks
- Uses: zod, joi libraries

---

## J

**Jira / Linear**
- Project management tools
- Tag AI tasks: `[AI-Assisted]`

---

## K

**KPI (Key Performance Indicator)**
- Metrics measuring performance
- Examples: Defect rate, Cycle time, Coverage

---

## L

**Layer (Architecture)**
- Controller, Service, Model, Utils
- AI code must be placed in the correct layer

**Linting**
- Automated code style checking
- Tool: ESLint
- Enforces consistent formatting

---

## M

**Merge**
- Combine code into main branch (Git)
- Only after all gates pass & review approved

**Metrics**
- Data measuring AI effectiveness

---

## N

**Non-Negotiable Constraints**
- Absolute rules that must not be violated
- Examples: No hardcoded secrets, input validation
- Details: [`security-constraints.md`](../risk-management/security-constraints.md)

**N+1 Query**
- Inefficient DB query pattern
- Loop calls DB multiple times instead of once

---

## O

**Output Format**
- Expected format of AI output
- Examples: Code only, Code + Tests, JSON

---

## P

**Pipeline**
- 7-step process: AI → Review → Merge
- Section III.4 in original documentation

**Prompt**
- Instruction sent to AI
- Template: [`prompts/PROMPT-TEMPLATE.md`](../prompts/PROMPT-TEMPLATE.md)

**Prompt Library**
- Standardized collection of prompts
- Location: [`prompts/`](../prompts/)

---

## Q

**Quality Control**
- Multi-layer checks before merge
- Details: [`quality-control/`](../quality-control/)

---

## R

**Regression**
- New bug introduced by a change
- Prevention: Unit tests + review

**Refactor**
- Rewrite code without changing behavior
- Improve: Performance, readability, maintainability

**Review**
- Human inspection of AI code
- Uses: [`code-review-checklist.md`](../quality-control/code-review-checklist.md)

---

## S

**SAST (Static Application Security Testing)**
- Tool that scans code for security issues
- Examples: SonarQube, Snyk

**Schema**
- Data structure definition
- Database tables, API types

**Security Constraints**
- Non-negotiable security rules
- Details: [`security-constraints.md`](../risk-management/security-constraints.md)

**Self-Check Report**
- AI's self-verification report
- Template: [`self-check-report-template.md`](../quality-control/self-check-report-template.md)

**SQL Injection**
- Security vulnerability from unsanitized input
- Prevention: Parameterized queries

---

## T

**Task**
- Unit of work (story, bug fix)
- Tagged with prompt ID + version when AI-assisted

**Technical Debt**
- Code quality issues accumulated over time
- Must be reduced regularly

**Test Coverage**
- % of code executed by tests
- Target: >= 80%

**Try-Catch**
- Exception handling block
- Mandatory for async operations

---

## U

**Unit Test**
- Test for an individual function/method
- Must be > 80% coverage

---

## V

**Vibe Coding**
- Delegating to AI without oversight or control
- ⚠️ Not recommended — risky!

---

## W

**Walkthrough**
- Step-by-step guide
- First task: [`onboarding/first-task-walkthrough.md`](../onboarding/first-task-walkthrough.md)

---

## X

**XSS (Cross-Site Scripting)**
- Security vulnerability
- Prevention: Input sanitization + CSP headers

---

## Y

**YAML**
- Data format for configs
- Prompt headers use YAML format

---

## Z

**Zero-Trust Security**
- Assume nothing is trusted by default
- Verify all inputs, no hardcoded secrets

**Zod**
- TypeScript-first schema validation library
- Used for input validation

---

**Glossary v1.0 | Last updated: 2026-05-12**

*More terms will be added as framework evolves.*
