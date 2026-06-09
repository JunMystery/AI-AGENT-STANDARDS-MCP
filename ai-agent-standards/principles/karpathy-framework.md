# Karpathy Principles Framework

**Foundational Behavioral Guidelines for AI-Assisted Development**

Based on Andrej Karpathy's observations on LLM coding pitfalls. These principles form the **core philosophy** for all AI-assisted coding in this framework, applied across all tools (Cursor, Claude, Copilot) and workflows.

**Version:** 1.0  
**Status:** Active Foundation  
**Last Updated:** May 13, 2026

---

## Overview: Why These Principles Matter

LLM coding mistakes fall into predictable patterns:
- **Wrong assumptions** → code solves the wrong problem
- **Overcomplication** → unnecessary abstractions, speculative features  
- **Scope creep** → changing unrelated code
- **Vague success criteria** → unclear when the task is done
- **Duplication** → copied logic, schemas, configs, and UI drift
- **Disorganization** → monolithic files and misplaced responsibilities

The Karpathy principles directly address these by promoting **careful analysis, simplicity, precision, verifiable outcomes, reuse, and clear organization**.

---

## 🎯 The 6 Core Principles

### 1. Think Before Coding

**Don't assume. Surface ambiguity. Present alternatives. Ask questions.**

**When:** BEFORE implementation begins (during step 1-2 of pipeline)

**Apply it:**

| Context | What You Do | Red Flag | Green Flag |
|---------|------------|----------|-----------|
| **Receive unclear request** | State assumptions explicitly; if multiple interpretations exist, present them | AI picks one silently without asking | "I see 3 possible interpretations—which is correct?" |
| **Simplification exists** | Mention simpler approaches before committing to complex ones | Implements 300-line architecture without mentioning 50-line alternative | "A simpler approach exists: [X]. Recommend that instead." |
| **Missing info** | Stop. Name what's confusing. Ask before guessing. | Implements with guesses; requires rework | "Unclear: [X]. Need clarification before proceeding." |
| **Implementation scope unclear** | Clarify boundaries: what's IN scope? what's OUT? | Adds features beyond request | "Scope: [what's included]. Out of scope: [what's excluded]" |

**Success Criteria:**
- ✓ Assumptions are stated explicitly before code begins
- ✓ Multiple interpretations are presented (never silently chosen)
- ✓ Clarifying questions appear in prompt or discussion BEFORE implementation
- ✓ Simpler alternatives are identified and recommended

**Complement to AI-Coding-Standards framework:**
- This principle elevates **prompt quality** before sending to AI (step 1 of pipeline)
- Reduces "back-and-forth" iterations by clarifying requirements upfront
- Aligns with `.ai-agent-standards/prompts/HEADER-TEMPLATE.yaml` requirement to define success criteria

**Real Example:**
```
❌ User says: "Add a feature to export user data"
❌ AI assumes: "Export ALL users to JSON file, write to disk, return filename"
❌ Problem: What about privacy, pagination, file location, which fields?

✅ What should happen:
Before coding, AI responds:
"Before I implement, clarify scope:
1. **All users or filtered subset?** (privacy implications)
2. **Output format?** File/API response/email?
3. **Which fields?** Some may be sensitive"
```

---

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

**When:** During code design & implementation (step 3 of pipeline)

**Apply it:**

| What AI Should NOT Do | Why | Test |
|----------------------|-----|------|
| Add features beyond request | Wastes effort, increases bugs | Is every line directly solving the stated problem? |
| Create abstractions for single-use code | Over-engineering; maintenance burden | Would you use this abstraction more than once? |
| Add "flexibility" or "configuration" not requested | Premature generalization | Did the user ask for this configurability? |
| Handle impossible error scenarios | Clutters code with defensive programming | Is this error realistically possible? |
| Write 200 lines when 50 solves it | Code complexity ∝ bugs | Could a senior engineer simplify this? |

**Success Criteria:**
- ✓ Code directly solves the stated problem—no extra features
- ✓ Each function/component does one thing well
- ✓ No defensive error handling for impossible cases
- ✓ Abstractions exist only if reused 2+ times
- ✓ Self-Check Report includes "Simplicity verification" section

**Complement to AI-Coding-Standards framework:**
- Part of **quality-control pipeline** (step 4)
- Reviewers use code-review-checklist.md to verify "no extra features" and "reasonable complexity"
- Reduces technical debt and testing burden

