---
name: lint-language-profiles
description: Apply language-aware lint profiles for Python, R, Stata, and MATLAB projects.
---

# lint-language-profiles

## Skill dependencies
- `activate_project`: resolve language, environment, and toolchain before selecting profiles.

## Pre-checks
- Parse `pyproject.toml` for configured language, environment manager, and lint/test tool preferences.
- Detect code and environment markers (`src/`, `R/`, `*.do`, `*.m`, `.venv/`, `.conda/`, `uv.lock`, `environment.yml`, `renv.lock`, `DESCRIPTION`).
- Run only profiles relevant to detected/configured languages.

## Python
- ruff check .
- ruff format --check .
- mypy src
- pytest

## R
- Run Rscript -e  lintr::lint_dir R  if R sources exist.
- Run project test command if present.

## Stata
- Run project lint script (src/linting.do) and inspect output logs.

## MATLAB
- Run project lint script (src/linting.m) and parse checkcode output.

## Mixed projects
- Run all relevant profiles and aggregate failures before fixing.
