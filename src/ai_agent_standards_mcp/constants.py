"""Static catalog configuration."""

TEXT_SUFFIXES = {".md", ".mdc", ".txt", ".yaml", ".yml", ".json"}
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "node_modules"}
DEFAULT_INCLUDE_DIRS = ("karpathy", "ai-agent-standards", "skills", "docs")

TASK_ANCHORS = {
    "security": (
        "ai-agent-standards/risk-management/security-constraints.md",
        "skills/security-review/SKILL.md",
    ),
    "api": (
        "skills/api-design/SKILL.md",
        "ai-agent-standards/prompts/sample-use-cases/create-api-with-rate-limiting.md",
    ),
    "tests": (
        "ai-agent-standards/engineering-practices/TESTING_STANDARDS.md",
        "skills/tdd-workflow/SKILL.md",
    ),
    "docs": (
        "ai-agent-standards/engineering-practices/DOCUMENTATION_STANDARDS.md",
        "skills/documentation-lookup/SKILL.md",
    ),
    "accessibility": (
        "ai-agent-standards/compliance/A11Y_CHECKLIST.md",
        "skills/accessibility/SKILL.md",
    ),
    "performance": (
        "ai-agent-standards/engineering-practices/NON_FUNCTIONAL_REQUIREMENTS.md",
        "skills/production-audit/SKILL.md",
    ),
    "release": (
        "ai-agent-standards/engineering-practices/RELEASE_PROCESS.md",
        "skills/git-workflow/SKILL.md",
    ),
    "skills": (
        "SKILL-REFERENCE.md",
        "skills/skill-scout/SKILL.md",
    ),
    "review": (
        "ai-agent-standards/quality-control/code-review-checklist.md",
        "ai-agent-standards/quality-control/audit-ai-code-full.md",
    ),
}
