# Cross-Tool Sync Guide: Karpathy Principles

**Keeping AI configurations synchronized across Cursor, Claude, VS Code/Copilot, and other tools**

**Version:** 1.0  
**Last Updated:** May 13, 2026

---

## Problem & Solution

Your team uses multiple AI tools:
- **Cursor** (IDE-integrated development)
- **Claude** (API and web interface)
- **VS Code / GitHub Copilot** (autocomplete and inline suggestions)

**Challenge:** Principles can drift across tools if not kept in sync

**Solution:** This guide establishes a single source of truth and sync process

---

## 🎯 Source of Truth Architecture

```
┌─────────────────────────────────────────────────┐
│  MASTER: principles/karpathy-framework.md       │
│  (Single authoritative source)                  │
└────────────────────┬────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    ┌─────────┐  ┌─────────┐  ┌──────────┐
    │.instructions│Cursor │Claude  │
    │   .md   │ rules   │ prompt │
    │ (Copilot)│ (.mdc)  │ (.md)  │
    └─────────┘  └─────────┘  └──────────┘
    │           │           │
    └───────────┴───────────┘
         Sync Quarterly
```

---

## 📋 Configuration Files & Their Sources

### 1. Master Document (Single Source of Truth)

**File:** `principles/karpathy-framework.md`

**Contains:**
- Principle 1-4 detailed explanations
- Integration with existing framework
- Reviewer checklist
- Success criteria

**Status:** Reference point for all tools  
**Update Frequency:** As needed (major updates only)  
**Last Updated:** May 13, 2026

---

### 2. VS Code / GitHub Copilot

**File:** `.instructions.md` (at project root)

**Source:** Based on `principles/karpathy-framework.md`

**Contains:**
- 4 principles summarized for Copilot
- Specific guidance on Copilot's role
- Project context & standards
- Dos and don'ts
- Self-Check Report format

**When to sync:**
- When core principles change
- Quarterly review (even if no changes)
- When discovering Copilot misapplies principles

**How to sync:**
1. Read `principles/karpathy-framework.md`
2. Check if `.instructions.md` still accurately reflects it
3. If drift detected, update section
4. Test with actual Copilot suggestions

**Validation:** Run a test prompt and verify Copilot applies principles correctly

---

### 3. Cursor IDE

**File:** `.ai-agent-standards/.cursor/rules/karpathy-guidelines.mdc`

**Source:** Based on `principles/karpathy-framework.md`

**Contains:**
- 4 principles for Cursor
- Project context specific to Cursor workflows
- Scenario examples for Cursor usage
- Communication guidelines

**When to sync:**
- When core principles change
- Quarterly review
- When discovering Cursor misapplies principles

**How to sync:**
1. Read `principles/karpathy-framework.md`
2. Compare to `.cursor/rules/karpathy-guidelines.mdc`
3. Check if sections match (principles, examples, guidance)
4. If drift: update Cursor rules to match master
5. Test with sample Cursor tasks

**Validation:** Create test Cursor task, verify it applies principles

