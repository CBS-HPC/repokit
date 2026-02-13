---
name: test-driven-development
description: Follow test-driven development (red-green-refactor) with language-appropriate test frameworks selected from pyproject.toml and detected project structure.
---

# test-driven-development

## Skill dependencies
- `activate_project`: resolve language/environment/toolchain before writing and running tests.
- `lint-language-profiles`: source of truth for broader language-specific checks during refactor/expand steps.

## Use when
- Implementing new behavior or fixing bugs.
- A task can be expressed as executable acceptance tests.
- You want minimal regressions with incremental proof of correctness.

## Pre-checks
- Parse `pyproject.toml` for language, environment manager, and configured test tools.
- Detect code and test layout (`src/`, `tests/`, `R/`, `tests/testthat/`, `*.do`, `*.m`).
- Detect environment markers (`.venv/`, `.conda/`, `uv.lock`, `environment.yml`, `renv.lock`).
- Use `activate_project` first to resolve runtime/toolchain profile.

## Workflow (Red-Green-Refactor)
1. Red:
   - Write or update a failing test that captures the requested behavior.
   - Run the smallest relevant test target and confirm failure.
2. Green:
   - Implement the minimal code change required to pass that test.
   - Re-run the same test target until it passes.
3. Refactor:
   - Improve structure/readability while preserving behavior.
   - Re-run tests after each meaningful refactor.
4. Expand:
   - Add edge-case tests for discovered boundaries.
   - Run broader, language-appropriate checks before completion.

## Tooling selection
- Python: `pytest` (and configured test/lint/type checks from `pyproject.toml` and skills).
- R: project test command or `testthat`/`Rscript` workflows when configured.
- Stata: project `.do` test/lint scripts when available.
- MATLAB: project `.m` test/lint scripts when available.

## Verify
- A new or updated test fails before implementation and passes after.
- Related regression and edge-case tests pass.
- Test commands and results are documented in `TASKS.md` when applicable.
