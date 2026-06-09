# Think Before Coding Worksheet

**Interactive Exercise: Mastering Principle #1**

**Time:** 30 minutes  
**Prerequisites:** Read karpathy-principles-guide.md first

---

## Overview

This worksheet helps you practice **Principle #1: Think Before Coding** through guided exercises. By the end, you'll be skilled at:

- ✓ Stating assumptions explicitly
- ✓ Surfacing ambiguity
- ✓ Presenting multiple interpretations
- ✓ Asking clarifying questions BEFORE coding

---

## Exercise 1: Identify Hidden Assumptions

**Scenario:** You receive this request:

```
"Add a feature to export user data to CSV"
```

### Your Task

List ALL assumptions AI might make (without asking):

```
1. ________________
2. ________________
3. ________________
4. ________________
5. ________________
```

### Answer Key (Compare Your Answers)

**Common assumptions AI makes (usually wrong):**

1. **Scope:** Export ALL users vs. filtered subset? (privacy implications)
2. **Format:** Users expect specific CSV columns—which ones? (all data, or just name/email?)
3. **File location:** Where to save? User's downloads folder? Server storage?
4. **Headers:** Should CSV have headers? Should they be friendly or database column names?
5. **Date format:** How to format dates? (2026-05-13 or May 13, 2026?)
6. **Permissions:** Can any user export all users? Only admins?
7. **Volume:** Is there a limit on how many users? Pagination?
8. **Encoding:** UTF-8? Should handle special characters like José, 李?

### Why This Matters

Without surfacing these assumptions:
- AI codes with its best guesses
- Code does something unexpected
- Engineers have to rework it

With surfacing assumptions:
- You clarify once upfront
- AI implements correctly
- Done in first try

---

## Exercise 2: Surface Ambiguity

**Scenario:** Request says "Make search faster"

### Your Task

This is ambiguous. List 3 different interpretations (different solutions needed for each):

```
Interpretation 1: ________________
  - Why different? ________________
  - Solution approach: ________________

Interpretation 2: ________________
  - Why different? ________________
  - Solution approach: ________________

Interpretation 3: ________________
  - Why different? ________________
  - Solution approach: ________________
```

### Answer Key (Compare Your Answers)

**"Make search faster" has 3 valid interpretations:**

**Interpretation 1: Response Time (make each search respond quicker)**
- Why different? Focuses on latency of individual searches
- Solution approach: Database indexing, query optimization, caching
- Metric to track: Search takes 500ms → 100ms
- Effort: ~2 hours
- Risk: Low

**Interpretation 2: Throughput (handle more searches at once)**
- Why different? Focuses on concurrent capacity, not individual speed
- Solution approach: Connection pooling, async queries, load balancing
- Metric to track: Handle 100 concurrent → 1000 concurrent
- Effort: ~4 hours
- Risk: Medium

**Interpretation 3: Perceived Speed (feels faster to user)**
- Why different? Not about actual speed, about UX perception
- Solution approach: Show partial results early, progressive loading, debouncing
- Metric to track: Time-to-first-result: 500ms → 100ms
- Effort: ~3 hours
- Risk: High (UI complexity)

### Why This Matters

Different goals need different solutions. If AI picks the wrong one, entire implementation is wasted.

---

## Exercise 3: Ask Clarifying Questions

**Scenario:** Request says:

```
"Add role-based access control to our app"
```

### Your Task

Write 5 clarifying questions you'd ask BEFORE implementation:

```
1. Q: ________________
   Why important: ________________

2. Q: ________________
   Why important: ________________

3. Q: ________________
   Why important: ________________

4. Q: ________________
   Why important: ________________

5. Q: ________________
   Why important: ________________
```

### Answer Key (Compare Your Answers)

**Good clarifying questions to ask:**

1. **Q: How many roles?** (admin, user, guest? or many more?)
   - Why important: Affects data model. 3 roles = simple if/else. 20 roles = needs strategy pattern.

2. **Q: Who assigns roles?** (admin panel? API? database seed?)
   - Why important: Affects implementation. Admin UI vs. backend-only changes approach.

3. **Q: Do role permissions change at runtime?** (or only on app restart?)
   - Why important: Affects caching strategy. Affects performance.

4. **Q: Which endpoints/features need role protection?** (all? specific ones?)
   - Why important: Affects scope. Protects all vs. specific features = different effort.

5. **Q: What should happen when unpermitted access occurs?** (error message? redirect? logs?)
   - Why important: Affects error handling and security logging.

---

## Exercise 4: Write a Clarifying Response

**Scenario:** You're an AI assistant. You receive:

```
"Optimize the database queries"
```

### Your Task

Write what you'd say to the engineer BEFORE implementing:

```
Your response:
___________________________________________________________________

___________________________________________________________________

___________________________________________________________________

___________________________________________________________________
```

### Answer Key (Example Response)

