# Karpathy Principles Guide - Detailed Training

**Comprehensive training guide for the 4 Karpathy Principles**

**For:** Engineers new to AI-Coding-Standards framework  
**Time:** 20-30 minutes  
**Prerequisites:** Read quick-reference.md (5 min)

---

## Introduction: Why These Principles?

LLM coding mistakes follow predictable patterns:

| Mistake | Root Cause | Principle That Prevents It |
|---------|------------|--------------------------|
| Code solves wrong problem | Hidden assumptions | #1: Think Before Coding |
| 300-line solution instead of 50 | Over-engineering | #2: Simplicity First |
| Review takes 2 hours, diff is huge | Scope creep | #3: Surgical Changes |
| "Works but doesn't verify to requirements" | Vague goals | #4: Goal-Driven Execution |

**The Karpathy Principles directly address these** by promoting careful analysis, simplicity, precision, and verification.

---

## 🎓 Principle 1: Think Before Coding

**Concept:** Surface ambiguity and make careful decisions BEFORE implementation

### Why It Matters

**The Problem:**
```
Engineer: "Add a feature to export user data"
AI (without thinking):
  - Assumes "export ALL users"
  - Assumes "JSON format"
  - Assumes "write to disk"
  - Assumes "these 5 fields"
  
Result: 200 lines of wrong code
Rework required: 1-2 hours
```

**With Principle #1:**
```
AI responds:
"Before I code, let me surface assumptions:

1. **Scope:** All users or filtered subset? (privacy?)
2. **Format:** File download, API response, or email?
3. **Fields:** All fields or specific subset? (sensitive data?)
4. **Volume:** How many users? Affects approach

I recommend: Start with paginated API endpoint

Clarify above, then I'll implement."

Result: 30 lines of correct code in first try
```

### The Three Components

#### 1a. State Assumptions Explicitly

**What it means:** Before coding, list what you're assuming about the requirement

**Example:**

```
Request: "Add caching to improve performance"

My assumptions:
1. You want in-memory caching (not Redis)
2. Cache should persist for 5 minutes
3. Cache key is the user ID
4. Memory limit: OK with 100MB

Are these correct? Or should I adjust?
```

**Why:** Different people have different assumptions. Surface them.

#### 1b. Present Multiple Interpretations

