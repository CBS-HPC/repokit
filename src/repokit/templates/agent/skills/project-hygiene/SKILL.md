---
name: project-hygiene
description: Run lint/type/test checks, auto-fix safe issues, and iterate until clean or blocked with a clear fix list.
---

# project-hygiene

## Skill dependencies
- `activate_project`: resolve project execution profile first.
- `lint-language-profiles`: source of truth for language-specific lint/type/test commands.

## Pre-checks
- Parse `pyproject.toml` for selected language, environment manager, and configured checks.
- Detect environment markers (`.venv/`, `.conda/`, `uv.lock`, `environment.yml`, `renv.lock`) and code layout (`src/`, `R/`, `*.do`, `*.m`).
- Use `lint-language-profiles` for language-specific check selection before running fixes.

## Workflow
1. Run baseline checks:
   - Run `repokit lint` when configured/available.
   - Run language-appropriate lint/type/test checks from `lint-language-profiles`.
2. Apply safe fixes:
   - Apply tool-native safe auto-fixes only for active languages/toolchains.
3. Re-run all checks.

## Completion
- All configured checks pass, or
- Remaining failures are documented with exact files and required code changes.
