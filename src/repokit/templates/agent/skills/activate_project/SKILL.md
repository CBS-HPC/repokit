---
name: activate_project
description: Initialize project execution context by reading README and pyproject.toml, detecting language/toolchain/version-control markers, and selecting the correct environment before any task.
---

# activate_project

## Use when
- Starting a new task/session.
- Switching to a different project/repo.
- Any time language, toolchain, or version-control mode is unclear.

## Data access bootstrap (first step)
- Run `python skills/activate_project/scripts/ensure_data_access_policy.py` before broad file reads.
- Behavior:
  - If `[tool.data_policy]` is missing in `pyproject.toml`, prompt user to select sensitive/proprietary top-level directories and write policy.
  - Sync selected sensitive paths to `.codexignore`, `.claudeignore`, and `.cursorignore`.
  - On later runs, ask whether existing policy is still correct; if not, reconfigure and rewrite.
  - Apply this consistently for Codex/Claude/Cursor agent setups (`.codex`, `.claude`, `.cursor`).
- Do not continue with normal project activation until this step is completed.

## Pre-checks
- Parse `pyproject.toml` for language, environment manager, and version-control settings.
- Read `README` for project intent and workflow notes.
- Detect repo markers: `.git/`, `.dvc/`, `.datalad/`, `.venv/`, `.conda/`, `uv.lock`, `environment.yml`, `renv.lock`, `DESCRIPTION`.
- Detect code layout and file types: `src/`, `tests/`, `R/`, `inst/`, `*.py`, `*.R`, `*.Rmd`, `*.do`, `*.m`.

## Workflow
1. Run data access bootstrap script and enforce resulting access policy.
2. Build an execution profile from config + detected code/markers.
3. Select runtime/toolchain from the profile:
   - Python: `uv`/`.venv` or conda/`.conda` based on config and markers.
   - R: `renv`/`Rscript` when R markers are present.
   - Stata/MATLAB: project scripts/tooling for `.do`/`.m`.
4. Select VC mode from config + markers:
   - Git if `.git/` exists and VC mode is git.
   - DVC if `.dvc/` exists and VC mode is dvc.
   - Datalad if `.datalad/` exists and VC mode is datalad.
   - If VC mode is none, do not run VC commands unless explicitly requested.
5. Report resolved profile before making changes (language, env, toolchain, VC mode, key paths).

## Verify
- Data access policy exists in `pyproject.toml` under `[tool.data_policy]`.
- Sensitive paths from policy are present in `.codexignore`, `.claudeignore`, and `.cursorignore`.
- Chosen commands match `pyproject.toml` and detected markers.
- Any config-vs-filesystem mismatch is explicitly reported.
- Downstream skills use this resolved profile.

