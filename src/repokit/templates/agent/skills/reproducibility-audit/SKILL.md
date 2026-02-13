---
name: reproducibility-audit
description: Audit project reproducibility by checking environment, dependencies, provenance, and a small end-to-end run.
---

# reproducibility-audit

## Skill dependencies
- `activate_project`: resolve runtime/toolchain/VC mode before audits.
- `project-hygiene`: source of truth for language-appropriate check execution.
- `dmp-governance`: source of truth for dataset and DMP consistency checks.

## Pre-checks
- Parse `pyproject.toml` for dependencies, language/runtime settings, and policy blocks used for reproducibility.
- Detect active environment and VC markers (`.venv/`, `.conda/`, `uv.lock`, `environment.yml`, `renv.lock`, `.git/`, `.dvc/`, `.datalad/`).
- Choose minimal-run commands that match the detected/configured stack.

## Workflow
1. Verify dependency files are synchronized.
2. Verify DMP and dataset metadata are current.
3. Run a minimal pipeline/test command from a clean environment.
4. Record provenance details (versions, parameters, output paths).

## Verify
- Another user can reproduce a minimal run using documented steps.
- No hidden local assumptions remain in scripts or docs.
