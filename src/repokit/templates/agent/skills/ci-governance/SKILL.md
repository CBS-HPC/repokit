---
name: ci-governance
description: Keep CI aligned with project language and version-control mode, and enforce reproducibility checks.
---

# ci-governance

## Skill dependencies
- `activate_project`: resolve language, environment, and VC mode before CI changes.
- `lint-language-profiles`: source of truth for language-specific lint/type check commands.
- `test-driven-development`: source of truth for language-specific test execution strategy.

## Pre-checks
- Parse `pyproject.toml` for selected language, environment manager, and version-control mode.
- Detect relevant markers (`.git/`, `.dvc/`, `.datalad/`, `.venv/`, `.conda/`, `uv.lock`, `environment.yml`, `renv.lock`).
- Detect CI platform/config files and target only the active provider:
  - GitHub: `.github/workflows/*.yml` or `.github/workflows/*.yaml`
  - GitLab: `.gitlab-ci.yml`
  - Codeberg/Forgejo/Gitea Actions: `.forgejo/workflows/*.yml`, `.forgejo/workflows/*.yaml`, `.gitea/workflows/*.yml`, `.gitea/workflows/*.yaml`
  - Codeberg Woodpecker: `.woodpecker.yml`, `.woodpecker.yaml`, `.woodpecker/*.yml`, `.woodpecker/*.yaml`
- If version control is set to none, do not apply CI toggles unless explicitly requested.

## Workflow
1. Enable or disable CI via repokit:
   - repokit ci --on
   - repokit ci --off
2. Build CI commands from dependent skills:
   - lint/type checks from `lint-language-profiles`
   - test commands from `test-driven-development`
3. Verify workflow file reflects active toolchain and selected VC mode.
4. Ensure checks include only language-appropriate commands for the detected/configured stack.

## Verify
- CI config matches selected language and VC mode.
- Commands in CI are consistent with dependent skill guidance and runnable from a clean environment.

