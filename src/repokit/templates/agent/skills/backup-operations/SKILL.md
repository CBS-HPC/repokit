---
name: backup-operations
description: Manage backup remotes and data sync with repokit-backup commands and verification checks.
---

# backup-operations

## Skill dependencies
- `activate_project`: resolve project profile before backup commands.
- `vc-governance`: align backup behavior with active VC mode.

## Automation safety
- Use non-interactive command forms only (`--remote <remote>` explicitly set).
- If a command requires credential entry, browser auth, or manual confirmation, stop and request human input.
- Do not run destructive sync/recovery operations unless explicitly requested.

## Pre-checks
- Parse `pyproject.toml` for backup/storage configuration (for example `REMOTE_BACKUP`, `REMOTE_STORAGE`) and policy constraints.
- Confirm backup operations are enabled by config or explicitly requested.
- Verify repo and ignore markers relevant to sync scope (for example `.git/`, `.dvc/`, `.datalad/`, `.rcloneignore`).

## Workflow
1. Configure remote:
   - repokit-backup add --remote <remote>
2. Push:
   - repokit-backup push --remote <remote>
3. Pull (recovery/testing):
   - repokit-backup pull --remote <remote>
4. Compare state:
   - repokit-backup diff --remote <remote>

## Verify
- Remote config exists and secrets are not committed.
- Diff output is reviewed before destructive operations.