**Real Example:**
```
❌ Request: "Add a function to calculate discount"
❌ AI provides: 150-line DiscountStrategy pattern with abstract classes, 
   enums, dataclasses, configurable min/max bounds

✅ What should happen: 40-line function
def apply_discount(amount: float, discount_type: str, discount_value: float):
    if discount_type == 'percent':
        return amount * (1 - discount_value / 100)
    elif discount_type == 'fixed':
        return max(0, amount - discount_value)
```

---

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

**When:** During code editing & integration (step 3 of pipeline)

**Apply it:**

| Situation | What's Surgical | What's NOT Surgical |
|-----------|-----------------|-------------------|
| **Editing existing code** | Change only the lines solving the problem | "Improve" adjacent code, reformat unrelated sections |
| **Style differences** | Match existing style, even if different from yours | Enforce your preferred style on old code |
| **Dead code noticed** | Mention it; don't delete unless asked | Delete pre-existing dead code unprompted |
| **Your changes create orphans** | Remove imports/vars YOUR change made unused | Remove old unused code |
| **Refactoring urge** | Fix only things YOUR changes broke | Refactor working code just because |

**Success Criteria:**
- ✓ Every changed line traces directly to user's request
- ✓ No unrelated reformatting or style changes
- ✓ Pre-existing issues are mentioned, not fixed
- ✓ Only orphans created BY this change are removed
- ✓ Git diff shows surgical precision (small, focused changeset)

**Complement to AI-Coding-Standards framework:**
- Enforces "controlled AI" philosophy—AI doesn't decide what "good code" looks like
- Reduces review friction (smaller diffs are easier to verify)
- Prevents scope creep in change requests
- Aligns with risk-management principle: "AI changes only what's requested"

**Real Example:**
```
❌ Request: "Add input validation to login function"
❌ AI also: Refactors error handling, rewrites logging, reformats the whole file

✅ What should happen: ONLY add validation
- If input validation added → OK
- If error handling improved → NOT OK (unless your validation broke it)
- If file reformatted → NOT OK
- If someone else's dead code removed → NOT OK
```

---

### 4. Goal-Driven Execution

**Define verifiable success criteria. Test until satisfied.**

**When:** Task planning & verification (steps 1 & 7 of pipeline)

**Apply it:**

| Vague Criteria | ↓ Transform Into | Verifiable Outcome |
|---|---|---|
| "Add validation" | Write tests for invalid inputs, then make them pass | ✓ Tests run, all pass |
| "Fix the bug" | Write a test reproducing the bug, then make it pass | ✓ Test went from fail→pass |
| "Refactor X" | Ensure tests pass before & after refactor, verify performance | ✓ Metrics show improvement |
| "Make it faster" | What does "faster" mean? Response time? Throughput? | ✓ Metric [X] improved by [Y]% |
| "Clean up code" | Which specific code? What does "clean" mean? | ✓ Complexity metrics reduced |

**For multi-step tasks, create a brief plan:**
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

**Success Criteria:**
- ✓ Success is objectively measurable (tests, metrics, or observable change)
- ✓ Criteria defined BEFORE coding begins (in prompt step 1)
- ✓ Verification steps are part of the task plan
- ✓ Self-Check Report includes verification results
- ✓ AI iterates until criteria are met (no "hope it works")

**Complement to AI-Coding-Standards framework:**
- **Core to prompt quality**: HEADER-TEMPLATE.yaml requires "Success Criteria" field
- **Enables independent iteration**: Strong criteria let AI loop without asking for clarification
- **Reduces code review friction**: Reviewers check if criteria met, not subjective quality
- **Part of 7-Step Pipeline**: Steps 1 (define criteria) & 7 (verify metrics) are strengthened

**Real Example:**
```
❌ Request: "Optimize the cache"
❌ Problem: What cache? What metric? Reduced latency? Hit rate? Memory usage?

✅ What should happen (from prompt):
"Optimize the user_cache for faster lookups.
Success Criteria:
- Cache hit rate >= 85% (test with production-like data)
- Lookup time < 5ms (benchmark before/after)
- Memory usage doesn't exceed 100MB
Verification: Run cache_benchmark.test.js, include results in Self-Check Report"
```

---

### 5. DRY & Reusability

