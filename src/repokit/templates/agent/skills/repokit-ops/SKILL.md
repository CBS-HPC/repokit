---
name: repokit-ops
description: Run core repokit CLI workflows with verification steps for dependencies, README sync, templates, and CI toggles.
---

# repokit-ops

## Use when
- You need to run repokit commands as part of project maintenance.
- You want consistent command order and post-run checks.

## Skill dependencies
- `activate_project`: resolve project profile before running repokit workflows.
- `readme-sync`: source of truth for README regeneration and post-edit checks.
- `ci-governance`: source of truth for CI provider detection and CI command composition.

## Automation safety
- Prefer non-interactive command execution paths.
- If a repokit subcommand opens an interactive prompt/wizard, stop and request explicit human guidance.
- Do not assume defaults for interactive choices in autonomous runs.

## Pre-checks
- Parse `pyproject.toml` for language/toolchain/version-control and enabled workflows.
- Detect markers that affect command choice (`.git/`, `.dvc/`, `.datalad/`, `.venv/`, `.conda/`, `uv.lock`, `environment.yml`, `renv.lock`).
- Skip workflows disabled by config (for example CI when VC mode is none), unless explicitly requested.

## Workflow
1. Run dependency sync:
   - repokit deps
2. Regenerate README:
   - repokit readme
3. Refresh templates/examples when requested:
   - repokit templates
   - repokit ex-code
   - repokit tests
4. Manage CI when requested:
   - repokit ci --on or repokit ci --off

## Verify
- git status --short reflects expected file changes only.
- Generated files are still valid (README.md, env files, template outputs).

