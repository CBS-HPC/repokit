---
name: dmp-schema-sync
description: Update and validate dmp.json against maDMP schema (1.2) in a fully headless workflow, producing a required-field mapping report without using the interactive editor.
---

# dmp-schema-sync

## Use when
- You need to update `dmp.json` without `repokit-dmp editor`.
- You want schema-based validation and a machine-readable mapping report.
- You need to confirm required maDMP fields are present/missing.

## Skill dependencies
- `activate_project`: resolve project profile and toolchain first.

## Pre-checks
- Ensure project root contains `pyproject.toml`.
- Prefer schema cache at `./bin/maDMP-schema-1.2.json`.
- If schema cache is missing, run `repokit-dmp update` once to fetch/cache schema.
- Treat `repokit-dmp editor` as human-interactive and out-of-scope for this skill.

## Workflow (headless)
1. Update normalized DMP:
   - `repokit-dmp update`
2. Sync dataset metadata into DMP:
   - `repokit-dmp dataset`
3. Ensure schema file exists:
   - `./bin/maDMP-schema-1.2.json`
4. Build required-field mapping report:
   - `python skills/dmp-schema-sync/scripts/map_dmp_schema.py --dmp dmp.json --schema ./bin/maDMP-schema-1.2.json --out dmp_schema_map.json`
5. If `jsonschema` is available, include validation errors in the report.

## Outputs
- Updated `dmp.json`
- Mapping/validation report at `dmp_schema_map.json`

## Verify
- `dmp.json` exists and is valid JSON.
- `dmp_schema_map.json` exists and lists:
  - required field paths discovered from schema
  - present required paths
  - missing required paths
  - validation errors (if validator is available)
