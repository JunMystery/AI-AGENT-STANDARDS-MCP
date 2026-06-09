# Karpathy Principles — Real-World Examples

Real-world code examples demonstrating the four principles. Each example shows what LLMs commonly do wrong and how to fix it.

> **Reference:** These examples complement [principles.md](./principles.md) — the source of truth for all 4 principles.

---

## 1. Think Before Coding

### Example 1: Hidden Assumptions

**User Request:** "Add a feature to export user data"

**❌ What LLMs Do (Wrong Assumptions)**

```python
def export_users(format='json'):
    """Export all users to a file."""
    users = User.query.all()
    
    if format == 'json':
        with open('users.json', 'w') as f:
            json.dump([u.to_dict() for u in users], f)
    elif format == 'csv':
        with open('users.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'email', 'name'])
            writer.writeheader()
            writer.writerows([u.to_dict() for u in users])
    
    return f"Exported {len(users)} users"
```

**Problems:**
- Assumed it should export ALL users (what about pagination? privacy?)
- Assumed file location without asking
- Assumed which fields to include
- Assumed CSV fieldnames without checking actual data structure

**✅ What Should Happen (Surface Assumptions)**

```
Before implementing, I need to clarify:

1. **Scope**: Export all users or filtered subset? (privacy implications)
2. **Format**: You mentioned "export" - did you mean:
   - Download file in browser?
   - Background job with email notification?
   - API endpoint returning data?
3. **Fields**: Which user fields? (some might be sensitive)
4. **Volume**: How many users typically? (affects approach)

Simplest approach: Add an API endpoint that returns paginated JSON.
Would need more info for file-based exports.

What's your preference?
```

### Example 2: Multiple Interpretations

**User Request:** "Make the search faster"

**❌ What LLMs Do (Pick Silently)**

```python
# Adds caching, database indexes, and async processing
# without asking which "faster" matters
@lru_cache(maxsize=1000)
async def search(query: str) -> List[Result]:
    # ... 200 lines of optimization code
```

**✅ What Should Happen**

```
"Make the search faster" could mean:

1. **Faster response time** (< 100ms instead of 500ms)
   - Add database indexes
   - Cache frequent queries
   - Estimated effort: 2 hours

2. **Handle more concurrent searches** (throughput)
   - Add async/await
   - Connection pooling
   - Estimated effort: 4 hours

3. **Faster perceived speed** (UX)
   - Show partial results immediately
   - Progressive loading
   - Estimated effort: 3 hours

Current search takes ~500ms for typical queries. 
Which aspect matters most for your use case?
```

---

## 2. Simplicity First

### Example 1: Over-abstraction

**User Request:** "Add a function to calculate discount"

**❌ What LLMs Do (Overengineered)**

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Protocol, Union
from dataclasses import dataclass

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float:
        pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def calculate(self, amount: float) -> float:
        return amount * (self.percentage / 100)

class FixedDiscount(DiscountStrategy):
    def __init__(self, fixed_amount: float):
        self.fixed_amount = fixed_amount
    
    def calculate(self, amount: float) -> float:
        return min(self.fixed_amount, amount)

@dataclass
class DiscountConfig:
    strategy: DiscountStrategy
    min_purchase: float = 0.0
    max_discount: float = float('inf')

class DiscountCalculator:
    def __init__(self, config: DiscountConfig):
        self.config = config
    
    def apply_discount(self, amount: float) -> float:
        if amount < self.config.min_purchase:
            return 0
        discount = self.config.strategy.calculate(amount)
        return min(discount, self.config.max_discount)

