---
name: database-migrations
description: Database migration planning and review workflow. Use when creating, altering, renaming, backfilling, indexing, or deleting database schema or data, especially when zero-downtime, rollback, large tables, or production safety matters.
origin: ECC
---

# Database Migrations

Use this skill when database structure or persisted data changes.

## What to Apply

- Separate schema changes from data backfills when risk or scale is meaningful.
- Prefer expand-contract migrations for renames, type changes, and destructive changes.
- Check locks, large-table behavior, default values, indexes, and rollback strategy.
- Treat deployed migrations as immutable.
- Require tests or dry runs that match the project migration tooling.

## Reference Files

- [ai-agent-standards/prompts/sample-use-cases/database-migration.md](../../ai-agent-standards/prompts/sample-use-cases/database-migration.md)
- [ai-agent-standards/engineering-practices/TESTING_STANDARDS.md](../../ai-agent-standards/engineering-practices/TESTING_STANDARDS.md)
- [ai-agent-standards/risk-management/escalation-workflow.md](../../ai-agent-standards/risk-management/escalation-workflow.md)

## Output Expectation

State the migration sequence, rollback or forward-fix plan, and verification steps before touching production data.