**Also manage:** `.cursor/rules/other-rules.mdc` (if you have other custom rules, ensure they don't contradict Karpathy principles)

---

### 4. Claude (API & Web)

**File:** `prompts/claude-system-instructions.md`

**Source:** Based on `principles/karpathy-framework.md`

**Contains:**
- Copy-paste system prompt
- Karpathy principles for Claude
- Workflow context
- Self-Check Report template

**When to sync:**
- When core principles change
- Quarterly review
- When upgrading Claude model versions
- When discovering Claude misapplies principles

**How to sync:**
1. Read `principles/karpathy-framework.md`
2. Update system prompt section in `claude-system-instructions.md`
3. Test: Use updated system prompt with Claude
4. Verify Claude applies principles correctly

**Validation:** 
- Test 3 scenarios (ambiguous request, simplicity check, goal verification)
- Confirm Claude surfaces ambiguity and asks clarifying questions

---

### 5. Existing Project Documentation

**Files to check for consistency:**
- `onboarding/quick-reference.md` — Principles summary
- `quality-control/code-review-checklist.md` — Principle validation checklist
- `quality-control/self-check-report-template.md` — Principle verification sections
- `prompts/HEADER-TEMPLATE.yaml` — Prompt structure

**When to check:**
- Quarterly review
- When updating principles
- When onboarding new team members

**How to check:**
1. Each file should reference the 4 principles
2. Each file should link to `principles/karpathy-framework.md`
3. Terminology should be consistent across files
4. Examples should align

---

## 🔄 Sync Process

### Quarterly Sync (Recommended Cadence)

**When:** Every 3 months (end of Q1, Q2, Q3, Q4)

**Duration:** 30 minutes

**Process:**

1. **Read Master Document** (5 min)
   - Open `principles/karpathy-framework.md`
   - Skim all 4 principles
   - Note any recent clarifications or changes

2. **Check Copilot Config** (5 min)
   - Open `.instructions.md`
   - Compare sections to master doc
   - Look for drift (outdated examples, missing context)
   - [ ] Principles accurate?
   - [ ] Examples current?
   - [ ] Links working?

3. **Check Cursor Rules** (5 min)
   - Open `.ai-agent-standards/.cursor/rules/karpathy-guidelines.mdc`
   - Compare to master doc
   - [ ] Principles match?
   - [ ] Cursor-specific guidance useful?
   - [ ] Scenarios realistic?

4. **Check Claude Instructions** (5 min)
   - Open `prompts/claude-system-instructions.md`
   - Compare system prompt to master doc
   - [ ] Principles accurately translated?
   - [ ] Examples appropriate for Claude?
   - [ ] Self-Check template current?

5. **Check Supporting Docs** (5 min)
   - Spot-check: quick-reference.md, code-review-checklist.md, self-check-report-template.md
   - [ ] Each references principles correctly?
   - [ ] Links to framework doc working?
   - [ ] Terminology consistent?

6. **Make Updates** (if needed)
   - Update any drifting configs
   - Commit changes with message: "Q1 2026 sync: Karpathy principles configs"

7. **Validate** (if changes made)
   - Test Copilot with a sample prompt
   - Test Cursor with a sample file edit
   - Test Claude with system prompt
   - Verify each applies principles

---

### Ad-Hoc Sync (When Needed)

**Trigger:** Team member notices tool isn't applying principles correctly

**Process:**

1. Document what went wrong: "Claude accepted over-engineered code without questioning simplicity"
2. Read relevant principle in `principles/karpathy-framework.md`
3. Check if tool config mentions it: Search for keyword in `.instructions.md` / `.cursor/...` / `claude-system-instructions.md`
4. If not mentioned: Add it
5. If mentioned but unclear: Clarify it
6. Test fix
7. Log in issue tracker: "[Tool] [Principle] - Updated config to prevent [issue]"

---

## 📝 Maintenance Checklist

**Use this checklist for quarterly sync or when making changes:**

### Principles Definitions
- [ ] 4 principle names are consistent everywhere
- [ ] Descriptions are accurate (check against master)
- [ ] Examples are current and relevant
- [ ] Order is consistent (always 1-4 in same order)

### Project Context
- [ ] Framework name (AI-Coding-Standards) consistent
- [ ] Governance model clearly explained
- [ ] Links to framework documentation working
- [ ] Project standards (80% test coverage, no secrets, etc.) mentioned

### Tool-Specific Guidance
- [ ] Copilot config (.instructions.md): Talks about auto-complete, inline suggestions
- [ ] Cursor config (.cursor/rules): Talks about IDE integration, project tree access
- [ ] Claude config (claude-system-instructions.md): Talks about API usage, chat interface

### Examples
- [ ] Each tool has relevant examples (not generic)
- [ ] Examples show "wrong vs. right" approach
- [ ] Examples are realistic and relatable

### Self-Check Templates
- [ ] Principles verified in Self-Check Report
- [ ] All 4 principles have checkboxes
- [ ] Checklist matches code-review-checklist.md

### Links & References
- [ ] All internal links work (test by opening them)
- [ ] Links to supporting docs updated
- [ ] References to other frameworks are current

### Training Materials
- [ ] karpathy-principles-guide.md current
- [ ] think-before-coding-worksheet.md exercises still valid
- [ ] quick-reference.md reflects latest principles

---

## 🚨 Common Drift Scenarios & Fixes

### Scenario 1: Master Doc Changes, Tool Configs Lag

**Symptom:** "Principle #2 now includes 'don't over-abstract', but Copilot config still says abstractions OK"

**Fix:**
1. Update `.instructions.md` to mention abstraction rule
2. Update `.cursor/rules/karpathy-guidelines.mdc` similarly
3. Update `claude-system-instructions.md` system prompt
4. Test with sample code to confirm all tools now check for over-abstraction

---

### Scenario 2: Tool Acts Against Principles

**Symptom:** "Claude generated 300-line strategy pattern for simple problem (violates Simplicity)"

**Cause:** System prompt doesn't emphasize simplicity strongly enough

**Fix:**
1. Check `prompts/claude-system-instructions.md`
2. Look for "Simplicity" section
3. Make it more prominent or clear
4. Test with similar problem: does Claude now simplify?

---

### Scenario 3: Tool-Specific Misalignment

**Symptom:** "Cursor applies all 4 principles beautifully, but Copilot seems to skip #3 (Surgical Changes)"

**Cause:** `.instructions.md` might not emphasize surgical changes in Copilot context

**Fix:**
1. Open `.instructions.md`
2. Find Principle #3 section
3. Add specific Copilot context: "When suggesting inline edits, only change the line requested, not surrounding code"
4. Add example specific to Copilot's inline mode
5. Test Copilot with a request to modify one line—verify it only changes that line

---

## 🔗 Sync Dependencies

**Tool configurations depend on master doc in this order:**

```
1. principles/karpathy-framework.md (PRIMARY)
   ├─ .instructions.md (Copilot)
   ├─ .cursor/rules/karpathy-guidelines.mdc (Cursor)
   ├─ prompts/claude-system-instructions.md (Claude)
   └─ Supporting docs:
      ├─ onboarding/quick-reference.md
      ├─ onboarding/karpathy-principles-guide.md
      ├─ quality-control/code-review-checklist.md
      └─ quality-control/self-check-report-template.md
```

**Update order (for major changes):**
1. Update `principles/karpathy-framework.md` (master)
2. Update tool configs (.instructions.md, .cursor/rules, claude-system-instructions.md)
3. Update supporting docs
4. Test each tool
5. Commit all changes together

---

## 📊 Sync Log Template

**Track sync activities:**

```markdown
## Karpathy Principles Sync Log

### Q1 2026 Sync
- **Date:** May 13, 2026
- **Duration:** 30 min
- **Changes Made:**
  - [ ] principles/karpathy-framework.md reviewed (no changes needed)
  - [ ] .instructions.md updated (added Principle #2 example)
  - [ ] .cursor/rules/karpathy-guidelines.mdc - no changes
  - [ ] claude-system-instructions.md - clarified system prompt
  - [ ] Supporting docs reviewed and cross-checked
  
- **Tests Performed:**
  - [ ] Copilot: Tested with ambiguous request → surfaced assumptions ✓
  - [ ] Cursor: Tested with edit task → only changed requested lines ✓
  - [ ] Claude: Tested with vague task → asked clarifying questions ✓

- **Issues Found:** None

- **Issues Fixed:** None

---

### Q2 2026 Sync
- **Date:** [Date]
- **Duration:** [Duration]
- **Changes Made:**
  - [ ] ...
  
- **Tests Performed:**
  - [ ] ...

- **Issues Found:**
  - Issue 1: [Description]
  - Issue 2: [Description]

- **Issues Fixed:**
  - Fix 1: [What was updated]
  - Fix 2: [What was updated]
```

---

## 🎯 Success Criteria

**Sync is successful when:**

1. ✓ All 4 principles accurately reflected in all tool configs
2. ✓ No contradictions between tools
3. ✓ Each tool correctly applies principles when tested
4. ✓ Team members report consistency across tools
5. ✓ Code review shows principles being validated
6. ✓ No "principle drift" detected for 3+ months

---

## Questions & Support

**Q: What if a tool can't express a principle clearly?**  
A: That's OK—focus on what the tool CAN do. E.g., GitHub Copilot's limitations mean it can't always ask clarifying questions, so emphasize that in `instructions.md`.

**Q: How often should I actually sync?**  
A: Minimally quarterly. More frequently if: (a) principles change, (b) team discovers misalignment, (c) new tools added.

**Q: What if I disagree with a principle?**  
A: Raise it with the team. Discuss. If consensus changes, update `principles/karpathy-framework.md` FIRST, then sync all tools.

**Q: Can I have tool-specific variations of principles?**  
A: Minor emphasis variations are OK (e.g., Cursor emphasizes "surgical changes" more because it edits code directly). But the 4 core principles must be consistent.

---

## Related Documents

- [Karpathy Framework](../principles/karpathy-framework.md) — Master doc
- [VS Code Instructions](./.instructions.md) — Copilot config
- [Cursor Rules](./.cursor/rules/karpathy-guidelines.mdc) — Cursor config
- [Claude Instructions](../prompts/claude-system-instructions.md) — Claude config
- [Code Review Checklist](../quality-control/code-review-checklist.md) — Principle validation

---

**Last Updated:** May 13, 2026  
**Status:** 🟢 Active