# Usage requires 30+ lines of setup for a simple calculation
```

**✅ What Should Happen (Simple)**

```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate discount amount. percent should be 0-100."""
    return amount * (percent / 100)

# Usage
discount = calculate_discount(100.0, 10.0)  # $10 off
```

**When to add complexity:** Only when you actually need multiple discount types. If that requirement comes later, refactor then.

### Example 2: Speculative Features

**User Request:** "Save user preferences to database"

**❌ What LLMs Do (Unnecessary Features)**

```python
class PreferenceManager:
    def __init__(self, db, cache=None, validator=None):
        self.db = db
        self.cache = cache or InMemoryCache()
        self.validator = validator or DefaultValidator()
    
    def save(self, user_id: int, prefs: dict, 
             merge: bool = True, 
             validate: bool = True,
             notify: bool = False) -> bool:
        """Save preferences with optional merging, validation, and notifications."""
        # ... 40+ lines for features nobody asked for
```

**✅ What Should Happen (Just What Was Asked)**

```python
def save_preferences(db, user_id: int, preferences: dict):
    """Save user preferences to database."""
    db.execute(
        "UPDATE users SET preferences = ? WHERE id = ?",
        (json.dumps(preferences), user_id)
    )
```

**Add later if needed:** Caching (when performance matters), validation (when bad data appears), merging (when requirement emerges).

---

## 3. Surgical Changes

### Example 1: Drive-by Refactoring

**User Request:** "Fix the bug where empty emails crash the validator"

**❌ What LLMs Do (Too Much)**

```diff
  def validate_user(user_data):
-     # Check email format
-     if not user_data.get('email'):
+     """Validate user data."""
+     email = user_data.get('email', '').strip()
+     
+     # Validate email
+     if not email:
          raise ValueError("Email required")
-     
-     # Basic email validation
-     if '@' not in user_data['email']:
+     if '@' not in email or '.' not in email.split('@')[1]:
          raise ValueError("Invalid email")
      
-     # Check username
-     if not user_data.get('username'):
+     # Validate username
+     username = user_data.get('username', '').strip()
+     if not username:
          raise ValueError("Username required")
+     if len(username) < 3:
+         raise ValueError("Username too short")
+     if not username.isalnum():
+         raise ValueError("Username must be alphanumeric")
      
      return True
```

**Problems:** "Improved" email validation beyond the bug fix, added username validation nobody asked for, changed comments, added docstring.

**✅ What Should Happen (Surgical)**

```diff
  def validate_user(user_data):
      # Check email format
-     if not user_data.get('email'):
+     email = user_data.get('email', '')
+     if not email or not email.strip():
          raise ValueError("Email required")
      
      # Basic email validation
-     if '@' not in user_data['email']:
+     if '@' not in email:
          raise ValueError("Invalid email")
      
      # Check username
      if not user_data.get('username'):
          raise ValueError("Username required")
      
      return True
```

**Only changed:** The specific lines that fix empty email handling.

### Example 2: Style Drift

**User Request:** "Add logging to the upload function"

**❌ What LLMs Do:** Changed quote style, added type hints, added docstring, reformatted whitespace, changed boolean return logic.

**✅ What Should Happen:** Match existing style — single quotes, no type hints, same boolean pattern, same spacing. Only add `logger.info/error/exception` calls.

---

## 4. Goal-Driven Execution

### Example 1: Vague vs. Verifiable

**User Request:** "Fix the authentication system"

**❌ What LLMs Do (Vague Approach)**

```
I'll fix the authentication system by:
1. Reviewing the code
2. Identifying issues
3. Making improvements
4. Testing the changes

[Proceeds to make changes without clear success criteria]
```

**✅ What Should Happen (Verifiable Goals)**

```
To "fix authentication," I need to define success criteria. 
What specific issue are we solving?

If the issue is "users stay logged in after password change":

Plan:
1. Write test: Change password → verify old session invalidated
   Verify: Test fails (reproduces bug)

2. Implement: Invalidate sessions on password change
   Verify: Test passes

3. Check edge cases: Multiple active sessions, concurrent changes
   Verify: Additional tests pass

4. Verify no regression: Existing auth tests still pass
   Verify: Full test suite green

What's the specific auth issue you're seeing?
```

### Example 2: Multi-Step with Verification

**User Request:** "Add rate limiting to the API"

**❌ What LLMs Do:** Implement full rate limiting with Redis, multiple strategies, configuration system, and monitoring in one 300-line commit with no verification steps.

**✅ What Should Happen (Incremental with Verification)**

```
Plan for rate limiting:

1. Add basic in-memory rate limiting (single endpoint)
   Verify: Test: 100 requests → first 10 succeed, rest get 429

2. Extract to middleware (apply to all endpoints)
   Verify: Rate limits apply to /users and /posts

3. Add Redis backend (for multi-server)
   Verify: Rate limit persists across app restarts

4. Add configuration (rates per endpoint)
   Verify: /search allows 10/min, /users allows 100/min

Each step is independently verifiable and deployable.
Start with step 1?
```

---

## 5. DRY & Reusability

### Example 1: UI Design System

**User Request:** "Add a submit button to the form"

**❌ What LLMs Do (Hardcoding Styles)**

```html
<button style="background-color: #E53935; color: white; padding: 10px 20px; border-radius: 4px; border: none; font-weight: bold;">
    Submit
</button>
```

**✅ What Should Happen (Reusability)**

```html
<!-- Assuming the project uses a UI library or shared CSS -->
<Button variant="primary">Submit</Button>
<!-- OR -->
<button class="btn btn-primary">Submit</button>
```

### Example 2: Logic Duplication

**User Request:** "Format the price on the cart page"

**❌ What LLMs Do (Repeating Logic)**

```javascript
// Writing the same formatting logic for the 5th time in the project
const formattedPrice = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
}).format(cart.total);
```

**✅ What Should Happen (Reusability)**

```javascript
// Using an existing shared function, or creating one in a shared utils directory
import { formatCurrency } from '@/utils/currency';

const formattedPrice = formatCurrency(cart.total);
```

### Example 3: Configuration & Types Duplication

**User Request:** "Create a service to call the shipping API and define the response structure"

**❌ What LLMs Do (Duplicating Types & Env Configuration)**

```typescript
// Duplicating API types and hardcoding config values locally
const API_URL = "https://api.shipping-provider.com/v1"; // Hardcoded config

interface ShippingResponse {
  id: string;
  trackingNumber: string;
  status: string;
  estimatedDelivery: string;
}
```

**✅ What Should Happen (Reusability)**

```typescript
// Importing shared configurations and extending shared type declarations
import { config } from '@/config'; // Central config
import { BaseApiResponse } from '@/types/api.types';

// Reusing base types instead of duplicating fields
interface ShippingResponse extends BaseApiResponse {
  trackingNumber: string;
  estimatedDelivery: string;
}
```

---

## 6. Code Organization

### Example 1: Avoiding Monolithic Files

**User Request:** "Implement user registration, validation, and email notification"

**❌ What LLMs Do (Monolithic File)**
Add the validation rules, the database query, and the SMTP setup directly in the user registration endpoint controller in `auth.controller.js`. The file grows to 450 lines of mixed concerns.

**✅ What Should Happen (File Splitting)**
Separate the logic into dedicated modules/files:
1. `validators/register.schema.js` (Schema definition for validation)
2. `services/user.service.js` (Core registration business and DB logic)
3. `helpers/email.utils.js` (Helper function to send emails)
4. `auth.controller.js` (Controller coordinates validators, services, helpers, and returns HTTP response)

### Example 2: Suffix Naming & General Files

**User Request:** "Add calculation helper functions for taxes and shipping fees"

**❌ What LLMs Do (Ad-hoc naming)**
Create a file named `taxCalculate.js` and another named `shippingFee.js` containing single-line helper functions, scattered in random folders.

**✅ What Should Happen (General Files and Suffixes)**
Group related utilities in a general helper file:
`src/helpers/finance.helper.js` containing both `calculateTax()` and `calculateShippingFee()`.

---

## Anti-Patterns Summary

| Principle | Anti-Pattern | Fix |
|-----------|-------------|-----|
| Think Before Coding | Silently assumes file format, fields, scope | List assumptions explicitly, ask for clarification |
| Simplicity First | Strategy pattern for single discount calculation | One function until complexity is actually needed |
| Surgical Changes | Reformats quotes, adds type hints while fixing bug | Only change lines that fix the reported issue |
| Goal-Driven | "I'll review and improve the code" | "Write test for bug X → make it pass → verify no regressions" |
| DRY & Reusability | Hardcoding inline styles, duplicating logic, types, or config | Use existing design system, shared configs, utilities, and base types |
| Code Organization | Massive 500+ LOC files with mixed concerns, ad-hoc filenames | Split into dedicated files (<300 LOC), use standard suffix suffixes |

## Key Insight

The "overcomplicated" examples aren't obviously wrong — they follow design patterns and best practices. The problem is **timing**: they add complexity before it's needed, which makes code harder to understand, introduces more bugs, takes longer to implement, and is harder to test.

**Good code is code that solves today's problem simply, not tomorrow's problem prematurely.**