**Do not duplicate UI, logic, configs, schemas, types, or test setup.**

**When:** During implementation and review (steps 4-6 of pipeline)

**Apply it:**

| What AI Should Do | Red Flag | Green Flag |
|---|---|---|
| Reuse existing helpers and components | Copies similar logic into a new file | Imports the existing helper or extends it narrowly |
| Keep configs and schemas single-source | Same enum or constant repeated in two places | Shared config/type used by both callers |
| Extract only real reuse | Creates a generic abstraction for one call site | Extracts after 2+ concrete uses or clear local pattern |

**Success Criteria:**
- ✓ No duplicated business logic, UI structure, configs, schemas, or types
- ✓ Existing project helpers are used before adding new ones
- ✓ New abstractions are justified by real reuse
- ✓ Self-Check Report notes any intentional duplication and why it remains

---

### 6. Code Organization

**Put code in the right layer with clear names. Avoid monolithic files.**

**When:** During architecture alignment, implementation, and review (steps 3-6 of pipeline)

**Apply it:**

| What AI Should Do | Red Flag | Green Flag |
|---|---|---|
| Respect existing module boundaries | Controller talks directly to persistence when services exist | Logic stays in the established service/model layer |
| Keep files focused | Adds unrelated functions to a catch-all file | Creates or updates the smallest appropriate module |
| Use clear, general names | Names tied to one prompt or temporary workflow | Names match existing domain vocabulary |

**Success Criteria:**
- ✓ Code lives in the correct layer/module
- ✓ No monolithic files or dumping-ground modules are created
- ✓ Names are clear, general, and consistent with nearby code
- ✓ Architecture constraints and 12 security constraints remain intact

---

## 🔄 Principles in the 7-Step Pipeline

### Where Each Principle Applies

```
STEP 1: Write Prompt
├─ Apply: PRINCIPLE #1 (Think Before Coding)
│  └─ State assumptions, surface ambiguities, define success criteria CLEARLY
│
STEP 2: Paste to AI
├─ Apply: All principles (prompt quality determines output quality)
│
STEP 3: AI Generates Code + Self-Check Report
├─ AI applies: #2 (Simplicity), #3 (Surgical), #4 (Goal-Driven), #5 (DRY), #6 (Organization)
│  └─ Simple, focused, reusable, well-organized code that verifies success criteria
│
STEP 4: Review Code + Self-Check Report ← CRITICAL
├─ YOU verify: All 6 principles
│  ├─ #1: Were assumptions clear? Success criteria defined?
│  ├─ #2: Code simple or overengineered?
│  ├─ #3: Changes surgical or scope-creeping?
│  ├─ #4: Success criteria met? Verified?
│  ├─ #5: Duplication avoided? Existing helpers reused?
│  └─ #6: Code in the correct layer/module?
│
STEP 5: Approve OR Request Changes
├─ If FAIL on any principle → Back to Step 2 with feedback
│
STEP 6: Merge to Git
│  └─ Merged code adheres to all 6 principles
│
STEP 7: Done! Log metrics
```

---

## ✅ Applying Principles: Reviewer Checklist

**When reviewing AI-generated code, check for each principle:**

### Principle 1: Think Before Coding
- [ ] Assumptions were stated explicitly (visible in prompt or discussion)?
- [ ] If multiple interpretations existed, were all presented?
- [ ] Success criteria were defined upfront?
- [ ] No "creative reinterpretation" of the request?

### Principle 2: Simplicity First
- [ ] Code directly solves the problem—no extra features?
- [ ] Functions/classes do one thing well?
- [ ] No defensive error handling for impossible cases?
- [ ] No "future-proofing" abstractions?
- [ ] Could it be written simpler? (If yes, request changes)

### Principle 3: Surgical Changes
- [ ] Git diff shows focused, minimal changes?
- [ ] No unrelated reformatting or refactoring?
- [ ] Pre-existing issues mentioned but not fixed?
- [ ] Only orphans created BY this change are removed?
- [ ] Changes directly trace to the request?

### Principle 4: Goal-Driven Execution
- [ ] Success criteria from prompt are clearly met?
- [ ] Verification steps were performed?
- [ ] Self-Check Report documents verification results?
- [ ] Tests pass? Metrics improved? Observable outcome verified?
- [ ] AI iterated until criteria satisfied (not "hope it works")?

