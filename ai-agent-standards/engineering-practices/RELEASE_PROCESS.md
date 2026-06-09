# Versioning & Release Management

This document defines the standard operating procedures for versioning, branching, and releasing software.

> **When to use this skill:** `@reference` this file when the AI is asked to prepare a release, update versions, or configure Git branching strategies.

---

## 1. Semantic Versioning (SemVer)

All projects **MUST** adhere to [Semantic Versioning 2.0.0](https://semver.org/). Version numbers use the format `MAJOR.MINOR.PATCH`.

- **MAJOR:** Incompatible API changes or massive architectural overhauls.
- **MINOR:** Adding functionality in a backwards-compatible manner.
- **PATCH:** Backwards-compatible bug fixes.

**AI Agent Rule:** When asked to bump a version, the AI must analyze the git diff or changelog to accurately determine if the bump should be Major, Minor, or Patch.

## 2. Git Branching Strategy

Projects should utilize a simplified **GitHub Flow** or structured **Gitflow**, depending on the project size.

### Standard Flow:
1. `main` (or `master`): Always production-ready and deployable.
2. `develop` (optional): Integration branch for features before release.
3. Feature Branches: `feature/[ticket-id]-short-description`
4. Bugfix Branches: `bugfix/[ticket-id]-short-description`
5. Hotfix Branches: `hotfix/[ticket-id]-short-description` (branched from `main`, merged back to `main` and `develop`).

**AI Agent Rule:** Never push directly to `main`. Always propose changes via a Pull Request.

## 3. Pre-Release Checklist

Before any code is merged into `main` or tagged for a release, the following pipeline MUST pass:

- [ ] **Tests Passing:** Unit, Integration, and E2E test suites must show 100% pass rate.
- [ ] **Coverage Met:** Test coverage must remain above the defined threshold (e.g., 80%).
- [ ] **Lint & Format:** Code must pass all strict linting rules.
- [ ] **Security Audit:** SAST tools (e.g., SonarQube, GitHub Advanced Security) report 0 Critical/High vulnerabilities.
- [ ] **Changelog Updated:** `CHANGELOG.md` reflects the changes for this specific version.
- [ ] **Version Bumped:** `package.json`, `pom.xml`, or equivalent configuration files must have the updated SemVer.

## 4. Tagging Releases

Once merged into `main`, the commit **MUST** be tagged with the version number (e.g., `v1.2.3`). Automated deployment pipelines should trigger off these tags.
