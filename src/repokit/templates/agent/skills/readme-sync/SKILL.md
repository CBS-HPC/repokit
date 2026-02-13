---
name: readme-sync
description: Regenerate README via repokit and then apply project-specific edits so docs match actual project behavior.
---

# readme-sync

## Skill dependencies
- `activate_project`: resolve configured language/toolchain/VC context before doc sync.

## Pre-checks
- Parse `pyproject.toml` for language/toolchain/version-control configuration to avoid stale instructions.
- Detect code layout and active tooling markers (`src/`, `R/`, `*.do`, `*.m`, `.venv/`, `.conda/`, `.git/`, `.dvc/`, `.datalad/`).
- Ensure README updates reflect configured and detected project reality.

## Workflow
1. Run repokit readme.
2. Post-edit README.md for project-specific accuracy:
   - align terminology with domain and methods
   - remove irrelevant boilerplate
   - ensure command examples are valid in this repo
   - ensure package/tool names match current CLI names
3. Recheck links and anchors.

## Verify
- README.md has no stale command names.
- All edited sections reflect current code and folder layout.
