# Documentation Standards

This document defines the mandatory documentation standards for all projects using the AI-Coding-Standards framework.

> **When to use this skill:** `@reference` this file when the AI is asked to generate project documentation, `README.md`, `CHANGELOG.md`, or API specs.

---

## 1. README.md Requirements

Every project repository **MUST** contain a root `README.md` with the following minimum structure:

1. **Title & Description:** Clear, 1-2 sentence explanation of what the project does.
2. **Prerequisites:** Required language versions (e.g., Node.js v20+), databases, or global tools.
3. **Quick Start (Installation & Run):** Exact copy-pasteable commands to get the project running locally within 5 minutes.
4. **Environment Variables:** List of required `.env` variables. DO NOT include actual secrets. Provide an `.env.example`.
5. **Project Structure:** A brief tree of the `src/` directory.
6. **Architecture/Stack:** Brief list of core technologies used.

## 2. Changelog Standards

We strictly adhere to the [Keep a Changelog](https://keepachangelog.com/) standard.

- File name **MUST** be `CHANGELOG.md` at the repository root.
- Versions must use Semantic Versioning (see `RELEASE_PROCESS.md`).
- Entries must be grouped by: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

**Example:**
```markdown
## [1.2.0] - 2026-05-15
### Added
- New authentication flow using OAuth2.
### Fixed
- Memory leak in the data processing worker.
```

## 3. Code Documentation (Docstrings)

Self-documenting code is preferred over excessive comments. However, public APIs, shared utilities, and complex algorithms **MUST** have docstrings.

- **TypeScript/JavaScript:** Use standard `JSDoc` tags (`@param`, `@returns`, `@throws`).
- **Python:** Use `Sphinx` or `Google` style docstrings.
- **Rule:** Never write a comment explaining *what* the code does (the code should show that). Write comments explaining *why* a specific approach was taken.

## 4. API Documentation

All RESTful or GraphQL APIs exposed to frontend applications or third parties **MUST** be documented.

- **Standard:** Use OpenAPI 3.0 (Swagger) for REST APIs.
- **Location:** Keep API documentation as close to the code as possible (e.g., using Swagger annotations in controllers).
- **Minimum Requirements:** Every endpoint must document its request payload, response schema, and possible HTTP error codes (400, 401, 403, 404, 500).
