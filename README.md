# repokit

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/CBS-HPC/repokit/actions/workflows/ci.yml/badge.svg)](https://github.com/CBS-HPC/repokit/actions/workflows/ci.yml)

Core utilities for the **Research Template** setup flow. `repokit` provides reusable setup helpers, CLI tools, and automation used by the cookiecutter template. It composes smaller, independent packages:

- **repokit-common**: shared utilities (env, prompts, paths, config helpers)
- **repokit-backup**: rclone-based backup tooling
- **repokit-dmp**: data management plan (DMP) tooling

## Installation

```bash
pip install repokit
```

From source:

```bash
git clone https://github.com/CBS-HPC/repokit.git
cd repokit
pip install -e .
```

## CLI

`repokit` provides a core CLI plus two companion CLIs that ship via dependencies:

- `repokit` (core)
- `repokit-backup` (backup/sync)
- `repokit-dmp` (DMP tooling)

### `repokit` commands

| Command | Description |
|---------|-------------|
| `repokit copy` | Copy/sync files based on project rules. |
| `repokit deps-update` (`repokit deps`) | Update dependency metadata and lockfiles. |
| `repokit readme-update` (`repokit readme`) | Regenerate `README.md`. |
| `repokit templates-reset` (`repokit templates`) | Regenerate script templates. |
| `repokit examples-code` (`repokit ex-code`) | Generate code example scripts. |
| `repokit examples-test` (`repokit ex-test`) | Generate test examples. |
| `repokit git-config` | Apply Git configuration helpers. |
| `repokit ci-control` | Enable/disable CI configuration. |
| `repokit lint` | Run language-aware linting. |
| `repokit agent` | Scaffold agent files/skills. |

## Notes

- See `repokit-backup` and `repokit-dmp` READMEs for their CLI details.

## License

MIT
