---
name: cli-actionability
description: Determine whether repokit, repokit-backup, and repokit-dmp commands are machine-actionable or require human interaction, and choose safe non-interactive command paths.
---

# cli-actionability

## Use when
- Choosing commands for automation or agent execution.
- Auditing whether a workflow can run headlessly.
- Avoiding accidental interactive prompts during autonomous runs.

## Pre-checks
- Run `activate_project` first.
- Confirm target CLI and subcommand (`repokit`, `repokit-backup`, `repokit-dmp`).
- Read `references/cli_actionability.md` for current classification and caveats.

## Workflow
1. Identify the exact subcommand and options to run.
2. Classify it using the matrix in `references/cli_actionability.md`:
   - `machine-actionable`
   - `conditionally interactive`
   - `human-interactive`
3. If command is `conditionally interactive`, provide required flags/inputs/paths to avoid prompts.
4. If command is `human-interactive`, stop and request explicit human handling or a headless alternative.
5. Record the classification and selected path in `TASKS.md` when applicable.

## Verify
- Chosen command path does not require `input()`/UI interaction at runtime.
- Any required human step is explicitly called out before execution.
- For DMP updates, prefer `dmp-schema-sync` over `repokit-dmp editor` in autonomous runs.
