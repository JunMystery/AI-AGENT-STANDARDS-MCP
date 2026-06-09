# Rules Generation

Agent instruction files are generated from a small set of shared sources so the framework can update rules without editing every AI configuration file by hand.

## Source Files

- `karpathy/principles.md`: source of truth for the 6 Core Principles.
- `rules/agent-manifest.json`: list of supported agents, labels, output paths, templates, and optional frontmatter.
- `rules/templates/`: wrapper content for each instruction-file format.
- `scripts/generate-rules.py`: renders generated files and checks drift.

Do not edit generated instruction files directly. Edit the source files above, then regenerate.

## Generate

```bash
python scripts/generate-rules.py
```

Generate one agent only:

```bash
python scripts/generate-rules.py --agent codex
```

## Check Drift

```bash
python scripts/generate-rules.py --check
```

The check fails when any generated instruction file differs from the current source output. Run the generator and commit the regenerated files.

## Setup Script Relationship

`scripts/setup.py` reads `rules/agent-manifest.json` to know which instruction files can be installed into another project. It does not generate files during setup; it copies the generated files already committed in this repo and rewrites internal links for the target project.

## Skill Installation

The generator does not modify or move `skills/`, `skills/*/SKILL.md`, or `SKILL-REFERENCE.md`. Generated instruction files must continue to reference `SKILL-REFERENCE.md` and `skills/` so task-specific skill loading keeps working.
