---
name: git-workflow
description: Git collaboration workflow for branches, commits, PRs, reviews, releases, tags, and conflict handling. Use when preparing changes for review, planning branch strategy, writing commit or PR text, or managing release flow.
origin: ECC
---

# Git Workflow

Use this skill when the task involves collaboration through version control.

## What to Apply

- Keep branches short-lived and tied to one intent.
- Write commits and PR descriptions around user-visible or maintainer-visible changes.
- Review diffs before handoff and call out unrelated dirty worktree changes.
- Prefer non-destructive recovery steps unless the user explicitly approves otherwise.
- Align release tags, changelogs, and version bumps with the repo release process.

## Reference Files

- [ai-agent-standards/engineering-practices/RELEASE_PROCESS.md](../../ai-agent-standards/engineering-practices/RELEASE_PROCESS.md)
- [ai-agent-standards/quality-control/ci-cd-gates.md](../../ai-agent-standards/quality-control/ci-cd-gates.md)
- [.github/pull_request_template.md](../../.github/pull_request_template.md)

## Output Expectation

Provide branch, commit, PR, or release guidance with the exact verification status.
