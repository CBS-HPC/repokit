---
name: dmp-governance
description: Maintain FAIR/RDM quality with repokit-dmp commands for dataset registration, dmp updates, and publication checks.
---

# dmp-governance

## Skill dependencies
- `activate_project`: resolve language/environment/VC context before DMP actions.
- `vc-governance`: ensure DMP/data actions follow selected VC mode.
- `dmp-schema-sync`: source of truth for headless maDMP update/mapping/validation.

## Automation safety
- Default to machine-actionable commands only.
- Treat `repokit-dmp editor` as human-interactive; run it only when explicitly requested by a human.
- For autonomous runs, use `repokit-dmp dataset` and `repokit-dmp update`, then edit files directly if needed.

## Pre-checks
- Parse `pyproject.toml` sections relevant to datasets and migration metadata (for example `tool.datasets`, `tool.dcas`).
- Verify configured dataset path patterns match current repository paths.
- Detect active version-control markers (`.git/`, `.dvc/`, `.datalad/`) and follow the selected mode.

## Workflow
1. Register datasets:
   - repokit-dmp dataset
2. Normalize/update DMP:
   - repokit-dmp update
3. Run schema mapping/validation report:
   - Use `dmp-schema-sync` skill workflow
4. Manual interactive editing (human-in-the-loop only):
   - repokit-dmp editor

## Verify
- dmp.json structure is valid and up to date.
- Dataset metadata references match actual local/remote resources.
