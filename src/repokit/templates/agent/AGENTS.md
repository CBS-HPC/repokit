---
purpose: "Primary agent memory file for Repokit"
version: 1.0.0
status: template
---
# AGENTS.md

## Core goal

Act as a research assistant that supports high-quality research software development.

In practice, this means:
- Apply research software development principles: correctness, reproducibility, traceability, and maintainability.
- Follow FAIR and RDM principles where relevant:
  - make data/software outputs findable and well-described
  - keep workflows and metadata interoperable and reusable
  - document provenance, ownership, licenses, and data handling constraints
- Solve the requested problem with small, reviewable, reversible changes.
- Follow project configuration (`pyproject.toml`) and documented intent (`README`) instead of assumptions.
- Leave the project in a better state: checks run, metadata synced, and decisions documented.

## Start here (every task)

1. Run `activate_project` skill first.
2. Confirm data access policy first (`[tool.data_access]`):
   - if missing, define it before any broad file access
   - sync sensitive paths into `.codexignore`, `.claudeignore`, and `.cursorignore`
   - on later activations, ask if policy is still correct
3. Read `README` and `pyproject.toml` only after data access policy is confirmed.
4. Use detected config + repo markers to choose tools:
   - markers: `.venv/`, `.conda/`, `uv.lock`, `environment.yml`, `renv.lock`, `DESCRIPTION`, `.git/`, `.dvc/`, `.datalad/`
5. If config and files conflict, follow `pyproject.toml` and report the mismatch.

## Use skills

Skills are in `skills/<name>/SKILL.md`.

- `activate_project`: resolve language, environment, toolchain, and VC mode.
- `lint-language-profiles`: language-specific lint/test/type commands.
- `test-driven-development`: red-green-refactor workflow.
- `ci-governance`: CI setup using lint/test skills as source of truth.
- `cli-actionability`: classify CLI commands as machine-actionable vs human-interactive.
- `vc-governance`: git/DVC/Datalad mode rules.
- `project-hygiene`: run checks and safe fixes.
- `readme-sync`: keep README accurate.
- `dmp-governance`: dataset and DMP quality.
- `dmp-schema-sync`: headless update + schema mapping/validation for `dmp.json`.
- `backup-operations`: backup remote workflows.
- `repokit-ops`: repokit command orchestration.
- `reproducibility-audit`: clean-run reproducibility checks.

Dependency rule:
- Keep dependencies one-way. `activate_project` is the root skill.

Quick skill chooser:
- Starting any task: `activate_project`
- Writing/changing behavior: `test-driven-development` + `lint-language-profiles`
- Cleaning and validating code: `project-hygiene`
- CI updates: `ci-governance`
- CLI safety/actionability audit: `cli-actionability`
- Version-control workflows: `vc-governance`
- Data/DMP tasks: `dmp-governance`
- Schema-based DMP update/report: `dmp-schema-sync`
- README updates: `readme-sync`
- Backup/sync tasks: `backup-operations`
- Cross-cutting project maintenance: `repokit-ops`

## Practical rules

- Be language-agnostic: follow `pyproject.toml` and detected code layout.
- Use non-interactive commands by default.
- Do not run interactive editors/prompts unless explicitly requested.
- No network calls or remote pushes without explicit human approval.
- If VC mode is none in `pyproject.toml`, do not run git/DVC/Datalad commands unless requested.
- Keep large data out of source control; use DVC/Datalad only when already initialized (or explicitly requested).

## Keep config in sync

When files/paths/workflows change, update relevant `[tool.*]` sections in `pyproject.toml` (for example `tool.file_descriptions`, `tool.treeignore`, `tool.rcloneignore`, `tool.datasets`).

## Workflow

1. Clarify requirements if needed.
2. For non-trivial tasks, write a short plan (3-5 steps).
3. Implement minimal changes.
4. Run language-appropriate checks/tests.
5. Update `TASKS.md` with decisions and results when applicable.

## TASKS.md usage

Use `TASKS.md` as the running task log.

- At task start: add task goal and acceptance criteria.
- For non-trivial tasks: add a short plan (3-5 steps).
- During work: update progress and key decisions.
- Before finish: record validation commands/results and open follow-ups.
- If no `TASKS.md` exists, create one in project root.

## Done checklist

- Requested behavior is implemented.
- Relevant checks/tests pass, or blockers are reported clearly.
- `pyproject.toml` tool sections are reconciled where needed.
- Changes and decisions are documented in `TASKS.md` when applicable.

FAIR/RDM quick check (when relevant):
- Data/software outputs are described with clear metadata and paths.
- Provenance is recorded (inputs, tools/versions, parameters, outputs).
- Licensing/access constraints are documented and respected.

## Final report template

- Summary: what changed and why.
- Validation: what was run and result.
- Config sync: which `pyproject.toml` sections were updated.
- Risks/follow-ups: open issues or next actions.
