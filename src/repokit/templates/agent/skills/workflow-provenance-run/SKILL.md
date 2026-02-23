---
name: workflow-provenance-run
description: Draft skill for running end-to-end project workflows with provenance capture, preferring datalad or dvc when available.
---

# workflow-provenance-run (Draft)

## Status
- Draft only. Not yet integrated into `AGENTS.md`.
- Intended for iterative refinement.
- Maintain progress notes in `LOG.md` in this skill folder.

## Use when
- Running a full project workflow (for example `main.py`, `main.R`, `s00_main.py`, `00_main.py`).
- Capturing reproducibility/provenance for a workflow run.
- Producing a traceable run record for FAIR/RDM reporting.

## Preconditions
- Run `activate_project` first.
- Respect `[tool.data_policy]` policy and ignore files before touching data paths.
- Use non-interactive command paths.

## Entrypoint detection (default order)
1. User-provided explicit command (highest priority).
2. Project-defined command from config (if present).
3. Conventional entrypoints in repo root or code dir:
   - Python: `main.py`, `s00_main.py`, `00_main.py`
   - R: `main.R`, `s00_main.R`, `00_main.R`
   - Stata: `main.do`, `s00_main.do`, `00_main.do`
   - MATLAB: `main.m`, `s00_main.m`, `00_main.m`

## Provenance backend decision tree
1. If `.datalad/` exists:
   - Prefer `datalad run -m "<message>" -i <inputs> -o <outputs> "<cmd>"`
   - Require explicit input/output declaration for high-quality provenance.
2. Else if `.dvc/` exists:
   - Stable/baseline run: `dvc repro`
   - Exploratory run: `dvc exp run`
3. Else:
   - Run command directly and write provenance manifest (`provenance/run-<timestamp>.json`).

## Minimum provenance fields to record
- Timestamp, duration, cwd, command, args, exit code.
- Git commit hash and dirty state.
- VC mode (`datalad`/`dvc`/`git`/`none`).
- Runtime/tool versions (Python/R + key tools).
- Declared inputs and outputs.
- Checksums or file stats for key outputs.
- Data-access mode used (`blocked`, `metadata-only`, `allowed`).

## Suggested outputs
- `provenance/run-<timestamp>.json` (machine-readable manifest)
- `provenance/latest.md` (human-readable summary)

## Verification checklist
- Workflow run result is recorded (success/failure).
- Provenance artifact(s) are written.
- If DataLad/DVC exists, backend-specific provenance command was used.
- Inputs/outputs are explicit (especially for `datalad run`).
- Any policy constraints or blocked paths are reported.

## Open design questions (for later refinement)
- Exact schema for `provenance/run-*.json` (W3C PROV-compatible or custom).
- How to auto-discover safe default inputs/outputs.
- When to auto-save/commit (and when to require human approval).
- How strict validation should be when entrypoint detection is ambiguous.

## Iteration log
- Keep a running design/change log in `LOG.md`.
- Add one entry per revision with:
  - date
  - what changed
  - rationale
  - open questions