### Principle 5: DRY & Reusability
- [ ] No duplicated UI, logic, configs, schemas, types, or test setup?
- [ ] Existing helpers/components/patterns reused where appropriate?
- [ ] New abstractions justified by real reuse?
- [ ] Any intentional duplication documented?

### Principle 6: Code Organization
- [ ] Code lives in the correct layer/module?
- [ ] No monolithic file or catch-all module created?
- [ ] Names are clear, general, and consistent with nearby code?
- [ ] Architecture and security constraints respected?

**Decision:**
- ✓ **All pass** → Approve & merge
- ✗ **1+ fail** → Request changes, explain which principle violated

---

## 🔗 Integration with Existing Framework

| Framework Component | Karpathy Principle | How They Work Together |
|---|---|---|
| **HEADER-TEMPLATE.yaml** | #1, #4 | Template now requires "Assumptions" and "Success Criteria" fields |
| **code-review-checklist.md** | All 6 | Checklist updated to validate each principle |
| **self-check-report-template.md** | #2, #4 | AI now reports simplicity verification and success criteria met |
| **7-Step Pipeline** | All 6 | Each step references which principles to apply |
| **prompt library** | #1 | Existing prompts reviewed for clarity & assumption-stating |
| **quality-control gates** | All 6 | Automated checks validate principle compliance |
| **onboarding materials** | All 6 | Training now emphasizes principles-first thinking |

---

## 🚫 Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Principle(s) Violated |
|---|---|---|
| **Copy-paste AI code without reading it** | Hidden assumptions, scope creep, overcomplicated | All 6 |
| **"Make the AI implement my entire idea at once"** | Vague criteria, multiple interpretations | #1, #4 |
| **"Let AI refactor while fixing the bug"** | Scope creep, unverified changes | #3, #4 |
| **"Add error handling for every edge case"** | Over-defensive, not simple | #2 |
| **"Implement first, ask questions later"** | Wrong problem solved, wasted effort | #1 |
| **"Accept code that 'looks good' but isn't tested"** | Unverified success criteria | #4 |
| **"Copy-paste similar code because it is faster"** | Duplicated behavior drifts and becomes hard to test | #5 |
| **"Put the new feature in the nearest large file"** | Module boundaries erode; review and maintenance get harder | #6 |
| **"Use an AI agent in autonomous mode"** | No surgical control, wrong assumptions | All 6 |

---

## 📚 References & Extensions

**Foundational sources:**
- [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls
- `/andrej-karpathy-skills/CLAUDE.md` — Detailed principle explanations
- `/andrej-karpathy-skills/EXAMPLES.md` — Real-world "wrong vs. right" code examples

**Framework integration:**
- [HEADER-TEMPLATE.yaml](../prompts/HEADER-TEMPLATE.yaml) — Updated prompt structure
- [code-review-checklist.md](../quality-control/code-review-checklist.md) — Principle validation
- [7-Step Pipeline](../INDEX.md#7-step-pipeline) — Application workflow

**Training materials:**
- [karpathy-principles-guide.md](../onboarding/karpathy-principles-guide.md) — Detailed training
- [think-before-coding-worksheet.md](../onboarding/think-before-coding-worksheet.md) — Interactive exercise

---

## ❓ FAQ

**Q: Aren't these just "best practices"?**  
A: Yes—but they're specific to LLM assistance. Human programmers often rely on context, experience, and cleanup. AI needs explicit, surface-level clarity.

**Q: What if the request IS vague?**  
A: That's the point! Principle #1 says: surfacing vagueness IS the right move. Don't code around it.

**Q: Do I apply all 6 principles to every task?**
A: Yes. For trivial tasks, they're lightweight. For complex tasks, they prevent major rework.

**Q: What if AI refuses to simplify?**  
A: Principle #2 is non-negotiable. Request changes. If AI insists on complexity, escalate or switch models.

**Q: Can I automate principle validation?**  
A: Partially—see CI/CD gates in quality-control/. Code complexity metrics, test coverage, and git diff size can be checked automatically.

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | May 13, 2026 | Initial framework—6 principles, pipeline integration, reviewer checklist |

---

**Last Updated:** May 13, 2026  
**Maintainer:** AI-Coding-Standards Governance Team  
**Status:** 🟢 Active Foundation
