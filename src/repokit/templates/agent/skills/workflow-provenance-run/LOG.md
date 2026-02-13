# workflow-provenance-run log

Use this file to track draft iterations and design decisions for this skill.

## Entry template
- Date: YYYY-MM-DD
- Change:
- Rationale:
- Open questions:

## 2026-02-13
- Change: Initial draft skill created (`SKILL.md`) and logging policy added.
- Rationale: Keep provenance-run design iterative before integrating into `AGENTS.md`.
- Open questions:
  - Should provenance manifest follow strict W3C PROV JSON-LD or a pragmatic custom schema first?
  - How should default input/output discovery work for `datalad run`?
  - Should exploratory DVC runs default to `dvc exp run` unless user asks for baseline update?
