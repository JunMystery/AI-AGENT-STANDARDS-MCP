# Compliance & Industry Standards Alignment

This framework is designed to generate code that inherently aligns with major industry standards for security, reliability, and risk management. 

> **When to use this skill:** `@reference` this file when auditing the system architecture, evaluating security risks, or preparing for compliance certification.

---

## 1. OWASP Top 10 for LLM Applications

We map our framework controls directly to the [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

| OWASP Risk | Framework Mitigation |
|------------|----------------------|
| **LLM01: Prompt Injection** | Addressed via strict input validation mandates in `security-constraints.md`. |
| **LLM02: Insecure Output Handling** | Handled by enforcing XSS protection and strict sanitization rules in the Reviewer Agent. |
| **LLM03: Training Data Poisoning** | We do not train models on dynamic user data. Architecture rules forbid modifying production databases via AI. |
| **LLM04: Model Denial of Service** | Mitigated via `NON_FUNCTIONAL_REQUIREMENTS.md` enforcing Rate Limiting and Caching strategies. |
| **LLM06: Sensitive Information Disclosure** | Addressed by the "No Hardcoded Secrets" zero-trust constraint. |
| **LLM07: Insecure Plugin Design** | Enforced via strict API validation and schema checks in `TESTING_STANDARDS.md`. |
| **LLM08: Excessive Agency** | Prevented by the Multi-Agent architecture (Coder agent cannot run arbitrary prod commands; Human is the final gate). |

## 2. NIST AI Risk Management Framework (AI RMF)

The US National Institute of Standards and Technology (NIST) provides a framework to manage AI risks. Our workflow aligns with the four core functions:

- **GOVERN:** We govern AI behavior through the 6 Core Principles and strict Role-Playing Agents (Coder vs. Reviewer).
- **MAP:** Risks are mapped in the `security-constraints.md` and flagged during the PR checklist.
- **MEASURE:** We measure AI effectiveness using the `Self-Check Report` and track iterations and defect escape rates.
- **MANAGE:** We manage risks by enforcing a Human-in-the-Loop (HITL) gate before any code is merged into `main`.

## 3. CISA Guidelines for Secure Software Development

The Cybersecurity and Infrastructure Security Agency (CISA) promotes "Secure by Design." This repo complies by:

- Using default-deny architectural patterns.
- Enforcing strict test coverage and SAST scanning (`.github/workflows/ai-code-audit.yml`).
- Mandating a structured release process with Semantic Versioning (`RELEASE_PROCESS.md`).