**What it means:** If the request is ambiguous, show ALL valid interpretations (don't pick one silently)

**Example:**

```
Request: "Make search faster"

This could mean 3 different things:

Option A: Faster response time (500ms → 100ms)
  - Solution: Database indexing
  - Effort: 2 hours
  - Risk: Low

Option B: Handle more concurrent searches
  - Solution: Async queries + connection pooling
  - Effort: 4 hours  
  - Risk: Medium

Option C: Faster perceived speed (UX)
  - Solution: Show partial results immediately
  - Effort: 3 hours
  - Risk: High (UI complexity)

Which matters most for your use case?
```

**Why:** Engineers often say "faster" when they mean something specific. Different solutions for each.

#### 1c. Ask Clarifying Questions BEFORE Implementing

**What it means:** Stop and ask instead of guessing

**Example:**

```
❌ WRONG: Implement immediately with guesses
✅ RIGHT: 
"I see the request is: 'Add user role-based access'

Before I implement, clarify:
- How many roles? (admin, user, guest? or many more?)
- Who assigns roles? (admin panel? API? database seed?)
- Do role permissions change at runtime?
- Should I add role seeding to migrations?

These questions affect the implementation approach."
```

**Why:** Implementation details depend on context. Guessing = rework.

### How to Apply in Practice

**When writing a prompt for AI:**

```markdown
## My Task: [What do I want?]

### Assumptions I'm Making
- [Assumption 1]
- [Assumption 2]

### Success Criteria (Verifiable)
- [Criterion 1: how I'll check]
- [Criterion 2: how I'll check]

### Context
- [Relevant code]
- [Relevant documentation]

### Constraints
- [Constraint 1]
- [Constraint 2]

---

AI, before you code:
1. State if these assumptions are correct
2. If ambiguous, present options
3. Ask any clarifying questions
4. Confirm you understand success criteria
```

**When reviewing code from AI:**

- [ ] Did AI state assumptions explicitly?
- [ ] If ambiguous, did AI present multiple options?
- [ ] Were clarifying questions asked BEFORE coding started?
- [ ] Are success criteria clear and verifiable?

---

## 🎓 Principle 2: Simplicity First

**Concept:** Write minimum code that solves the problem—nothing speculative

### Why It Matters

**The Problem:**
```
Request: "Add a discount calculation"

Over-engineered version:
- Abstract classes (DiscountStrategy, FixedDiscount, PercentageDiscount)
- Dataclasses for configuration
- Type hints everywhere
- Factory patterns
- 150+ lines

Simple version:
def apply_discount(amount, discount_type, value):
    if discount_type == 'percent':
        return amount * (1 - value/100)
    else:
        return max(0, amount - value)

Result: 8 lines vs 150 lines
Bugs: 0 vs multiple | Test time: 5 min vs 1 hour
```

### The Five Rules of Simplicity

#### 2a. No Features Beyond What Was Asked

**What it means:** Code exactly what was requested—no more

**Example:**

```
Request: "Add email validation"

✅ SIMPLE: 
def is_valid_email(email):
    return '@' in email and '.' in email.split('@')[1]

❌ OVERCOMPLICATED:
def is_valid_email(email, check_mx=False, allow_subdomains=True):
    # RFC 5322 full implementation
    # MX record checking
    # Subdomain configuration
    # 200 lines
```

**Why:** Speculative features add complexity without value. Engineer can ask for them.

#### 2b. No Abstractions Unless Reused 2+ Times

**What it means:** Don't extract to a utility function unless you use it 2+ times

**Example:**

```
Request: "Format error messages"

✅ SIMPLE (1 use case): 
error_msg = f"Invalid: {field_name}"

❌ OVERCOMPLICATED (1 use case):
def format_error(field, message):
    return f"Invalid {field}: {message}"

error_msg = format_error("email", "Invalid format")

GOOD (multiple uses):
✅ Extract after you use it 3 times
```

**Why:** Premature abstraction adds indirection. Keep it simple until you have reason to abstract.

#### 2c. No Defensive Error Handling for Impossible Cases

**What it means:** Handle real errors, not theoretical ones that can't happen

**Example:**

```
Request: "Get user by ID"

✅ SIMPLE:
user = User.find(user_id)
if not user:
    raise UserNotFound(user_id)

❌ DEFENSIVE:
try:
    user = User.find(user_id)
    if not user:
        raise UserNotFound(user_id)
    # Check if the database is None (can't happen)
    # Check if user_id somehow changed (can't happen)
    # Handle cosmic rays corrupting data (can't happen)
except Exception as e:
    if user is None and db is None:
        ...  # Many impossible cases
```

**Why:** Impossible error handling clutters code without preventing real bugs.

#### 2d. Every Line Must Earn Its Place

**What it means:** If you write 200 lines and could write 50, rewrite it

**Test:** "Would a senior engineer say this is overcomplicated?"  
If YES → Simplify

**Example:**

```
200-line version:
- Multiple inheritance
- Generic types
- Builder pattern  
- Strategy pattern
- Decorator pattern
- 5 levels of indirection

50-line version:
- Direct function calls
- Simple conditionals
- Readable variable names

Senior engineer says: "Why so complicated?"
→ Simplify immediately
```

#### 2e. The "Simplicity Question"

Always ask yourself:

```
"Would a senior engineer say this is overcomplicated?"

YES → Rewrite simpler
NO → Ship it
```

### How to Apply in Practice

**When writing code:**

1. Write the simplest thing that works
2. Run tests
3. Ask: "Could this be 50% shorter?"
4. If yes: refactor to simpler version
5. Ship the simpler version

**When reviewing AI code:**

- [ ] Does this directly solve the problem?
- [ ] Any speculative features? (Remove them)
- [ ] Any abstractions for single use? (Inline them)
- [ ] Any defensive error handling? (Remove it)
- [ ] Could this be significantly simpler? (If yes, request change)

---

## 🎓 Principle 3: Surgical Changes

**Concept:** Touch only what you must. Clean up only your own mess.

### Why It Matters

**The Problem:**
```
Request: "Add input validation to login function"

Wide scope (WRONG):
- Adds validation (good)
- Refactors error handling (bad—not asked)
- Rewrites logging (bad—not asked)
- Reformats entire file (bad—not asked)
- Removes dead code (bad—not asked)

Result: 
- Huge diff (500 lines changed)
- Code review takes 2 hours (have to check each change)
- Risk of introducing bugs in unrelated code
- Easy to miss the actual validation logic

Surgical scope (RIGHT):
- Adds ONLY validation
- Leaves other code untouched
- Preserves style and formatting
- Small diff (20 lines changed)

Result:
- Review takes 10 minutes (easy to follow)
- Low risk (only touched what was asked)
- Clear what changed and why
```

### The Surgical Rules

#### 3a. Touch ONLY What You Must

**What it means:** Make changes that directly solve the problem, nothing else

**Example:**

```
Request: "Add caching to the getUserById function"

✅ SURGICAL:
- Add cache check at start
- Add cache update at end
- Nothing else

❌ NOT SURGICAL:
- Add caching (good)
- Refactor the error handling (not asked)
- Rewrite variable names (not asked)
- Extract helper function (not asked)
```

**Test:** "Does every changed line directly solve the stated problem?"  
If NO → Remove that change

#### 3b. Match Existing Style—Don't "Improve"

**What it means:** Code like the rest of the project, even if you prefer different style

**Example:**

```
Project style:
- camelCase for variables
- 4-space indentation
- Single quotes for strings

Your preference:
- snake_case  
- 2-space indentation
- Double quotes

✅ RIGHT: Follow project style (camelCase, 4 spaces, single quotes)
❌ WRONG: Use your preferred style
```

**Why:** Consistent style makes code readable. Don't change it just because you prefer different style.

#### 3c. Don't Refactor Unrelated Code

**What it means:** If it's not broken and not touched by your change, don't fix it

**Example:**

```
Task: "Add new user endpoint"

You notice: Old password hashing function is weak

✅ RIGHT:
- Add new endpoint
- Mention: "Old password function might be weak"
- Don't change the old function

❌ WRONG:
- Add new endpoint  
- Refactor old password function
- Now reviewer has to check 2 unrelated things
```

**Why:** Mixing concerns = harder review + more bugs.

#### 3d. Clean Up Only Your Own Mess

**What it means:**
- If YOUR changes create unused imports → Remove them
- If YOUR changes create dead code → Remove it
- If YOUR changes break something → Fix it
- If pre-existing dead code exists → Leave it

**Example:**

```
Request: "Remove the old cache function"

❌ WRONG (too much):
- Remove old cache function
- While you're at it: remove other dead code you see
- Clean up formatting elsewhere

✅ RIGHT:
- Remove old cache function (asked for it)
- Remove imports that were ONLY used by old cache (your cleanup)
- Leave other dead code (not your mess)
```

**Why:** Only your changes = only your responsibility.

#### 3e. Every Line Traces to the Request

**Test:** Pick any line you changed. Can you point to the request and say "that line solves this part"?

If NO → That line doesn't belong

### How to Apply in Practice

**When making changes:**

1. Look at the request
2. Identify exactly what needs to change
3. Make ONLY those changes
4. Before submitting, review your diff:
   - Every line changed = direct solution?
   - Any unrelated improvements? (Remove them)
   - Any style changes? (Revert them)
   - Any dead code removal? (Unless it's your orphans)

**When reviewing AI code:**

- [ ] Changes minimal and focused?
- [ ] Unrelated refactoring? (Request surgical rework)
- [ ] Unnecessary reformatting? (Reject)
- [ ] Pre-existing issues "fixed"? (Reject—not asked)
- [ ] Code style consistent with project? (If not, reject)

---

## 🎓 Principle 4: Goal-Driven Execution

**Concept:** Define verifiable success criteria upfront. Verify before considering done.

### Why It Matters

**The Problem:**
```
Request: "Fix the bug"

Vague criteria (WRONG):
- "Make it work"
- "Fix the issue"
- "It should be faster"

Result:
- AI implements something
- Engineer says "that's not what I meant"
- Rework required
- Wasted effort

Clear criteria (RIGHT):
- Bug: Users can't login when name has special character
- Success: 
  * Test writes case with name "José" → login succeeds
  * Test writes case with name "李" → login succeeds
  * All existing tests still pass

Result:
- AI implements exactly this
- Engineer verifies criteria met
- Done in first try
```

### The Goal-Driven Rules

#### 4a. Define Verifiable Success Criteria

**What it means:** Success is measurable, not subjective

**Examples of VAGUE criteria:**
- "Make it better"
- "Optimize the code"
- "Fix the performance issue"
- "Improve error handling"

**Examples of VERIFIABLE criteria:**
- "Response time < 100ms (benchmark with [dataset])"
- "All unit tests pass + coverage >= 80%"
- "Users can login with email addresses containing non-ASCII characters"
- "Cache hit rate >= 85% (test with production-like data)"

**Test:** "How will the engineer VERIFY this is done?"  
If answer requires judgment → Not verifiable. Make it concrete.

#### 4b. Transform Vague Tasks into Testable Goals

**What it means:** Break down vague requests into steps with verification

| Vague Request | → | Testable Goal |
|---|---|---|
| "Add validation" | | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | | "Write test reproducing bug, then fix code until test passes" |
| "Refactor X" | | "Ensure tests pass before & after, measure complexity/performance" |
| "Make it faster" | | "Define metric, benchmark baseline, improve metric by X%, verify" |
| "Improve security" | | "List specific threat, write test for threat, implement fix" |

**Example:**

```
Vague: "Add email validation to signup"

Testable:
1. Write test_valid_emails() - test all valid formats → expect pass
2. Implement email validation → make test pass
3. Write test_invalid_emails() - test all invalid formats → expect fail
4. Verify: coverage >= 80%

Success verified when: All tests pass
```

#### 4c. State a Clear Plan with Verification Steps

**What it means:** For multi-step tasks, break down into steps + verification

**Example:**

```
Task: Implement caching for user queries

Plan:
1. Add in-memory cache object
   → Verify: Cache stores 100+ entries

2. Add cache.get() before database query
   → Verify: test_cache_hit() passes (validates hit rate)

3. Add cache.set() after database query
   → Verify: test_cache_set() passes

4. Add cache invalidation on user update
   → Verify: test_invalidation() passes

5. Benchmark performance
   → Verify: Response time < 50ms, hit rate >= 80%

Success: All 5 verification steps pass
```

#### 4d. Verify Success Before Considering Done

**What it means:** Run verification steps, confirm they pass, THEN submit

**Example:**

```
Before submitting:

[] Do all tests pass? ✓ 24/24 pass
[] Is coverage >= 80%? ✓ 87%
[] Does performance meet target? ✓ 45ms < 50ms target
[] Did I break anything? ✓ All existing tests still pass

→ Ready to submit
```

### How to Apply in Practice

**When writing a prompt:**

```markdown
## Success Criteria (Verifiable)

1. [Criterion 1]
   - How I'll verify: [specific check]
   
2. [Criterion 2]
   - How I'll verify: [specific check]

3. [Criterion 3]
   - How I'll verify: [specific check]

(Include test cases or metrics)
```

**When reviewing AI code:**

- [ ] Success criteria from request are clearly met?
- [ ] How was each criterion verified?
- [ ] Tests passing? Coverage adequate?
- [ ] Observable outcome confirmed?
- [ ] Metrics improved (if applicable)?

---

## 📝 Workshop: Putting It Together

### Exercise 1: Identify Principle Violations

**Scenario 1:**

```
Request: "Add a button to the form"

AI Response:
"Sure! I'll add a button. Also, I noticed the form CSS is messy, 
so I'm refactoring it while I'm here. Also improving the validation 
logic. Also updating the comments. Here's the new code:"
```

**Question:** Which principles violated?

**Answer:**
- #2 (Simplicity): Added unrelated CSS refactoring (not asked)
- #3 (Surgical): Refactored validation and comments (not asked)

---

### Exercise 2: Make a Vague Request Testable

**Vague request:** "Optimize the search"

**Your task:** Transform into verifiable success criteria

**Answer (example):**
```
Optimization request needs clarity:

Option A: Faster response time
- Target: < 200ms for typical query
- Verification: Run search_performance_test.py
- Baseline: Currently 500ms
- Goal: 500ms → < 200ms

Option B: Higher throughput
- Target: Handle 1000 concurrent searches
- Verification: Load test with 1000 concurrent users
- Baseline: Currently handles 100
- Goal: 100 → 1000 concurrent

Option C: Better UX (perceived speed)
- Target: Show first results in 100ms
- Verification: Users see "partial results" in 100ms
- Baseline: Currently wait for all results (500ms)
- Goal: Progressive results in 100ms

Which optimization matters most?
```

---

### Exercise 3: Write Surgical Code

**Request:** "Cache the getUserById function"

**Your task:** Write ONLY changes needed for caching

**Wrong approach:**
```python
# While we're here, let's also:
# - Refactor the error handling
# - Improve the variable names
# - Extract a separate service class
# - Add logging everywhere

def get_user_by_id(user_id):
    # 200 lines of changes...
```

**Right approach:**
```python
# ONLY add caching
_user_cache = {}

def get_user_by_id(user_id):
    if user_id in _user_cache:  # Added: cache check
        return _user_cache[user_id]
    
    user = database.query(User).filter(id=user_id).first()
    
    if user:
        _user_cache[user_id] = user  # Added: cache update
    
    return user
```

---

## 🎯 Quick Reference During Code Review

**Print this and keep handy:**

| Principle | Check Before Approving |
|-----------|----------------------|
| #1: Think Before Coding | Were assumptions clear? Success criteria verifiable? |
| #2: Simplicity First | Could this be written simpler? Any unnecessary abstractions? |
| #3: Surgical Changes | Every line trace to request? Any unrelated changes? |
| #4: Goal-Driven Execution | Success criteria met? Verified? |

---

## 📚 Additional Resources

- **Karpathy Framework:** `principles/karpathy-framework.md` — Deep dive into each principle
- **Code Review Checklist:** `quality-control/code-review-checklist.md` — What to check
- **Examples:** `/andrej-karpathy-skills/EXAMPLES.md` — Real "wrong vs. right" code
- **Quick Reference:** `onboarding/quick-reference.md` — 1-page summary

---

**Next Steps:**
1. Read this guide (20-30 min)
2. Practice with the worksheet: `think-before-coding-worksheet.md`
3. Apply principles to your next AI-assisted task
4. Share feedback on what's confusing

---

**Last Updated:** May 13, 2026  
**Status:** 🟢 Active Training Material
