---
name: vc-governance
description: Apply version-control best practices for git, dvc, or datalad workflows used by research-template projects.
---

# vc-governance

## Skill dependencies
- `activate_project`: resolve configured VC mode and repository markers first.

## Pre-checks
- Parse `pyproject.toml` for selected version-control mode.
- Detect VC markers: `.git/`, `.dvc/`, `.datalad/`.
- If VC mode is none, do not run git/DVC/Datalad commands unless explicitly requested.
- If config and markers conflict, prefer configured mode and report mismatch.

## Git mode
- Use focused branches and small commits.
- Keep CI green before merge.

## DVC mode
- Ensure data/artifacts are tracked with DVC, not Git.
- Validate dvc.yaml and lock consistency after changes.

## Datalad mode
- Ensure dataset saves are explicit and provenance-preserving.
- Validate siblings/remotes and dataset state.

## Verify
- git status clean after intended commits.
- Data pointers/remotes are consistent for selected mode.
