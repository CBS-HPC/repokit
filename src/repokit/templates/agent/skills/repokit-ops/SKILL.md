---
name: repokit-ops
description: Run core repokit CLI workflows with verification steps for dependencies, README sync, templates, and CI toggles.
---

# repokit-ops

## Use when
- You need to run repokit commands as part of project maintenance.
- You want consistent command order and post-run checks.

## Workflow
1. Run dependency sync:
   - repokit deps
2. Regenerate README:
   - repokit readme
3. Refresh templates/examples when requested:
   - repokit templates
   - repokit ex-code
   - repokit tests
4. Manage CI when requested:
   - repokit ci --on or repokit ci --off

## Verify
- git status --short reflects expected file changes only.
- Generated files are still valid (README.md, env files, template outputs).

