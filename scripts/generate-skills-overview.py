#!/usr/bin/env python3
import os
import re
from pathlib import Path

def parse_skill_file(skill_path: Path):
    try:
        content = skill_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {skill_path}: {e}")
        return None

    # Try to parse frontmatter
    name = skill_path.parent.name
    description = ""
    when_to_use = []

    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    body = content
    if frontmatter_match:
        frontmatter_text = frontmatter_match.group(1)
        body = content[frontmatter_match.end():]
        # Simple parser for frontmatter
        for line in frontmatter_text.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().lower()
                val = val.strip().strip('"').strip("'")
                if key == "name":
                    name = val
                elif key == "description":
                    description = val

    # If description is empty or very short, try to extract first paragraph of body
    if not description:
        # Strip header from body
        body_no_header = re.sub(r"^#.*?\n", "", body, flags=re.IGNORECASE).strip()
        paragraphs = [p.strip() for p in body_no_header.split("\n\n") if p.strip()]
        if paragraphs:
            # clean up md format
            description = re.sub(r"\[.*?\]\(.*?\)", "", paragraphs[0])
            description = description.replace("\n", " ").strip()

    # Search for "When to Use" or "When to use"
    when_to_use_match = re.search(r"##\s*When\s+to\s+Use\s*\n(.*?)(?=\n##|$)", content, re.IGNORECASE | re.DOTALL)
    if when_to_use_match:
        lines = when_to_use_match.group(1).strip().splitlines()
        for line in lines:
            line_str = line.strip()
            if line_str.startswith("-") or line_str.startswith("*"):
                # Clean up bullet list item
                item = line_str.lstrip("-* ").strip()
                if item:
                    when_to_use.append(item)
            elif line_str and not line_str.startswith("#"):
                # Clean up non-empty lines that aren't headers
                item = line_str
                when_to_use.append(item)

    return {
        "id": skill_path.parent.name,
        "name": name,
        "description": description,
        "when_to_use": when_to_use[:4] # limit to top 4 use cases for brief overview
    }

def main():
    repo_root = Path(__file__).resolve().parents[1]
    skills_dir = repo_root / "skills"
    docs_dir = repo_root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    skills = []
    for skill_folder in sorted(skills_dir.iterdir()):
        if skill_folder.is_dir():
            skill_md = skill_folder / "SKILL.md"
            if skill_md.is_file():
                parsed = parse_skill_file(skill_md)
                if parsed:
                    skills.append(parsed)

    # Generate SKILLS_OVERVIEW.md
    output_path = docs_dir / "SKILLS_OVERVIEW.md"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Skills Overview\n\n")
        f.write(f"This document provides a comprehensive directory of the **{len(skills)}** local skills packaged with the Agent Guidance MCP Server.\n\n")
        
        f.write("| Skill / Tool Name | Description | When to Use |\n")
        f.write("| :--- | :--- | :--- |\n")
        
        for s in skills:
            name_link = f"[`{s['name']}`](../skills/{s['id']}/SKILL.md)"
            desc = s['description'].replace("|", "\\|")
            if len(desc) > 180:
                desc = desc[:177] + "..."
            
            use_cases = " / ".join(s['when_to_use'])
            if len(use_cases) > 180:
                use_cases = use_cases[:177] + "..."
            if not use_cases:
                use_cases = "General workflow enhancement."
                
            f.write(f"| {name_link} | {desc} | {use_cases} |\n")
            
    print(f"Successfully generated {output_path} with {len(skills)} skills.")

if __name__ == "__main__":
    main()
