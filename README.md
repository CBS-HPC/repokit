# repokit

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/CBS-HPC/repokit/actions/workflows/ci.yml/badge.svg)](https://github.com/CBS-HPC/repokit/actions/workflows/ci.yml)

Core utilities for the Research Template setup flow. `repokit` provides reusable setup helpers, CLI tools, and automation used by the cookiecutter template. It composes smaller, independent packages:

- repokit-common: shared utilities (env, prompts, paths, config helpers)
- repokit-backup: rclone-based backup tooling
- repokit-dmp: data management plan (DMP) tooling

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

## CLI overview

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
| `repokit tests` (`repokit examples-test`, `repokit ex-test`) | Generate test examples. |
| `repokit git` | Apply Git configuration helpers. |
| `repokit ci` | Enable/disable CI configuration. |
| `repokit lint` | Run language-aware linting. |
| `repokit agent` | Scaffold agent files/skills. |

Below is a detailed description of each CLI command available in the project, including usage, behavior, and example output.

### <a id="repokit-deps-update"></a>
<details>
<summary><strong>📦 <code>repokit deps-update</code></strong></summary>

The `repokit deps-update` command scans your project for imported packages and updates your dependency files (`requirements.txt`, `environment.yml`, and `uv.lock`) accordingly. It supports Python, R, MATLAB, and Stata, using language-specific tooling to track packages across `./src/` (or `./R/`, `./stata/do/`).

This command is useful for keeping your project environment reproducible and ensuring that all scripts and notebooks reference installable dependencies.

#### Usage

```bash
repokit deps-update
```

#### What it does

- Regenerates `requirements.txt` using `pip freeze`
- Ensures missing packages are added to `uv.lock` (if used)
- Scans the `./src/` (or `./R/`, `./stata/do/`) directories for imports and writes dependency lists:
  - `./src/dependencies.txt` (or `R/`, `stata/`)
- Updates and tags `environment.yml` and `requirements.txt` with platform-specific selectors (via `platform_rules`)
- Runs `renv` for R, or language-specific setup scripts for MATLAB and Stata

> Paths and rules are derived from the `pyproject.toml` and `platform_rules.json` config.

#### Example output

```bash
📄 requirements.txt has been created successfully.
✅ Conda environment file created: environment.yml
✅ requirements.txt updated with platform tags
✅ Updated environment.yml with Conda-style platform tags
```

---
</details>

### <a id="repokit-readme-update"></a>
<details>
<summary><strong>📝 <code>repokit readme-update</code></strong></summary>

The `repokit readme-update` command regenerates your `README.md` with up-to-date project information, including:

- Code metadata and environment details
- Project folder structure as a tree diagram
- Software dependencies (from `dependencies.txt`)
- Auto-generated descriptions for core files and scripts

This helps maintain a professional and standardized `README.md` that aligns with reproducibility and publication requirements (e.g., DCAS).

#### Usage

```bash
repokit readme-update
```

#### What it does

- Reads the selected programming language from `.cookiecutter`
- Parses existing files and structure to infer documentation
- Updates or inserts:
  - Code dependency section (`code_dependencies` fenced block)
  - File descriptions from `file_descriptions.json`
  - Directory structure (`tree` block in README)
- Regenerates the `README.md` with consistent formatting
- Automatically creates `README.md` if it doesn’t exist

> File and folder annotations are pulled from `file_descriptions.json`.
> Files ignored by `.treeignore` or `pyproject.toml -> treeignore.patterns` are excluded from the directory tree.

---
</details>

### <a id="repokit-examples-code"></a>
<details>
<summary><strong>💡 <code>repokit examples-code</code></strong></summary>

The `repokit examples-code` command generates realistic starter scripts and notebooks for your selected programming language using predefined Jinja2 templates.

This is useful for quickly bootstrapping a project with well-structured, language-appropriate examples for each analysis stage.

#### Usage

```bash
repokit examples-code
```

#### What it does

- Detects your project language from `.cookiecutter`
- Renders example scripts for:
  - `s00_main.*` (pipeline entry point)
  - `s01_install_dependencies.*` (dependency setup)
  - `s02_utils.*` (helper functions)
  - `s03_data_collection.*` to `s06_visualization.*` (workflow stages)
- Saves outputs in the appropriate `./src/`, `R/`, `stata/do/`, etc.
- Calls:
  - `get_dependencies` to update `dependencies.txt`
  - `repokit readme-update` to regenerate project metadata

> Uses templates from `repokit/templates/j2/example` inside the package.
> Script locations depend on your selected programming language.
> Existing files will be overwritten if they share the same name.

---
</details>

### <a id="repokit-templates-reset"></a>
<details>
<summary><strong>🧱 <code>repokit templates-reset</code></strong></summary>

The `repokit templates-reset` command regenerates all core analysis and test scripts using predefined Jinja2 templates. It ensures a consistent structure and coding pattern across different scripting languages.

This command is useful for initializing or resetting project scripts to their default structure.

#### Usage

```bash
repokit templates-reset
```

#### What it does

- Automatically detects your selected programming language from `.cookiecutter`
- Regenerates standard source scripts:
  - `s00_main.*` (pipeline orchestration)
  - `s01_install_dependencies.*` (package installation)
  - `s02_utils.*` (shared utilities)
  - `s03_data_collection.*` to `s06_visualization.*` (analysis stages)
  - `get_dependencies.*` (collects project dependencies)
- Generates:
  - `s00_workflow.*` (interactive notebook)
  - `test_*.*` (unit test scaffolds)

#### Output paths

- Scripts are placed in:
  - `./src/`, `./R/`, `./stata/do/`, or equivalent source directory
- Test templates are placed in:
  - `./tests/`, `./tests/testthat/`, etc., depending on language

> Uses Jinja2 templates stored in `repokit/templates/j2/code` inside the package.
> Existing scripts with the same name may be overwritten.

---
</details>

### <a id="repokit-git"></a>
<details>
<summary><strong>🌐 <code>repokit git</code></strong></summary>

The `repokit git` command sets up your version control system and configures a remote Git repository on GitHub, GitLab, or Codeberg based on environment settings.

This command streamlines the process of remote repo creation, authentication, Git setup, and CI pipeline configuration.

#### Usage

```bash
repokit git
```

#### What it does

- Reads repository settings from `.cookiecutter` and environment variables:
  - `REPO_NAME`, `CODE_REPO`, `VERSION_CONTROL`, `PROJECT_DESCRIPTION`
- Configures Git remotes using platform APIs:
  - GitHub REST API
  - GitLab API
  - Codeberg API
- Authenticates using personal access tokens (`GITHUB_TOKEN`, `GITLAB_TOKEN`, etc.)
- Initializes remote repositories and sets the correct `origin` URL
- Pushes the local repo to the remote and sets the tracking branch
- Automatically sets up CI configuration via `ci_config()`

#### Supports

- GitHub (requires `gh` CLI or PAT)
- GitLab (installs and uses `glab` CLI or token)
- Codeberg (via Gitea API + token)

> Remote login and repo creation are tested via platform-specific APIs.
> Pushes both root repo and data repo (if applicable).
> Can auto-install `gh` or `glab` if not found locally.

---
</details>

### <a id="repokit-ci"></a>
<details>
<summary><strong>⚙️ <code>repokit ci</code></strong></summary>

The `repokit ci` command lets you enable or disable Continuous Integration (CI) for your project, and generates default CI configurations for your selected language and Git platform (GitHub, GitLab, or Codeberg).

This tool is helpful for bootstrapping or adjusting your CI setup without manually editing `.yml` files.

#### Usage

```bash
repokit ci --on     # Enable CI
repokit ci --off    # Disable CI
```

> You must specify one flag: `--on` or `--off`.
> This command is safe to run multiple times and won't overwrite existing CI files.

#### What it does

- Automatically generates CI config based on:
  - Programming language (from `.cookiecutter`)
  - Git hosting service (`CODE_REPO`)
- Supports:
  - `.github/workflows/ci.yml` for GitHub
  - `.gitlab-ci.yml` for GitLab
  - `.woodpecker.yml` for Codeberg
- Adds a `git commit-skip` alias for bypassing CI on minor commits
- Enables/disables CI by renaming files:
  - `ci.yml.disabled` ↔ `ci.yml`
  - `.gitlab-ci.yml.disabled` ↔ `.gitlab-ci.yml`
  - `.woodpecker.yml.disabled` ↔ `.woodpecker.yml`

#### Notes

- Installs CI templates from `repokit/templates/j2/ci` inside the package
- Only runs if a valid `CODE_REPO` is set
- CI files can be removed manually using `remove_ci_configs()` in code

---
</details>

### <a id="repokit-lint"></a>
<details>
<summary><strong>🧹 <code>repokit lint</code></strong></summary>

`repokit lint` runs project linting in a language-aware way. It looks for scaffolded scripts and executes them if present:

- Python → `src/linting.py` → Ruff (formatter + linter) and Mypy (type checker)
- R → `R/linting.R` → lintr::lint_dir() (auto-activates `renv` if `R/renv/activate.R` exists)
- MATLAB → `src/linting.m` → checkcode (static analysis)

#### Usage

```bash
repokit lint
```

#### Requirements

- Python: `ruff`, `mypy`
- R: `lintr` in your project’s `renv` (if used)
- MATLAB: `matlab` CLI on `PATH`

> The Python and MATLAB scripts live under `src/`, the R script under `R/`.
> CI YAML: implement a dedicated lint job/stage.

---
</details>

## Notes

- See `repokit-backup` and `repokit-dmp` READMEs for their CLI details.

## License

MIT