```
Before I optimize, I need clarity:

1. **What's the current problem?**
   - Are queries too slow? (latency issue)
   - Are you running out of database connections? (scalability issue)
   - Is the database using too much memory? (resource issue)
   - Are concurrent queries causing locks? (contention issue)

2. **What's your success metric?**
   - Response time < X ms?
   - Handle X concurrent queries?
   - Use < X GB memory?
   - Achieve X% cache hit rate?

3. **Current baseline:**
   - How long do queries take now?
   - How many concurrent queries now?
   - What data volume are we working with?

4. **Constraints:**
   - Can I add database indexes?
   - Can I add a caching layer (Redis)?
   - Can I change the schema?
   - Must remain backward compatible?

5. **Which queries are slowest?**
   - Have you profiled? (share logs/metrics)

My recommendation: Start with database profiling to identify the slowest query.
Then we'll know exactly what to optimize.

What's your top priority?
```

### Why This Response Works

✓ States what's ambiguous (3 possible meanings of "optimize")  
✓ Asks clarifying questions upfront  
✓ Shows impact (different solutions for different problems)  
✓ Gives specific next step (profile first)  
✓ Waits for clarification before coding  

---

## Exercise 5: Real-World Scenario

**You're reviewing AI-generated code. The request was:**

```
"Add error handling to the payment API"
```

**The AI did:**

```python
# Main change: added try-catch
try:
    process_payment(user_id, amount)
    return {"status": "success"}
except PaymentFailed as e:
    log_error(f"Payment failed: {e}")
    return {"status": "error", "message": str(e)}

# But also (unrelated):
except Exception:  # Catches EVERYTHING (bad practice)
    ...

# And also (unrelated):
except TypeError:  # Can't happen in this code
    ...

# And also (while here, refactored the logging):
def log_error(msg):  # This wasn't the request
    logger.error(f"[API] {msg}")

# And also (reformatted the file):
# File now uses double quotes instead of single quotes
```

### Your Task

**Questions:**

1. Which parts of AI's response align with "Principle #1: Think Before Coding"?

```
Answer: ________________
```

2. Which parts violate it?

```
Answer: ________________
```

3. What clarifying questions should have been asked BEFORE implementation?

```
Question 1: ________________

Question 2: ________________

Question 3: ________________
```

### Answer Key

**1. What aligns with Principle #1?**

✓ Handles the main issue: catches `PaymentFailed` and returns error

**2. What violates it?**

- ✗ Catches `Exception` (too broad—not asked for)
- ✗ Catches `TypeError` (impossible case—not asked for)
- ✗ Refactors logging function (not asked for)
- ✗ Reformats file with double quotes (not asked for)
- ✗ No verification that success criteria met

**3. Clarifying questions that should have been asked:**

- "Should we catch all exceptions, or specific payment errors?"
- "What should we do on error? Log, alert, retry, or just return error message?"
- "Should we include exception details in error message, or hide them for security?"
- "How should we handle network timeouts vs. insufficient funds vs. card declined?"
- "Should this be surgical (error handling only) or can I also refactor logging?"

---

## Exercise 6: Write Your Own Principle #1 Checklist

**Your task:** Based on what you've learned, create your own checklist for "Think Before Coding"

```
□ ________________
□ ________________
□ ________________
□ ________________
□ ________________
□ ________________
□ ________________
□ ________________
```

### Answer Key (Suggested Checklist)

```
□ Assumptions stated explicitly (list what I'm assuming)?
□ Ambiguity surfaced (if unclear, presented multiple interpretations)?
□ Clarifying questions asked (before coding started)?
□ Success criteria clear & verifiable (not vague)?
□ Context provided (relevant code, documentation)?
□ Edge cases considered (unusual inputs, error conditions)?
□ Simpler approaches suggested (if they exist)?
□ Ready to implement? (all questions answered)
```

---

## Exercise 7: Practice in Your Next Task

**This week:**

1. Pick your next AI-assisted coding task
2. Before asking AI to code, go through Principle #1 Checklist:
   - [ ] State assumptions explicitly
   - [ ] Surface any ambiguity
   - [ ] Ask clarifying questions
   - [ ] Define verifiable success criteria

3. Give your prompt to AI
4. Compare results to asking without Principle #1

**Expected outcome:** Fewer iterations to get working code

---

## Self-Reflection Questions

**After completing this worksheet, answer:**

1. **What was your biggest insight about hidden assumptions?**

```
Answer: ________________
```

2. **What's ONE thing you'll do differently next time?**

```
Answer: ________________
```

3. **How will "Principle #1" make your prompts better?**

```
Answer: ________________
```

---

## Next Steps

✓ **Completed this worksheet?** Great! You understand Principle #1.

**Now:**

1. Read [karpathy-principles-guide.md](karpathy-principles-guide.md) Principles #2, #3, #4
2. Get the [quick-reference.md](quick-reference.md) poster
3. Apply all 4 principles to your next AI task
4. Review code using [code-review-checklist.md](../quality-control/code-review-checklist.md)

---

## Answers Summary

| Exercise | Key Takeaway |
|----------|---|
| #1: Hidden Assumptions | Never assume—always list assumptions upfront |
| #2: Surface Ambiguity | Same words, different meanings—present all |
| #3: Clarifying Questions | Ask BEFORE coding, not after |
| #4: Clarifying Response | Show what's ambiguous, present options, ask |
| #5: Real-World Review | Many things violate Principle #1—spot them |
| #6: Checklist | Use this checklist every time |

---

**Last Updated:** May 13, 2026  
**Status:** 🟢 Active Training Exercise
