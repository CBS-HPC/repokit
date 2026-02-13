# CLI Actionability Matrix

This matrix classifies commands as:
- `machine-actionable`: safe for autonomous/headless execution.
- `conditionally interactive`: can prompt depending on state/config; provide all inputs and preconditions.
- `human-interactive`: designed for UI/prompt-based interaction.

## repokit

### machine-actionable
- `repokit deps-update` (`repokit deps`)
- `repokit readme-update` (`repokit readme`)
- `repokit templates-reset` (`repokit templates`)
- `repokit examples-code` (`repokit ex-code`)
- `repokit examples-test` (`repokit tests`, `repokit ex-test`, `repokit ex-tests`)
- `repokit ci-control` (`repokit ci`) with explicit `--on` or `--off`
- `repokit lint`
- `repokit agent init` (without guided interactive mode)

### conditionally interactive
- `repokit copy`
  - prompts if `--remote-path`/`--local-path` omitted or destination conflicts.
- `repokit git-config` (`repokit git`)
  - can prompt for version control, host, user/token, git identity, storage path.

### safe automation notes
- Always provide paths for `repokit copy`.
- Avoid `repokit git-config` unless all required env/config values are already set and no setup prompts are expected.

## repokit-backup

### machine-actionable
- `repokit-backup list`
- `repokit-backup types`
- `repokit-backup diff --remote <name>`
- `repokit-backup transfer --source <a> --destination <b> [--mode copy|sync] [--confirm]`
  - `--confirm` controls dry-run behavior; not an input prompt.

### conditionally interactive
- `repokit-backup add --remote <name> [--local-path <path>]`
  - often prompts for base folder, credentials, or backend-specific config.
- `repokit-backup push --remote <name> [...]`
  - may trigger setup prompts for SFTP/ucloud host/port/key if not configured.
- `repokit-backup pull --remote <name> [...]`
  - same conditional prompts as push.
- `repokit-backup delete --remote <name|all>`
  - explicit confirmation prompt before destructive delete.

### safe automation notes
- Prefer existing remotes and fully configured registry before push/pull.
- Avoid `delete` in autonomous runs unless a non-interactive delete path is implemented.

## repokit-dmp

### machine-actionable
- `repokit-dmp update`
- `repokit-dmp dataset`
- `repokit-dmp dcas-migration`

### human-interactive
- `repokit-dmp editor`
  - Streamlit UI with forms/buttons/tokens/upload/download.

### safe automation notes
- For autonomous DMP work, use:
  - `repokit-dmp update`
  - `repokit-dmp dataset`
  - `dmp-schema-sync` skill for schema mapping/validation report.

## Interaction triggers to watch for

If a command path includes any of these, treat as interactive-risk:
- `input(...)`, password prompts, confirm prompts
- setup wizards/auth flows
- browser/device auth
- UI frameworks (for example Streamlit)

## Decision rule

1. Prefer `machine-actionable` commands.
2. Use `conditionally interactive` commands only with all required parameters and preconfigured state.
3. Escalate `human-interactive` commands to human-in-the-loop.
